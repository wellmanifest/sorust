# Ticket 004: Validate Cargo.lock as a regular project input

- **ID**: ticket-004
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-09

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: repeated user request "kontynuuj, scalaj, testuj" authorizes this bounded Sorust correction, tests, PR and independent merge. Planfile PLF-006. Base b0e9c9c accepts an external Cargo.lock symlink, and changing only that controlled external file changes source_sha256. Reproduction executes no Cargo/build script and uses private owned scratch data. Primary receipt: cargo-lock-path-reproduction.json. Previous ticket-003 is merged and its lease released.

## Acceptance criteria

- AC-01: Cargo.lock must pass regular-file/no-symlink/containment checks; both internal and external symlinks fail configuration and real PEP517 sdist before Cython source generation; preserve missing-lock diagnostic.
- AC-02: Regular-source builds and full runtime/ABI/integrity and C/Rust/Python consumer tests pass unchanged.
- AC-03: Update existing indexed standard, pass local/required remote checks and independent frozen-head approval/merge; clean up only owned released worktree.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
