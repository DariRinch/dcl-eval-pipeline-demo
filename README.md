# DCL Eval Pipeline — Demo

A lightweight evaluation framework for monitoring and auditing 
LLM agent behavior in multi-agent systems.

## What this is

This demo implements a basic evaluation pipeline for LLM outputs:
- prompt quality assessment
- response consistency checks  
- anomaly detection in agent decision chains
- structured logging of agent actions

Built as a practical exploration of LLM observability and 
audit infrastructure.

## Stack

- Python 3.10+
- OpenAI API
- DeepEval
- Jupyter Notebook
- pandas / matplotlib

## Structure

- [`eval/pipeline.py`](eval/pipeline.py) — core evaluation logic  
- [`eval/metrics.py`](eval/metrics.py) — quality metrics  
- [`prompts/templates.py`](prompts/templates.py) — prompt templates  
- [`notebooks/demo.ipynb`](notebooks/demo.ipynb) — interactive demo  
- [`data/sample_logs.json`](data/sample_logs.json) — sample agent logs

## Quick Start

pip install -r requirements.txt
jupyter notebook notebooks/demo.ipynb

## Status

Work in progress. Part of ongoing research into 
deterministic audit systems for AI agents.
