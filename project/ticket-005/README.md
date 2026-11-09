# Ticket 005: Cover multi-module native consumer distributions

- **ID**: ticket-005
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-09

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user repeats "kontynuuj, scalaj, testuj". Planfile PLF-007. Previous ticket-004 is independently merged at 23e6adcf2ed09803b552ad229bc0dc87cf2409eb with released lease. Controlled isolated PEP517 offline-wheelhouse canary passed for two Python extensions (one nested), source selection, hashes, runtime without build tools/Sorust and installed C consumer. Primary receipt: isolated-adoption-check.json. Add durable real integration coverage, without claiming a runtime defect or changing implementation, ABI, dependencies or platforms.

## Acceptance criteria

- AC-01: Existing foreign-consumer integration test covers single and nested two-module layouts through actual sdist-to-wheel/install, selective source exclusion, all native/header hashes, installed extension functions and foreign Rust ABI.
- AC-02: Full pytest and native Cargo suites pass unchanged.
- AC-03: Update existing indexed canonical standard, pass local/required remote checks and independent frozen-head review/merge, then preserve generated data and remove only owned released merged worktree.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
