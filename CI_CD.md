# CI/CD Documentation

This document describes the Continuous Integration / Continuous Deployment
pipeline for pyffice.

## Overview

Pyffice uses automated CI/CD pipelines for validating code quality, running
the test matrix across supported Python versions, and publishing releases.

## Pipeline Stages

1. **Lint & Format** — ruff + black formatting checks across the codebase
2. **Test** — Unit + integration test suites (Python 3.10, 3.11, 3.12)
3. **Audit** — Sasquatch compliance auditor (security, maintainability, etc.)
4. **Build** — Package assembly via setuptools / poetry
5. **Deploy** — Publish to internal package registry

## Local Validation

```bash
# Run all checks locally
pytest tests/ -v
sasquatch analyze -p . --skip-pii-secrets
black . && ruff check .
```

## CI Configuration

CI runs the same checks as `local validation` on every push and pull
request. Coverage reports and audit artifacts are uploaded as build
artifacts.

## Deployment

Releases are tagged automatically when all stages pass. Manual approval is
required for production deployments.

## Secrets

- All secrets stored in PyKeyStore (encrypted at rest)
- No environment variables used for credentials
- CI uses short-lived tokens with workload identity federation
- The PyKeyStore passphrase prompt is deliberate (TTY-bound at runtime)
