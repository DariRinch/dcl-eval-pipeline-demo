from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
import yaml
import litellm
import sys
import os

# Phoenix tracing for OpenAI calls
# import only when we plan to instrument to keep deps optional
collector_endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT")
if collector_endpoint:
    try:
        from phoenix.trace.openai import OpenAIInstrumentor

        OpenAIInstrumentor().instrument(endpoint=collector_endpoint)
    except Exception as e:  # pylint: disable=broad-except
        # logging is not initialized yet, simply print
        print(f"warning: Phoenix instrumentation failed: {e}")

sys.path.insert(0, os.path.abspath('..'))

from eval.metrics import score_consistency, score_length, score_anomaly
from prompts.templates import get_prompt

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = config["model"]["name"]

app = FastAPI(
    title="DCL Eval Pipeline API",
    description="Audit and evaluation API for LLM agent behavior in regulated industries.",
    version="0.1.0"
)

class EvalRequest(BaseModel):
    template: str
    kwargs: dict = {}

class MetricResult(BaseModel):
    prompt_id: str
    score: float
    passed: bool
    reason: str = None

class EvalResponse(BaseModel):
    timestamp: str
    template: str
    aggregate_score: float
    passed: bool
    metrics: list
    response: str


def call_llm(prompt: str) -> str:
    response = litellm.completion(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=config["model"]["max_new_tokens"],
        temperature=config["model"]["temperature"],
        api_key=HF_TOKEN
    )
    return response.choices[0].message.content.strip()

@app.get("/")
def root():
    return {"status": "ok", "service": "DCL Eval Pipeline API"}

@app.post("/evaluate", response_model=EvalResponse)
def evaluate(request: EvalRequest):
    try:
        template = get_prompt(request.template, **request.kwargs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    text = call_llm(template["prompt"])

    from dataclasses import asdict
    metrics = [
        asdict(score_consistency(text, template["expected_keywords"])),
        asdict(score_length(text)),
        asdict(score_anomaly(text, template["forbidden_patterns"]))
    ]

    aggregate = round(sum(m["score"] for m in metrics) / len(metrics), 2)
    passed = all(m["passed"] for m in metrics)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "template": request.template,
        "aggregate_score": aggregate,
        "passed": passed,
        "metrics": metrics,
        "response": text
    }

    with open(config["paths"]["logs"], "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")

    return result
