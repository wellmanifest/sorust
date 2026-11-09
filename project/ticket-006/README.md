# Ticket 006: Export verified native binary bundles for reuse

- **ID**: ticket-006
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-09

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user repeats "kontynuuj, scalaj, testuj", continuing the original standalone binary reuse goal. Planfile PLF-008. Previous ticket-005 is independently merged at 37c7389400d26ec504e4156a381e6c8dda2c47bf, lease released and owned worktree removed. Add zero-dependency API/CLI export of already-built manifest-listed Python extensions, Rust cdylib and headers, with source verification and exclusive fresh output. Keep runtime counting, backend compilation, ABI, dependencies and supported platforms unchanged. Optional rlib remains a Cargo output outside wheel/export. No registry publication, deployment or consumer migration.

## Acceptance criteria

- AC-01: Installed API and CLI export verified exact native/header bytes and manifest to a new directory; independent Python and C clients execute exports. Existing destinations and invalid source inputs fail with preservation of user data.
- AC-02: Full pytest/Cargo pass, including generic foreign and nested consumer export.
- AC-03: Update indexed canonical standard v9, pass local/required remote gates and independent frozen-head review/merge; preserve generated data before removing only owned released worktree.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
