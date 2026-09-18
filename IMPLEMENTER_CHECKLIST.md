# Independent Implementer Checklist

Before coding:
- [ ] Read `README_FIRST.md`.
- [ ] Sign/record clean-room attestation intent.
- [ ] Record exact kit Git tag/commit/hash.
- [ ] Do not inspect/copy BTG ENTITY source implementation.

Phase one:
- [ ] Implement canonical JSON.
- [ ] Implement Ed25519/base64url/SHA-256 verification.
- [ ] Implement manifest verification.
- [ ] Implement signature-record verification.
- [ ] Implement principal/device/installation/application binding verification.
- [ ] Implement asset/event semantics.
- [ ] Implement lineage semantics.
- [ ] Implement node authorization/revocation.
- [ ] Implement service/domain resolution semantics.
- [ ] Implement sovereign-export verification.
- [ ] Implement the candidate CLI.
- [ ] Pass all 26 vectors.

Phase two:
- [ ] Independent → BTG live interop.
- [ ] BTG → Independent live interop.
- [ ] Negative principal-binding agreement.
- [ ] Provenance/lineage agreement.
- [ ] Sovereign export verified without originating BTG runtime.

Evidence:
- [ ] Publish/hash exact source commit.
- [ ] Hash build artifact.
- [ ] Complete independent attestation.
- [ ] Complete external conformance report.
- [ ] Sign external report/declaration.
