# Ticket 011: Prepare verified native scalar counters for repeated calls

- **ID**: ticket-011
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues "kontynuuj,scalaj,tetsuj". Planfile PLF-013. Previous ticket010 independently merged04e38d529532538ee9adbeb38b509bf95fc052e5, clean main/no active checkout or open PR/released lease observed. Baseline receipt:sorust.compiled-call-baseline.04e38d5 measured64B public compiled-python1.861ms vs verified bound native0.378us over7 warmed series. Add explicit prepared callable with artifact audit at preparation, safe byte normalization, bound entry/library lifetime and per-call owned Rust output. Prepared calls do not audit filesystem; explicit verify/new preparation audits drift. Existing APIs/checks unchanged; process loader caches are not hot reload. No dependencies/Rust/ABI/platform changes, registry release/deployment/consumer migration or real-workload speed claim.

## Acceptance criteria

- AC-01: Safe eager preparation and entry errors, bound lookup/normalization/plain-bytes identity/CDLL lifetime/FFI status, installed both-backend randomized/subclass/empty/threaded parity and explicit prepared-header-drift vs fresh-audit semantics pass.
- AC-02: Same-wheel compiled64B prepared median >=20x existing public scalar over7 warmed series; constructor cost separate, correctness/environment/hash/method limits recorded. Full pytest/Cargo/build/export/installed regressions pass.
- AC-03: Canonical standardv15, local/required remote gates and independent frozen-head approval/merge; owner release and preserved exact owned checkout cleanup/audit.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
