# Changelog

## v1.0.2 — 2026-09-24

Developer-workspace maintenance release. No ENTITY Protocol 1.0 semantic changes.

- Fixes issue #6 by allowing recognized local Python virtual environments (`.venv` or `venv`) during normal kit validation and verification.
- Keeps a `--strict-worktree` mode for release/CI checks so packaged kit contents remain contamination-sensitive.
- Preserves all protocol specifications, schemas, vectors, pass criteria, and external interoperability status.
- Re-seals the maintenance release under the existing ENTITY release signer.

## v1.0.1 — 2026-09-17

Canonicalization release. No ENTITY Protocol 1.0 semantic changes.

- Declares this repository the authoritative sealed test target for new external qualification campaigns.
- Requires independent candidate implementations to live in their own repositories and pin a published kit release/tag.
- Re-seals all kit artifacts under the ENTITY release signer after canonicalization metadata changes.
- Preserves external non-BTG interoperability status as PENDING.

## v1.0.0 — 2026-09-17

Initial sealed ENTITY Protocol 1.0 External Conformance Kit.

- Clean-room rules and normative interoperability profile.
- Language-neutral canonicalization/cryptography specification.
- Public schemas and trust material.
- 26 frozen synthetic valid/invalid vectors.
- Generic black-box candidate runner.
- Live bidirectional interoperability procedure.
- Independent attestation/report templates.
- Internal prerequisite evidence reduced to public-safe statuses/hashes.

External non-BTG implementation/interoperability status remains PENDING.
