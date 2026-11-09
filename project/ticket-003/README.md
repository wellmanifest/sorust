# Ticket 003: Bind FFI lengths and parity to actual bytes buffers

- **ID**: ticket-003
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-09

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: repeated user request "kontynuuj, scalaj, testuj" authorizes this bounded Sorust correction, tests, PR and independent merge. Planfile PLF-005. Base f6b9829 forwards1024 for an actual7-byte buffer when a bytes subclass overrides __len__; a capture stub proved it without executing native code with the invalid size. Ordinary subclasses also differ across Rust/compiled-Python. Primary receipt: bytes-buffer-reproduction.json. Previous ticket-002 is merged and its lease released.

## Acceptance criteria

- AC-01: Use actual immutable buffer bytes for subclasses, preserve ordinary bytes identity, ignore misleading length/iteration/bytes hooks, and prove backend/reference parity. Oversized-length tests use a stub; no invalid native memory access.
- AC-02: Full build/install/integrity/ABI and C/Rust/Python consumer tests pass without C ABI or Rust algorithm changes.
- AC-03: Update indexed canonical standard, pass local and required remote checks, independently approve/merge frozen HEAD and clean up only owned released worktree.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
