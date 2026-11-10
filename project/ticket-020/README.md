# Ticket 020: Export pinned installed Rust components through API and CLI

- **ID**: ticket-020
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues original Sorust reuse/test/protected merge after completed PLF-021. PLF-022. Add public API and CLI for installed native-only component export by distribution/version/package/raw manifest pin/library identity. Reuse existing metadata/payload snapshot validator and share export writer; no donor import/native loading/build dependencies at export. Preserve old explicit-path export and exact new raw manifest bytes. No backend/algorithm/ABI/schema/runtime dependency/platform changes, consumer migration, download, performance claim, registry release/deploy.

## Acceptance criteria

- AC-01: Native component identity/pin/ownership/snapshot/races/links validated; exact raw metadata and payload exported without import or native loading; invalid input/existing output preserved; legacy export/backend tests pass.
- AC-02: Full suites, actual fresh no-toolchain/no-build-dependency API/CLI exports, C ABI reuse/old-reader/final artifacts/reused NL8 pass; indexed canonicalv24 and pinned Docs checked.
- AC-03: Local/remote gates, independent frozen-head approval/merge, postmerge smoke, owner release and preserved exact cleanup.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
