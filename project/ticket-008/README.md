# Ticket 008: Bound batch memory with streaming token counts

- **ID**: ticket-008
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user repeats "kontynuuj, scalaj, tetsuj". Planfile PLF-010. Previous ticket-007 is independently merged ef788e90d9dce61c559418416b8d49c4a8b6ca66 with released lease and clean primary. Controlled installed baseline stream-baseline.json measured32.473MiB Python allocation peak for4096 unique4096B buffers across3 warm-kernel tracemalloc runs. Add lazy bounded batching over existing native many API, preserving order, explicit failure and caller source ownership. Rust/ABI/scalar/many behavior remains unchanged. No dependencies, registry release, deployment, platform expansion or consumer migration.

## Acceptance criteria

- AC-01: Stream construction does not touch source; bounded batches preserve order/backpressure, errors and source ownership, with eager argument checks and native capability required even for empty source. Installed Rust and compiled-python parity passes.
- AC-02: At batch256, median traced Python allocation peak <=10% of eager many for4096 unique4096B buffers, equal checksum and method/limits recorded; full pytest/Cargo/build/export regressions pass.
- AC-03: Canonical standardv11, local/required remote checks and independent frozen-head approval/merge; preserve generated data before removing only owned released merged worktree.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
