# Ticket 021: Prepare counters from pinned installed Rust components

- **ID**: ticket-021
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-11

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues original Sorust atomic binary reuse/test/protected merge after completed PLF-022. PLF-023. Prepare existing scalar counter directly from a pinned installed Rust-only component, using shared metadata/snapshot validation and C ABI binder. Audit each preparation; bounded native binding cache uses absolute path/payload hash, existing callable retains library. No donor import/export/copy/build. Preserve defaults and fingerprints; private root only. No algorithm/ABI/schema/dependency/platform change, consumer migration, hot reload, speed guarantee, registry release/deploy.

## Acceptance criteria

- AC-01: Invalid selection/descriptor/ownership/paths/drift/ABI/symbol rejected; bytes and lifetime/defaults retained; old/new backend fingerprints match.
- AC-02: Full suites and actual fresh-runtime clients share installed donor path/handle/mapping with no export/build tools/deps; final artifacts/reused NL8 and indexed canonicalv25/pinned Docs verified.
- AC-03: Exact-head gates/independent review and merge, postmerge smoke, owner release and preserved exact cleanup.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
