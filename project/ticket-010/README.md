# Ticket 010: Verify compiled package initializers and standalone binary imports

- **ID**: ticket-010
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues "kontynuuj,scalaj,tetsuj". Planfile PLF-012. Previous ticket009 independently merged bf83dc5a5da2eae33d3c7a666679e8dd3a5223d9; clean primary/no open PR/released lease and removed checkout observed. Baseline receipt:sorust.package-init-baseline.bf83dc5 confirms existing compiled __init__ with relative import/package path works; no runtime defect claimed. Add durable sdist/wheel and native-only exported root+nested initializer interop coverage and standardv14. Backend/runtime/Rust/ABI/dependencies/platforms unchanged; no release/deployment/consumer migration or protected-policy changes.

## Acceptance criteria

- AC-01: Real compiled root+nested initializers preserve relative imports, package paths and loaders; selected .py absent, unselected Python preserved in wheel, all hashes correct. Native-only exported package works in clean venv without Sorust/Cython/source .py and calls shared Rust C ABI.
- AC-02: Full pytest/Cargo/build/export and installed both-backend regression checks pass.
- AC-03: Canonical standardv14 and local/required remote gates, independent frozen-head approval/merge, owned lease release and preserved exact checkout cleanup/audit.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
