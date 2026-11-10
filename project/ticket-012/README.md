# Ticket 012: Include Cargo build scripts in source fingerprints

- **ID**: ticket-012
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues "kontynuuj,scalaj,tetsuj". Planfile PLF-014. Previous ticket011 independently merged ea3b05b39810b0add6b8d21e3fbd486d9432b96d; clean main, no active ticket/worktree or open PR observed. Baseline receipt:sorust.build-script-baseline.ea3b05b proves only build.rs changes native result/hash while source_sha256 stays identical. Include Cargo selected default/custom/parent-relative in-project build script once, honor build=false and require explicit build=true/path inputs. Reject missing/malformed/escaping/symlink inputs before compilers. No runtime/ABI/dependency/platform/release changes or complete dynamic-input provenance claim.

## Acceptance criteria

- AC-01: Real default/custom/shared script changes survive sdist and change both fingerprint and native result; absent/disabled behavior and early invalid-input rejection pass.
- AC-02: Full Python/Rust suites, final artifacts/export/installed smoke, canonical standard v16 with exact evidence and pinned own-document validation pass.
- AC-03: Local/required remote gates, independent frozen-head approval/merge, owner release and preserved checkout cleanup/audit.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
