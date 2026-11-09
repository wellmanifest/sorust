# Ticket 001: Sorust dual native artifacts and reusable kernels

- **ID**: ticket-001
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-11-09

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user requests a new sorust Python library and standard producing Python .so modules and reusable atomic Rust binaries for Wellmanifest nl-* libraries. Workspace intake PLF-003. Source, tests and documentation; existing consumers keep separate ownership. Publication authorization was extended by the user on 2026-11-09: "kontynuuj, scalaj". Use independent protected validation and merge; no author bypass.

## Acceptance criteria

- AC-01: Build a platform wheel containing both native artifacts and a checksum manifest; rebuild the same source through its sdist.
- AC-02: Validate Python/Rust parity, C ABI reuse and rejection of missing, corrupt or incompatible artifacts.
- AC-03: Deliver an indexed canonical standard and consumer example, run local governance and report commit/PR/merge separately.

- AC-04: Publish through the declared independent route after a protected initial-ref publisher creates the empty remote main baseline. Current blocker: GOV-PUSH-001 and missing independent exact-plan grant.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
