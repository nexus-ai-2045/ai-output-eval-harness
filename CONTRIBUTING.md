# Contributing

Thanks for improving `ai-output-eval-harness`.

## Local Setup

```powershell
python -m pip install -e .
python -m pytest
```

## Development Rules

- Keep the default path local-first and deterministic.
- Do not require external model calls for core tests.
- Add or update tests for evaluator, catalog, pipeline, and Obsidian behavior changes.
- Do not commit generated `reports/` output.
- Do not commit real private conversations, credentials, or user data.

## Public Data

Only use sample data that is synthetic, explicitly licensed, or otherwise safe to redistribute.

