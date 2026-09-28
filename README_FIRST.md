# Read This First — ENTITY Protocol 1.0 External Conformance Kit v1.0.2

This repository is the **authoritative sealed clean-room external conformance challenge** for new ENTITY Protocol 1.0 qualification campaigns. Use a published release/tag of this repository as the exact allowed test material.

Your task is **not** to install, wrap, call, port or inspect Blackmore Technology Group's ENTITY reference implementation. Your task is to implement the observable semantics of ENTITY Protocol 1.0 from the material in this repository alone.

## Minimum challenge

Your independent implementation MUST be able to:

1. Parse and validate a sovereign Entity manifest.
2. Verify ENTITY Ed25519 signatures.
3. Validate an `ent1-...` / `ent2-...` identity and distinguish aliases from authority.
4. Validate a signed Principal → Device → Installation → Application binding bundle.
5. Validate an Open SDK asset envelope.
6. Validate an Open SDK event envelope.
7. Preserve and interpret parent/derivation lineage.
8. Validate node authorization and revocation.
9. Validate an Entity service manifest.
10. Resolve or interpret an ENTITY Domain proof/snapshot.
11. Validate a sovereign domain export package.
12. Reject every supplied invalid/tampered vector.

Phase one is file/vector conformance. Phase two is live bidirectional interoperability with a BTG ENTITY node.

## Clean-room boundary

You MAY use only the files in this repository plus ordinary public cryptographic/JSON standards and libraries.

You MUST NOT use:
- the `blackmore-technology-group/ENTITY` source tree while implementing;
- BTG Python reference modules;
- BTG production state/databases;
- private release/signing keys;
- internal qualification implementations;
- NIKI, ADAM, BSIE, HuntAR, SearchAR or HikeAR code.

Questions about specification interpretation are allowed. Questions about how BTG Python classes implement behavior are outside the clean-room boundary.

Start with:
- `protocol/ENTITY_PROTOCOL_1_0_INTEROPERABILITY_PROFILE.md`
- `protocol/CANONICALIZATION_AND_CRYPTOGRAPHY.md`
- `profiles/CLEAN_ROOM_RULES.md`
- `conformance/IMPLEMENTATION_INTERFACE.md`
- `vectors/VECTOR_MANIFEST.json`
- `conformance/PASS_CRITERIA.md`
