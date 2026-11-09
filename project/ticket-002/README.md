# Ticket 002: Bind compiled Python import to verified artifacts

- **ID**: ticket-002
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-09

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: repeated user request "kontynuuj, scalaj, testuj" authorizes the bounded Sorust correction, tests, PR and independent protected merge. Owner request PLF-004. On merged base4d3d972, a valid manifest can hash listed_copy.so while the runtime imports the unlisted _compat extension and returns2. Exact reproduction is retained in the ignored primary receipt compiled-artifact-binding-reproduction.json. Original ticket-001 is already independently merged and its lease remains released.

## Acceptance criteria

- AC-01: The selected compiled extension must correspond to a verified manifest entry before import; reject unlisted, missing, source fallback and preloaded-unlisted cases, including absence of source execution side effects.
- AC-02: Full wheel/sdist, installed-wheel parity, ABI/integrity and C/Rust/Python consumer tests pass; no native API or semantic changes.
- AC-03: Update the indexed canonical standard, pass native governance, and independently approve/merge the frozen exact head. No author approval or direct merge.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
