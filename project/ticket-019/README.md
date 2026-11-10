# Ticket 019: Reproduce Cargo source component reuse on pinned NL code

- **ID**: ticket-019
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: EDIT
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user continues original Sorust reuse/test/protected merge task. PLF-021. Prior ticket018 complete via independent merge/terminal receipt, released lease and clean main. Add optional production source-Rust-component mode to the committed NL developer pilot. Use exact committed Cargo inputs, offline isolated source sdist/wheel without Cython, declared generated wheel in Rust-free NL consumer build. Preserve old modes and all inputs. No consumer source writes, runtime/ABI/schema/dependency/platform change, download, speed claim, registry release/deploy.

## Acceptance criteria

- AC-01: Invalid modes/unsafe inputs/stale native backend rejected; exact pinned sources and Cython-free producer snapshots, actual generated donor provenance and existing modes tested.
- AC-02: Full suites and actual isolated producer plus pinned NL consumer pass; 24 original conformance executions, byte provenance/export/C ABI/rlib verified; canonicalv23 indexed and pinned Docs checked.
- AC-03: Gates and independent frozen-head approval/merge, postmerge smoke, owner release and preserved exact cleanup.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
