# Ticket 018: Build standalone Rust wheels from Cargo sources

- **ID**: ticket-018
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues original Sorust binary reuse/test/protected merge task. PLF-020. Prior ticket017 complete, clean main5e96b66, no active ticket/openPR. Baseline receipt:sorust.rust-source-baseline.5e96b66 observes missing Rust-only source backend and dual config rejection. Add native source backend with shared Cargo/input/staging primitives, no Python/Cython payload, existing Rust manifest, strict source profile. Test producer source sdist/wheel and downstream Python dependency reuse; fresh Cython-absent builder. No kernel/ABI/dependency/platform changes, downloads, consumer migration, speed claim, registry release/deploy.

## Acceptance criteria

- AC-01: Strict source profile/shared-input compatibility, automatic source/script inclusion, actual Python-free wheel without Cython imports, metadata/export/C ABI and downstream Python build with Rust blocked pass.
- AC-02: Full suites, actual Cython-absent producer and final artifacts/installed source/provenance checks; canonicalv22/index/pinned Docs pass.
- AC-03: Local/remote checks, independent frozen-head approval/merge, postmerge smoke, current-owner release and preserved exact checkout cleanup.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
