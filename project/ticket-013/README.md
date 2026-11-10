# Ticket 013: Reproduce native reuse on pinned NL DSL consumer code

- **ID**: ticket-013
- **Owner**: unresolved:human
- **Status**: IN_PROGRESS
- **Workflow state**: PUBLICATION
- **Created**: 2026-11-10

## Goal and scope

SESSION_EXECUTION_AUTHORIZATION: user says "kontynuuj,scalaj,reuzywaj, badaj jak dziala w praktyce". Planfile PLF-015. Prior ticket012 independently merged16e802b; clean main/no active ticket or open PR observed. Baseline receipt:sorust.nl-dsl-build-baseline.16e802b builds unmodified standard/nl_dsl_llm.py from consumer aa47c8752f1ea446208f6dfb7a018ad02e92250a as .so in44.52s. Deliver a repeatable Sorust developer pilot: source/install/export comparison, actual pinned conformance functions, minimal runtime, explicit consumer resource sidecar, same prebuilt Rust .so in all modes and independent .rlib client, timing/profile/Unicode semantic boundary evidence. Consumer source remains read-only; no runtime/ABI/dependency changes, migration, external effects, production claim or broader cross-repository architecture report.

## Acceptance criteria

- AC-01: Input pin/confinement/parity guards and practical unchanged-source sdist/wheel/source/native/export tests, resource boundary and prebuilt Rust binary reuse pass.
- AC-02: Full Python/Rust tests, final artifacts and installed smoke;7-series measured timings/profile/environment/hash evidence without a speed threshold; canonical standardv17 documents this Sorust tool.
- AC-03: Local/remote gates and independent frozen-head approval/merge, verified postmerge install, released ownership and preserved cleanup/audit.

Canonical result: [Sorust binary standard](../../docs/information/sorust-binary-standard.md).
