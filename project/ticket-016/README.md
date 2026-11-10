# Ticket 016: Verify offline isolated prebuilt Rust adoption

- **ID**: ticket-016
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues "kontynuuj" under existing Sorust reuse/test/protected merge task. PLF-018; prior ticket015 complete, clean main78c0f69, released lease/no open PR. Baseline receipt:sorust.isolation-baseline.78c0f69 observes only prepared --no-isolation pilot. Extend bounded developer pilot with local wheelhouse snapshot and clean frontend, actual offline isolated PEP517 dependencies, existing Rust fail stubs, provenance and guard tests. No runtime/backend/kernel/ABI/dependency/platform changes, downloads, consumer source migration, speed guarantee, registry release/deploy.

## Acceptance criteria

- AC-01: Snapshot/SDK/input guards and no ambient dependency fallback tests pass.
- AC-02: Full suites, actual pinned NL isolated sdist/wheel with no Rust calls and24original conformance executions; missing local Cython fails, canonicalv20 and artifact identity checks pass.
- AC-03: Local/remote gates, independent frozen-head merge, postmerge install/smoke, lease release and preserved exact owned-checkout cleanup.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
