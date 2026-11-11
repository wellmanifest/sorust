# Ticket 022: Prepare shared native batch counters for repeated FFI calls

- **ID**: ticket-022
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-11-11

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues original Sorust atomic reuse/test/protected merge after completed PLF-023. PLF-024. Add prepared batch counter for SDK/compiled-python/pinned installed native component, reuse selection/audit/packing/status logic and existing scalar handle. Each preparation audits; hot batch calls use one FFI and no file/metadata reads. Preserve old APIs, byte and capability ordering. Actual no-toolchain shared donor proof plus paired warmed scalar-loop/batch timings on fixed data. No algorithm/ABI/schema/dependency/platform/consumer migration, streaming expansion, hot reload/global deduplication, speed guarantee, registry release/deploy.

## Acceptance criteria

- AC-01: Invalid inputs/selectors/capabilities/status fail; buffers/generators/empty outputs and compiled mode match old behavior; one batch FFI and library lifetime/audit-before-cache verified.
- AC-02: Full suites, actual shared installed scalar/batch clients with no export/build deps/tools, threaded parity/no hot reads and paired method-bound timings pass; final artifacts/reused NL8 and indexed canonicalv26/pinned Docs checked.
- AC-03: Exact-head gates/independent review and merge, postmerge smoke, owner release and preserved exact cleanup.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
