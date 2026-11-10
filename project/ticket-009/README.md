# Ticket 009: Prevent stale binaries in repeated consumer wheel builds

- **ID**: ticket-009
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues "kontynuuj,scalaj,tetsuj". Planfile PLF-011. Previous ticket008 is independently merged b10294160915d5507e8a50ace6a78f2a9db7feeb with clean primary, no open PR, released lease and removed worktree. Baseline receipt:sorust.rebuild-baseline.b102941 proves a second consumer wheel retains unlisted legacy.so after changing selection legacy->fresh, and installed import gives old10 rather than current11. Build each wheel in fresh owned build_lib staging; preserve compiler caches and existing outputs. Final hook option probe revealed --skip-build emitted an empty successful wheel; reject that option explicitly and validate no wheel is emitted. Runtime/Rust/ABI/dependencies/platforms remain unchanged. No registry release, deployment, consumer migration or protected-policy changes.

## Acceptance criteria

- AC-01: Repeated same-tree wheel builds package exactly current compiled modules; former compiled module uses current Python when retained and cannot import when removed. Actual installed behavior and manifest hashes verified for both cases.
- AC-02: Full pytest/Cargo/build and installed scalar/many/stream/native export regressions pass.
- AC-03: Canonical standardv13, required local/remote gates and independent frozen-head approval/merge; preserve generated data and release/remove only owned merged worktree.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
