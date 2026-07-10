# ADR-001: Use Architectural Decision Records

## Status

Accepted

## Context

As this project evolves, design decisions accumulate in commit messages and conversations but are hard to find later. New contributors (or future-me) need to understand why choices were made, not just what was built.

## Decision

Record significant architectural decisions in `docs/adr/` using a lightweight format (Status, Context, Decision, Consequences). Each ADR is numbered sequentially and immutable once accepted — superseded decisions get a new ADR rather than editing the old one.

## Consequences

- Decisions are discoverable and searchable in the repo
- The "why" behind choices is preserved alongside the code
- Slightly more overhead when making decisions (writing the ADR), offset by less time re-litigating past choices
