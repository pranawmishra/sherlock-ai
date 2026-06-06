<p align="center">
  <img src="docs/logo.png" alt="Sherlock AI" width="460">
</p>

<p align="center">
    <em>AI-powered monitoring, logging & error analysis for Python — zero friction, production ready.</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/sherlock-ai"><img src="https://img.shields.io/pypi/v/sherlock-ai?color=%2300BFA5&label=pypi%20package" alt="PyPI version"></a>
  <a href="https://pypi.org/project/sherlock-ai"><img src="https://img.shields.io/pypi/pyversions/sherlock-ai?color=%2300BFA5" alt="Python versions"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-%2300BFA5" alt="MIT License"></a>
</p>

---

**Source Code**: [https://github.com/pranawmishra/sherlock-ai](https://github.com/pranawmishra/sherlock-ai)

---

## What is Sherlock AI?

Sherlock AI is a Python observability toolkit that **automatically monitors, logs, and analyzes** your application — performance, memory, resources, and errors — with minimal setup. Drop in a decorator and you're done.

- ⚡ **Auto-Instrumentation** — Zero-code setup for FastAPI (Sentry-style monkey-patching)
- 🤖 **AI-Powered Insights** — Error analysis & performance suggestions via Groq or Azure OpenAI
- 📊 **Full-Stack Monitoring** — Performance · Memory · CPU/I/O · Resources
- 🗄️ **Flexible Storage** — MongoDB or HTTP API ingestion
- 🔄 **Async/Sync** — Works seamlessly with both
- 🎛️ **Config Presets** — `development`, `production`, `minimal`, `performance_only`
- 📋 **JSON Logs** — Structured output ready for log aggregators

---

## Installation

```bash
pip install sherlock-ai
```

---

## Quick Start

### One-liner setup (FastAPI / any app)

```python
from sherlock_ai import SherlockAI, LoggingConfig, get_logger

# Auto-instruments all FastAPI routes — do this BEFORE creating the app
SherlockAI(config=LoggingConfig(auto_instrument=True)).setup()

logger = get_logger(__name__)
```

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    # ✅ Automatically monitored: performance, memory, resources, errors
    return {"status": "healthy"}
```

### Decorator-based setup

```python
from sherlock_ai import sherlock_ai, get_logger, log_performance
from sherlock_ai.monitoring import sherlock_error_handler

sherlock_ai()  # call once at startup
logger = get_logger(__name__)

@log_performance
@sherlock_error_handler
def process_data(user_id: str):
    logger.info("Processing user %s", user_id)
    return {"result": "ok"}
```

---

## Core Features

### Performance Monitoring

```python
from sherlock_ai import log_performance, PerformanceTimer

@log_performance(min_duration=0.1, include_args=True)
def slow_query(user_id, limit=10):
    ...

with PerformanceTimer("batch_job"):
    run_batch()
```

### Memory & Resource Monitoring

```python
from sherlock_ai import monitor_memory, monitor_resources

@monitor_memory(trace_malloc=True)
@monitor_resources(include_io=True, include_network=True)
def heavy_computation():
    ...
```

### AI Error Analysis

```python
import os
from sherlock_ai.monitoring import sherlock_error_handler

os.environ["GROQ_API_KEY"] = "your-key"          # default provider
# os.environ["LLM_PROVIDER"] = "azure_openai"    # or Azure

@sherlock_error_handler
def risky_operation():
    return 1 / 0  # error auto-analyzed and stored
```

### Hardcoded Value Detection

```python
from sherlock_ai import hardcoded_value_detector

@hardcoded_value_detector
def api_handler():
    url = "https://api.example.com"  # auto-extracted to constants.py
    timeout = 30
    ...
```

---

## Configuration

### Presets

```python
from sherlock_ai import sherlock_ai, LoggingPresets

sherlock_ai(LoggingPresets.development())   # DEBUG, verbose
sherlock_ai(LoggingPresets.production())    # INFO, optimized
sherlock_ai(LoggingPresets.minimal())       # console + app.log only
sherlock_ai(LoggingPresets.performance_only())
```

### Custom config

```python
from sherlock_ai import SherlockAI, LoggingConfig, LogFileConfig

config = LoggingConfig(
    logs_dir="my_logs",
    log_format_type="json",          # creates .json files
    auto_instrument=True,
    log_files={
        "app":         LogFileConfig("application", max_bytes=100*1024*1024),
        "errors":      LogFileConfig("errors", level="ERROR"),
        "performance": LogFileConfig("perf"),
    }
)
SherlockAI(config).setup()
```

### LLM Providers

| | Groq (default) | Azure OpenAI |
|---|---|---|
| **Env vars** | `GROQ_API_KEY` | `LLM_PROVIDER=azure_openai` + 3 vars |
| **Models** | Open-source (fast) | GPT-3.5 / GPT-4 |
| **Best for** | Dev / small teams | Enterprise |

```bash
# Groq
export GROQ_API_KEY="gsk_..."

# Azure OpenAI
export LLM_PROVIDER="azure_openai"
export AZURE_OPENAI_API_KEY="..."
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4-turbo"
```

### API / MongoDB storage

```bash
# Send insights to your own backend
export SHERLOCK_AI_API_KEY="your-key"
export SHERLOCK_AI_API_BASE_URL="https://your-backend.com/v1"  # optional

# Or use local MongoDB
export MONGO_URI="mongodb://localhost:27017"
```

---

## Log Format

**Standard**
```
2025-07-15 20:51:19 - aa580b62 - PerformanceLogger - INFO - PERFORMANCE | my_module.fn | SUCCESS | 1.003s
```

**JSON** (`log_format_type="json"`)
```json
{"timestamp": "2025-07-15 20:51:19", "level": "INFO", "message": "PERFORMANCE | my_module.fn | SUCCESS | 1.003s", "request_id": "aa580b62"}
```

---

## Requirements

- Python ≥ 3.8
- `psutil` · `astor` · `groq` · `openai` · `pymongo` · `requests`

---

## Authors

**Pranaw Mishra** · [pranawmishra73@gmail.com](mailto:pranawmishra73@gmail.com)
**Kunal Aggarwal** · [aggarwalkunu263@gmail.com](mailto:aggarwalkunu263@gmail.com)

---

## License

[MIT](LICENSE)