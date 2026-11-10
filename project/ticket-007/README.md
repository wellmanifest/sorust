# Ticket 007: Amortize FFI overhead with batched token counting

- **ID**: ticket-007
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues "kontynuuj" under the original optimized shared-binary goal; earlier test/merge authorization persists. Planfile PLF-009. Previous ticket-006 is independently merged at069cf837755284b0a622ec25cc3b9a36bebe5dfd with released lease. Baseline receipt batch-baseline.json: 256x3B Rust-scalar290.425us vs reference74.633us; 256x64B Rust345.739us. Nine warmed repeats, no CPU affinity; controlled microbenchmark, not nl-* workload evidence. Add one-call batch ABI/API with immutable joined input and checked lengths, reference/compiled parity and source-bound benchmark. Scalar semantics and ABI1 baseline stay compatible. No dependencies, registry release, platform expansion or consumer migration.

## Acceptance criteria

- AC-01: Many-buffer results match reference/compiled/scalar across binary and subclass inputs; invalid ABI parameters/overflow cannot partially write output; native integrity failures remain explicit; legacy scalar ABI1 remains usable.
- AC-02: >=2x warmed median speedup for256x64B vs same-wheel scalar Rust, with other sizes/copy cost/limits recorded; full pytest/Cargo/build/export/C/Rust/Python regressions pass.
- AC-03: Canonical standardv10, required exact-head gates and independent frozen-head approval/merge; preserve generated data before removing only owned released merged worktree.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
