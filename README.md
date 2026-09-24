# ENTITY Protocol 1.0 External Conformance Kit

[![Release](https://img.shields.io/github/v/release/blackmore-technology-group/ENTITY-Protocol-1.0-Conformance-Kit?sort=semver)](https://github.com/blackmore-technology-group/ENTITY-Protocol-1.0-Conformance-Kit/releases/latest)
[![Kit validation](https://github.com/blackmore-technology-group/ENTITY-Protocol-1.0-Conformance-Kit/actions/workflows/kit-validation.yml/badge.svg)](https://github.com/blackmore-technology-group/ENTITY-Protocol-1.0-Conformance-Kit/actions/workflows/kit-validation.yml)
[![License](https://img.shields.io/github/license/blackmore-technology-group/ENTITY-Protocol-1.0-Conformance-Kit)](LICENSE)

[ENTITY](https://github.com/blackmore-technology-group/ENTITY) | [Independent interoperability challenge](https://github.com/blackmore-technology-group/ENTITY/blob/main/docs/INTEROPERABILITY_CHALLENGE.md) | [v3.3 engineering discussion](https://github.com/blackmore-technology-group/ENTITY/discussions/34)

> **AUTHORITATIVE SEALED TEST TARGET**
>
> This repository is the canonical Blackmore Technology Group external-conformance target for new ENTITY Protocol 1.0 qualification campaigns. Independent candidate implementations MUST live in their own repositories and MUST use a specific published release/tag of this kit.

**Independent implementation target for ENTITY Protocol 1.0.**

This repository exists to answer one technical question:

> Given only the published protocol, schemas, profiles, trust material and test vectors, can an independent developer reproduce ENTITY Protocol 1.0 semantics and interoperate with the BTG reference implementation?

This repository intentionally contains **no ENTITY reference runtime, no BTG Python SDK implementation, no production databases and no private authority material**.

## Kit status

**ENTITY Protocol 1.0 External Conformance Kit v1.0.2 — AUTHORITATIVE SEALED EXTERNAL TEST TARGET**

Internal prerequisites used to open this external milestone:
- SearchAR Release Integrity v2: PASS.
- ENTITY signed distribution qualification: PASS.
- ENTITY Protocol 1.0: FROZEN_FOR_EXTERNAL_CONFORMANCE.
- External non-BTG implementation/interoperability: PENDING.

The fact that this kit exists is **not** itself an external interoperability PASS.

## Repository layout

    ENTITY-Protocol-1.0-Conformance-Kit/
    ├── README_FIRST.md
    ├── PROTOCOL_VERSION.json
    ├── protocol/
    ├── schemas/
    ├── profiles/
    ├── vectors/
    │   ├── valid/
    │   ├── invalid/
    │   └── VECTOR_MANIFEST.json
    ├── conformance/
    │   └── black_box_tests/
    ├── live_interop/
    ├── evidence/
    ├── trust/
    └── provenance/

## Recommended independent implementations

A different language from the BTG Python reference implementation is strongly preferred, for example Rust, Go, TypeScript, Java, C#, Swift or Kotlin. It is not an absolute conformance requirement, but it strengthens independence evidence.

## Verify the sealed kit

Before implementing anything:

    python -m pip install -r requirements-ci.txt
    python tools/validate_kit.py
    python tools/verify_kit.py

Both commands MUST report `valid: true`. A normal developer checkout may use a recognized local virtual environment at `.venv` or `venv`; those local environment files are excluded from the default workspace scan. Release/CI qualification uses `--strict-worktree`.

The independent implementation SHOULD live in its **own repository**. Do not add candidate implementation code to this sealed kit repository; this repository is the fixed public test target.

## Phase 1 — vectors

Implement the CLI contract in `conformance/IMPLEMENTATION_INTERFACE.md`, then run:

    python conformance/black_box_tests/run_conformance.py --candidate "<your executable and arguments>"

The runner contains no ENTITY validation logic. It only presents each public vector to your candidate and compares the candidate's declared accept/reject result to `vectors/VECTOR_MANIFEST.json`.

## Phase 2 — live interoperability

After vector conformance passes, follow `live_interop/PROCEDURE.md` for bidirectional BTG ↔ independent implementation testing.

## Independence evidence

The external party must complete its own evidence package using the templates under `evidence/`. BTG must not author the independent implementation's final qualification report.

## License

Apache License 2.0.
