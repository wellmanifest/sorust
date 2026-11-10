# Ticket 017: Consume standalone Rust-only binary components

- **ID**: ticket-017
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues original Sorust binary reuse/test/protected merge task. PLF-019. Prior ticket016 complete, clean main8de2464, no active ticket or openPR. Baseline receipt:sorust.native-component-baseline.8de2464 shows native-only verify/export rejected before output. Add strict explicit-dir Rust-only manifest and optional native-only wheel in isolated NL pilot, preserve default SDK dual-artifact contract and all legacy modes. No kernel/ABI/dependency/platform or production source-builder changes, downloads, consumer migration, speed guarantee, registry release/deploy.

## Acceptance criteria

- AC-01: Strict schema/default-SDK/compatibility/metadata/actual wheel install-export-C ABI tests pass; old readers reject new schema without output.
- AC-02: Full Python/Rust, actual pinned NL isolated build uses Python-free native wheel with24original conformance executions and exact payload/provenance; final artifacts and canonicalv21 pass.
- AC-03: Local/remote checks, independent frozen-head approval/merge, postmerge smoke, current-owner CAS release and preserved exact checkout cleanup.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
