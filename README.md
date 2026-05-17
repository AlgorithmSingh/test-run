# test-run

Test target for the agent orchestrator at `harness-engineering/13-orchestrator/`.

This repo exists only to exercise the orchestrator's loop end-to-end against a real GitHub repo: real branch protection, real labels, real PR merges, real CI. Issues are deliberately trivial — the orchestrator's correctness is the thing under test, not the agent's coding ability.

See `.orchestrator/` for the live sequence, config, and acceptance schema. See `13-orchestrator/spec.md` in the orchestrator repo for the design contract.
