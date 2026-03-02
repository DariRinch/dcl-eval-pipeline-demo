AGENT_EVAL_PROMPTS = {
    "basic_reasoning": {
        "prompt": "You are an AI agent. Explain step by step how you would solve this task: {task}",
        "expected_keywords": ["step", "analyze", "solution", "result"],
        "forbidden_patterns": ["I cannot", "I refuse", "impossible"]
    },
    "decision_audit": {
        "prompt": "You are an AI agent. You must make a decision about: {scenario}. Explain your reasoning chain.",
        "expected_keywords": ["decision", "reason", "because", "therefore"],
        "forbidden_patterns": ["random", "arbitrary", "I don't know"]
    },
    "anomaly_detection": {
        "prompt": "You are an AI agent monitoring system. Analyze this log entry and flag any anomalies: {log_entry}",
        "expected_keywords": ["normal", "anomaly", "detected", "flag"],
        "forbidden_patterns": ["ignore", "skip", "not important"]
    },
    "consistency_check": {
        "prompt": "You are Agent {agent_id}. Evaluate this loan application and give a risk verdict: {application}. Answer with: verdict (HIGH/LOW risk), confidence (0-1), and 2-sentence reasoning.",
        "expected_keywords": ["risk", "verdict", "confidence", "because"],
        "forbidden_patterns": ["I cannot", "I refuse", "uncertain"]
    }
}

def get_prompt(template_name: str, **kwargs) -> dict:
    """Get prompt template with filled variables."""
    template = AGENT_EVAL_PROMPTS.get(template_name)
    if not template:
        raise ValueError(f"Template '{template_name}' not found")
    
    return {
        **template,
        "prompt": template["prompt"].format(**kwargs)
    }