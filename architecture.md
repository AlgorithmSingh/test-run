# Architecture

This project follows a layered architecture. Each layer has a defined dependency direction; crossing it is a defect.

## Layers

- `src/domain/` — pure business logic. Defines entities, value objects, and the interfaces it needs from the outside world. Must not depend on any other layer.
- `src/infra/` — concrete I/O: database, HTTP, filesystem. May depend on `domain/` (to implement domain-defined interfaces).
- `src/app/` — composition root and application services. May depend on both `domain/` and `infra/`.

## Rule (dependency-cruiser-compatible)

```
src/domain/ must not import from src/infra/.
src/domain/ must not import from src/app/.
src/infra/ must not import from src/app/.
```

Violations of these rules are blockers. A domain module that imports from `infra/` is reaching across a boundary the domain layer is supposed to be ignorant of.

## ADR pointer

Significant architectural decisions live under `docs/adr/`. A new top-level directory or a new cross-cutting concern (auth, logging strategy, error spine) requires an ADR entry before the change lands.
