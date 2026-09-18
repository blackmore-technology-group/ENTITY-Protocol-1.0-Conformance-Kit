# ENTITY Protocol 1.0 — External Conformance Specification

**Status:** FROZEN_FOR_EXTERNAL_CONFORMANCE
**Conformance Kit:** v1.0

This document is the normative entry point for the first clean-room external interoperability profile of ENTITY Protocol 1.0.

## Normative set

Conformance is determined by this document together with:
1. `ENTITY_PROTOCOL_1_0_FREEZE.json`
2. `ENTITY_PROTOCOL_GOVERNANCE_v1.md`
3. `CANONICALIZATION_AND_CRYPTOGRAPHY.md`
4. `ENTITY_PROTOCOL_1_0_INTEROPERABILITY_PROFILE.md`
5. `ENTITY_DOMAIN_PROTOCOLS_v1.md`
6. schemas under `../schemas/`
7. fixed valid/invalid vectors under `../vectors/`
8. public clarifications/errata recorded in `ERRATA.md`.

## Interpretation precedence

If materials appear to conflict:
1. a published protocol erratum for this kit version controls;
2. explicit normative rules in the protocol/profile control;
3. JSON schemas control structural requirements;
4. valid/invalid vectors resolve tested observable behavior;
5. prose examples are explanatory and do not override the above.

An ambiguity that cannot be resolved from this order MUST be raised publicly before being used for a qualification PASS.

## Core sovereignty invariants

- infrastructure possession is not sovereign authority;
- registration is not ownership;
- provenance is not factual/legal truth;
- aliases are not cryptographic authority;
- device possession is not the Entity;
- generic application events cannot manufacture consent, rights, licence, settlement, payment, capital or Digital Commodity state;
- historical signed records remain historical evidence but do not automatically regain current authority;
- provider replacement must not silently replace the Entity root.

## Phase-one scope

The independent implementation verifies the object families, cryptographic bindings and semantic outcomes required by `ENTITY_PROTOCOL_1_0_INTEROPERABILITY_PROFILE.md` and the 26 frozen vectors.

## Phase-two scope

Full external interoperability additionally requires bidirectional live communication and sovereign-export survival under `../live_interop/PROCEDURE.md`.

## Non-claim

Publication of this kit does not mean external interoperability has passed. The milestone remains PENDING until independently authored evidence satisfies every gate in `../conformance/PASS_CRITERIA.md`.
