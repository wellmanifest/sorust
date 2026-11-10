# Ticket 015: Build consumers from pinned installed Rust components

- **ID**: ticket-015
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues "kontynuuj" under existing test/reuse/protected-merge task. PLF-017. Prior ticket014 independently merged e78ce82 with clean main/no active ticket or open PR. Baseline receipt:sorust.prebuilt-baseline.e78ce82 records unsupported installed-component configuration and existing Cargo build branch. Add pinned installed build-dependency mode through metadata, owned verified snapshots and same-platform/data-free component contract, retaining source mode. New consumer wheels bundle existing Rust/header bytes and record provenance; source sdists carry only consumer files/pins. Test with Cargo/rustc fail stubs and unchanged actual NL source. No runtime/kernel/ABI/platform/dependency changes, automatic dependency installation, donor code import, consumer migration, process-wide deduplication, speed guarantee or release/deploy.

## Acceptance criteria

- AC-01: Strict descriptor/payload ownership/integrity/platform validation and no donor execution, snapshot/source fingerprint checks, real source-only sdist/wheel with Rust tools blocked, matching installed/exported payloads pass.
- AC-02: Full Python/Rust and final build/artifact smoke; actual NL source/wheel/export parity and24original conformance executions with prebuilt component/no build-time Cargo/rustc; canonicalv19.
- AC-03: Local/required remote checks and independent frozen-head approval/merge; postmerge installation, owner release and preserved exact checkout cleanup/audit.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
