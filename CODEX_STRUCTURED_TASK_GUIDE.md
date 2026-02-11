# Codex Implementation Guide for the Structured Task Prompt

This guide explains how to execute your `MODE: STRUCTURED_TASK` prompt in Codex in a practical, production-oriented workflow.

## 1) Prepare your Codex run context

1. Open the target repository in Codex.
2. Ensure Python 3.10+ is active.
3. Confirm dependency and test tooling are available (`pytest`, `aiohttp`, `beautifulsoup4` or `lxml`).
4. Create or switch to a feature branch before any edits.

## 2) Start Codex with a two-part instruction style

Use:
- **System/developer constraints** for governance (commit behavior, testing expectations, output format).
- **User prompt** (your XML task) for architecture and implementation requirements.

Practical tip: keep your XML prompt unchanged and add a short preface such as:
- "Implement this end-to-end in the current repository."
- "Produce code, tests, docs, then run tests."
- "Commit all changes and prepare a PR message."

## 3) Convert the XML prompt into an execution checklist

Before coding, ask Codex to restate your XML as a build checklist:

1. Core async crawling engine (`aiohttp` + `asyncio`)
2. Domain-level rate limiting
3. Retry policy with status-aware rules (`429/5xx` retry, `400/403` no retry)
4. Pluggable proxy provider interface
5. Parser strategy layer (BeautifulSoup/lxml)
6. Change detection via content fingerprint/hash
7. Storage abstraction + SQLite default + optional Postgres adapter
8. Daily delta report output (CSV + JSON)
9. Structured JSON logging
10. Idempotent incremental crawling
11. Unit tests for parser and diff logic
12. Architecture documentation

This checklist keeps Codex aligned and prevents missing mandatory constraints.

## 4) Ask Codex to scaffold the exact project structure first

Request the following directories and modules before implementing logic:

- `src/price_intel/core/` (`crawler.py`, `scheduler.py`, `rate_limiter.py`, `retry_policy.py`)
- `src/price_intel/parsers/` (`base.py`, `site_x.py`, registry)
- `src/price_intel/storage/` (`repository.py`, `sqlite_adapter.py`, `postgres_adapter.py`)
- `src/price_intel/reporting/` (`delta_calculator.py`, `csv_exporter.py`, `json_exporter.py`)
- `src/price_intel/infra/` (`proxy_provider.py`, `logging_config.py`)
- `tests/` (`test_parsers.py`, `test_change_detection.py`, retry/rate-limit tests)

This "scaffold-first" step reduces refactors and keeps layered architecture clean.

## 5) Enforce implementation order (important)

Tell Codex to implement in this order:

1. **Domain models and protocols** (typed entities, repository interface, parser interface)
2. **Core execution path** (fetch → parse → validate → hash/diff → persist)
3. **Cross-cutting controls** (rate limiting, retries, timeout guards, structured logging)
4. **Reporting** (daily deltas in CSV/JSON)
5. **Tests**
6. **Architecture documentation**

Why this order: correctness and invariants come before optimization.

## 6) Force explicit invariants in code

Ask Codex to encode these as checks/assertive guards:

- No write if parse validation fails.
- Crawl runs are idempotent (unique keys/upsert + run/date scoping).
- Rate limits are enforced per domain.

Also ask for clear type hints across all public methods.

## 7) Specify robust async/network behavior

Instruct Codex to include:

- Shared `aiohttp.ClientSession` per crawl run.
- Bounded concurrency using semaphores.
- Token bucket or equivalent limiter for per-domain throughput.
- Exponential backoff with jitter.
- Status-aware retry classifier.
- Configurable request timeout and max retry attempts.

## 8) Require safe storage semantics

Direct Codex to implement deterministic writes:

- Repository contract (`save_snapshot`, `get_latest_snapshot`, `save_price_event`, etc.).
- SQLite adapter with transactions and conflict handling.
- Optional Postgres adapter behind same interface.
- Idempotency keys (e.g., `(site, product_id, observed_at_day, fingerprint)`).

## 9) Require observability from day one

Ask Codex for JSON logs including fields like:

- `run_id`
- `site`
- `url`
- `attempt`
- `status_code`
- `latency_ms`
- `retry_decision`

This drastically reduces debugging time in production.

## 10) Add red-team gate as a required validation step

Tell Codex to generate and run a "failure mode review" section after coding:

1. Risk of rate-limit bans from misconfigured limits
2. False positives in change detection
3. DB corruption/locking under concurrent writes

If any are unresolved, Codex must revise concurrency/retry/storage before finalizing.

## 11) Testing commands you should require

At minimum request:

- `pytest -q`
- Focused tests for parsers and fingerprint diffing
- Optional stress-style async test for limiter/retry interplay

If test dependencies are missing, instruct Codex to document exactly what is missing and why.

## 12) Documentation deliverables

Require two artifacts:

1. **Architecture document** covering:
   - Problem and scope
   - Layered architecture
   - Event-driven async paradigm
   - Library choices and trade-offs
   - Performance and scaling limits
   - Security mitigations
2. **Inline code comments** for async flow, backpressure, and retry logic.

## 13) Example "controller prompt" to give Codex

You can prepend this before your XML block:

> Implement this task end-to-end in this repository as production-grade code. First produce a concise plan, then scaffold modules, then implement core async crawling with per-domain rate limiting and status-aware retry policy, then storage adapters, reporting, tests, and architecture docs. Enforce all invariants in code. Run `pytest -q`, fix failures, and summarize outputs. Finally commit changes and generate a PR title/body.

## 14) Quality checklist before accepting output

Use this quick gate:

- [ ] Uses `aiohttp` + `asyncio`
- [ ] Rate limiter present and domain-aware
- [ ] Retry rules follow `429/5xx` vs `400/403`
- [ ] Hash-based change detection exists
- [ ] SQLite default + optional Postgres adapter
- [ ] CSV and JSON daily delta reporting
- [ ] JSON structured logs
- [ ] Idempotent persistence strategy
- [ ] Parser + change detection tests in pytest
- [ ] Architecture doc included

## 15) Common pitfalls to explicitly warn Codex about

- Unbounded task creation causing event-loop saturation.
- Recreating HTTP sessions per request.
- Writing raw parsed data without validation.
- Missing unique constraints that break idempotency.
- Treating all HTTP errors as retryable.
- Ignoring SQLite lock behavior under concurrent writes.

---

If you follow this flow, your prompt becomes an actionable implementation pipeline rather than a high-level specification.
