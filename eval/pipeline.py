import json
import openai
from datetime import datetime
from eval.metrics import score_consistency, score_length, score_anomaly

def run_eval(prompt: str, expected_keywords: list, forbidden_patterns: list = None) -> dict:
    """Run evaluation pipeline on a single prompt."""
    
    client = openai.OpenAI()
    
    # Get response from LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    text = response.choices[0].message.content
    
    # Run metrics
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "response": text,
        "metrics": [
            score_consistency(text, expected_keywords).__dict__,
            score_length(text).__dict__,
            score_anomaly(text, forbidden_patterns or []).__dict__
        ]
    }
    
    # Log to file
    with open("data/sample_logs.json", "a") as f:
        f.write(json.dumps(results, ensure_ascii=False) + "\n")
    
    return results

if __name__ == "__main__":
    result = run_eval(
        prompt="Explain what an AI agent is in simple terms.",
        expected_keywords=["agent", "task", "decision"],
        forbidden_patterns=["I cannot", "I refuse"]
    )
    
    for metric in result["metrics"]:
        status = "✓" if metric["passed"] else "✗"
        print(f"{status} {metric['prompt_id']}: {metric['score']} — {metric['reason']}")