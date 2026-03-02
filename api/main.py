"""Basic API entrypoint for the evaluation pipeline.

This module can be expanded later to expose HTTP endpoints for running
evaluations, accessing metrics results, etc.  For now it provides a simple
placeholder function or minimal FastAPI app if a framework is desired.
"""

# Example skeleton using FastAPI (install via requirements.txt as needed)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from eval.pipeline import run_eval
from prompts.templates import get_prompt

app = FastAPI()

@app.get("/health")
def health_check():
    """Simple health endpoint."""
    return {"status": "ok"}


class EvaluateRequest(BaseModel):
    template: str
    # scenario and other template params are captured dynamically
    # we allow any other fields
    __root__: Dict[str, Any]


@app.post("/evaluate")
def evaluate(request: EvaluateRequest):
    data = request.__root__
    template_name = request.template

    # prepare prompt parameters (exclude template key)
    params = {k: v for k, v in data.items() if k != "template"}

    try:
        prompt_info = get_prompt(template_name, **params)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    eval_result = run_eval(
        prompt=prompt_info["prompt"],
        expected_keywords=prompt_info.get("expected_keywords", []),
        forbidden_patterns=prompt_info.get("forbidden_patterns"),
    )

    metrics = eval_result.get("metrics", [])
    if not metrics:
        raise HTTPException(status_code=500, detail="Evaluation produced no metrics")

    aggregate_score = round(sum(m.get("score", 0) for m in metrics) / len(metrics), 2)
    passed = all(m.get("passed") for m in metrics)

    return {
        "template": template_name,
        "aggregate_score": aggregate_score,
        "passed": passed,
        "metrics": metrics,
        "response": eval_result.get("response"),
    }
