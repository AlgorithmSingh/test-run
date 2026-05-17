# Acceptance Checklist Schema (v3)

Canonical schema for `.orchestrator/acceptance/issue-{N}.yml`. The orchestrator's gate evaluator (spec §6) reads each file in this format inside a fresh clone of the pushed branch. Non-conforming files are rejected (gate FAIL with synthetic defect).

## Top-level

```yaml
version: 3
issue: <int>                       # GitHub issue number (must match filename)
render_touching: false             # set true if this change affects render code
criteria:
  - <criterion>
  - <criterion>
```

## Criteria

Every criterion MUST be exactly one of five `kind`s. Anything else is rejected as non-machine-checkable.

Every criterion may declare `requires: [<binary>, ...]` listing PATH binaries needed on the verification host. Missing → criterion `ENV_BLOCKED` (counted separately from code failures; does NOT consume a fix attempt).

### `kind: file`

```yaml
- id: <slug>
  kind: file
  path: "<repo-relative path>"
  assert: exists | absent | sha256:<hex>
  requires: []
```

### `kind: command`

```yaml
- id: <slug>
  kind: command
  run: "<shell command>"
  expect_exit: <int>
  requires: [<host-binary>, ...]
```

### `kind: artifact_hash`

```yaml
- id: <slug>
  kind: artifact_hash
  path: "<repo-relative path to produced artifact>"
  sha256: "<hex sha256>"
  requires: []
```

### `kind: artifact_oracle`

For render-touching changes. Renders a fixture, then compares to a committed golden.

```yaml
- id: <slug>
  kind: artifact_oracle
  render: "<shell command that produces the artifact>"
  produces: "<repo-relative path to produced artifact>"
  oracle: frame_hashes | file_sha256
  golden: ".orchestrator/golden/issue-<N>/<name>"
  tolerance: 0                      # 0 = exact; >0 = max mismatched frames
  requires: [chromium, ffmpeg]      # whatever the render needs
```

Golden artifacts under `.orchestrator/golden/**` are PROTECTED — agents may not create or modify them. If no golden exists for a render-touching change, the agent must stop and a human provides the golden.

### `kind: harness_job`

A named local script run by the harness backend.

```yaml
- id: <slug>
  kind: harness_job
  job: "<job name>"                 # script at .orchestrator/harness/<job>.sh
  requires: []
```

## What makes auto-merge safe (orchestrator-enforced)

- Every file MUST have ≥1 executed criterion (`command`, `artifact_oracle`, or `harness_job`). File-existence-only is too weak.
- Render-touching changes (either `render_touching: true` or PR diff touching `harness.render_paths`) MUST contain ≥1 `artifact_oracle` with an existing committed golden, otherwise → FAIL.
- The PR diff may NOT modify anything under `.orchestrator/golden/**`, `.orchestrator/sequence.yml`, `.orchestrator/config.yml`, `.orchestrator/acceptance/SCHEMA.md`, or `.orchestrator/harness/**` (protected paths).
- Loosening across attempts (removed criteria, raised tolerance, repointed golden, downgraded kind, dropped requires, relaxed expect_exit) is rejected.
