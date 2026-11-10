# Ticket 014: Verify and export explicitly declared package resources

- **ID**: ticket-014
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues "ntynujcalaj,testuj". PLF-016. Prior ticket013/PLF015 independently merged55bb710 with clean main/no active ticket/open PR. Actual copied NL wheel baseline receipt:sorust.resource-baseline.55bb710 proves only JSON whitespace drift changes its hash while v1 audit remains unchanged and export omits the file. Implement optional explicit resources, safe package-relative regular inputs, automatic sdist/wheel inclusion and source hashing, resource-aware manifestv2 verification/export with legacyv1 support and old-reader refusal. Reuse actual pinned NL pilot to prove complete standalone export without manual resource copy. No kernel/ABI/dependency/platform change, consumer migration, arbitrary file discovery, publisher authenticity, timing guarantee or release/deploy.

## Acceptance criteria

- AC-01: Configuration and manifest safety, v1/v2 compatibility, resource drift/snapshot errors and real sdist/wheel/rebuild/export/minimal runtime integration pass.
- AC-02: Full Python/Rust suites, final artifacts/install/export; actual pinned NL source/wheel/export parity and8original conformance functions per mode, declared resource drift rejection and no manual copy; canonicalv18.
- AC-03: Local/required remote gates, protected independent exact-head approval/merge; verified postmerge installation, owner release and preserved owned checkout cleanup/audit.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
