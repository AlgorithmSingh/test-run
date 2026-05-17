# Acceptance Checklist Schema

Canonical schema for `.orchestrator/acceptance/issue-{N}.yml`. The orchestrator's gate evaluator (`13-orchestrator/spec.md` §6) reads each file in this format. Files that do not conform are rejected (gate result FAIL with defect `non-machine-checkable criterion` or `missing/invalid acceptance file`).

## Top-level

```yaml
version: 1
issue: <int>                       # GitHub issue number (must match filename)
independence: cloud | single-model # set by orchestrator, not by agents
criteria:
  - <criterion>
  - <criterion>
```

## Criteria

Every criterion MUST be one of four `kind`s. Anything else is rejected as non-machine-checkable.

### `kind: command`

```yaml
- id: <slug>
  kind: command
  run: "<shell command>"
  expect_exit: <int>
  requires: [<host-binary>, ...]   # optional; empty list means no host deps
```

### `kind: file`

```yaml
- id: <slug>
  kind: file
  path: "<repo-relative path>"
  assert: exists | absent | sha256:<hex>
  requires: []
```

### `kind: ci_job`

```yaml
- id: <slug>
  kind: ci_job
  job: "<exact CI job name>"
  requires: []
```

The job's `conclusion` is read from the GitHub checks API for the PR head SHA. Conclusion `success` = PASS.

### `kind: artifact_hash`

```yaml
- id: <slug>
  kind: artifact_hash
  path: "<repo-relative path>"
  sha256: "<hex>"
  requires: []
```

## Hard rules (enforced by the orchestrator)

1. Every criterion MUST be one of the four kinds above. "Agent confirms X", "looks correct", "presentation quality" are rejected.
2. `id` is a stable slug; the orchestrator hashes criteria by `id` across attempts.
3. **No loosening across fix attempts.** Removing a criterion, relaxing `expect_exit`, deleting `requires` entries, or changing `assert`/`sha256` to a weaker form is rejected. The id-set MUST be monotone across attempts and per-id (`kind`, `run`, `expect_exit`, `path`, `assert`, `sha256`, `job`, `requires`) MUST be field-equal.
4. **Founder-lane stricter requirement (§6.4):** an issue routed to the founder lane MUST have ≥1 `kind: ci_job` criterion. Rationale: the only independent oracle on the founder lane is GitHub CI.
5. Acceptance files MUST live at `.orchestrator/acceptance/issue-{N}.yml`. Edits to this path by an agent fix-phase commit are diffed against the prior attempt and rejected if they loosen the gate.

## Out of scope

- Subjective criteria of any form.
- Criteria that depend on an agent's self-report or any LLM judgment.
- Criteria whose result requires human interpretation.
