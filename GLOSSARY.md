# ENTITY Protocol 1.0 — Plain-Language Implementer Glossary

This glossary is an onboarding aid for the sealed external conformance kit. It does **not** replace the normative schemas, interoperability profile, canonicalization rules, clean-room rules, vectors, or pass criteria. If this glossary conflicts with those artifacts, the sealed protocol material wins.

## Core terms

### vector
A **conformance test case/input** supplied by the kit. In this repository, “vector” does not mean a mathematical vector or an attack vector. Valid and invalid vectors are used to test whether an implementation makes the expected protocol decision.

### Entity / entity root
A protocol identity represented by an `ent1-...` or `ent2-...` identifier and a sovereign Entity manifest. The interoperability profile treats the **Entity root as authoritative**. `ent2` identifiers are opaque and are intended to persist across operational-key or provider replacement.

### Entity ID
The protocol identifier matching the public `ent1` / `ent2` format. It identifies the Entity root used by the protocol; it is not the same thing as a display name, alias, DNS name, hosting account, or provider identity.

### alias
A governed alternate name/identifier associated with an Entity. An alias is **not an independent source of authority**. The minimum clean-room challenge explicitly requires implementations to distinguish aliases from authority.

### authority
Permission recognized by the protocol for a bounded action or scope. Authority is evaluated from the relevant signed/scoped protocol records; possession, hosting, storage, naming, or topology alone does not create it.

### sovereign authority
The root/control relationship recognized by ENTITY for an Entity. In this kit, “sovereign” does **not** mean a government assertion and does not mean that a hosting provider, DNS holder, storage operator, or infrastructure owner automatically has ENTITY authority.

### principal
The Entity that acts as the principal in the Principal → Device → Installation → Application binding flow. The binding is signed by the principal and binds the four Entity manifests plus the scoped relationships used by the clean-room profile.

### relationship
A signed/scoped record connecting an Entity to another party/reference. Relationship records carry a relationship type, scope, status and evidence origin. The interoperability profile requires specific active relationships in the principal binding flow and explicitly treats relationships as scoped and revocable.

### manifest
A signed protocol document describing an Entity or service state. A valid manifest signature establishes cryptographic control by the applicable active verification method; it does **not**, by itself, establish arbitrary legal ownership or factual truth.

### verification method
A public-key method carried by an Entity manifest. The public schema allows `active`, `retired`, and `revoked` status values. Protocol verification must use the applicable active method; a cryptographically well-formed signature is not enough if the authority/state rules fail.

### signature record
The protocol object carrying the signing key reference, signature suite and signature value used to verify signed protocol material. Signature verification establishes cryptographic integrity/control within the protocol rules; it is not a general proof of external-world truth.

### schema validity vs. protocol validity
JSON Schema checks structural requirements. Protocol validity additionally depends on cryptographic verification, authority state, revocation, lineage and the semantic rules in the interoperability profile. A document can be schema-valid and still be protocol-invalid; several invalid vectors intentionally test this distinction.

### fail closed
If a required authority/signature/binding check fails, or an unsupported major version is encountered, the implementation rejects rather than silently accepting or widening authority.

### lineage / derivation lineage
The parent/derivation relationship carried by protocol objects such as asset envelopes. Parent asset IDs preserve derivation lineage; registration or lineage does not by itself infer ownership or economic value.

### Domain
An `entity-domain-v1` object bound to an Entity root. The public schema explicitly says a BTG host, DNS, and a registrar are not required for the Domain object itself. Domain verification still follows the ordered identity/authorization/revocation/service/policy checks in the interoperability profile.

### name claim
A signed `entity-name-claim-v1` object connecting a normalized name/namespace to a Domain and Entity root. Its schema explicitly preserves that first-seen status is not ownership and DNS possession is not authority.

### node authorization
A signed `entity-node-authorization-v1` record defining a node, its public key, permitted services and network/publication/data scopes, effective time, optional expiry, and active authorization version.

### node revocation
A signed `entity-node-revocation-v1` record identifying the Domain, node, Entity root, reason and effective revocation time. Domain verification must apply authorization/revocation state before treating a node as authorized.

### asset envelope
An `entity-open-sdk-asset-envelope-v1.1` object describing a governed asset reference. It carries application/controller Entity IDs, content hash, size/media/title, `asset_kind`, optional lineage/contributor metadata, and requires `raw_content_included=false`. Registration does not infer ownership or economic value.

### event envelope
An `entity-open-sdk-event-envelope-v1` object for a governed event reference. The interoperability profile requires hashed payload representation with `raw_payload_included=false`, restricts event prefixes, and rejects generic submission of authority/ownership/licence/payment/settlement and similar semantics.

### Domain export
An `entity-domain-export-package-v1` package designed to remain interpretable without the originating BTG runtime. Verification recomputes package and embedded commitments, verifies the Entity root/signature chain, and requires that proprietary BTG databases and DNS are not necessary for interpretation.

## Enumeration / controlled-value guide

These fields are not all equivalent. Some are classification labels; others directly participate in protocol acceptance or authority state.

| Field | Allowed values in the public kit | How to read it |
| --- | --- | --- |
| `entity_type` | `person`, `family`, `business`, `product`, `application`, `system`, `community`, `service`, `organization`, `project` | A controlled classification on the Entity manifest. It does not itself grant authority. |
| `verification_methods.status` | `active`, `retired`, `revoked` | Semantic key state. The interoperability profile requires cryptographic control by an applicable active verification method. |
| `asset_kind` | `SOFTWARE`, `DATA`, `MODEL`, `KNOWLEDGE`, `EVIDENCE` | A required asset classification and part of asset-envelope validation. It does not by itself create ownership or economic value. |
| `conflict_state` | `CLEAR`, `CONFLICT` | Controlled state on a name claim. It concerns the claim’s conflict state; the same schema separately states that first-seen status is not ownership and DNS possession is not authority. |
| `delegated_actions` | `INGEST_ASSET`, `RECORD_EVENT` | Explicit actions carried by the principal binding. They are bounded delegated actions, not an open-ended grant of authority. |
| relationship `status` | `ACTIVE`, `REVOKED` | Semantic relationship state; the binding profile requires the relevant relationships to be active. |

## Four distinctions to keep visible while implementing

1. **Identity ≠ alias.** The Entity root is authoritative; an alias is not.
2. **Signature ≠ truth.** A valid signature proves the relevant cryptographic control/integrity, not arbitrary external-world truth.
3. **Possession/hosting ≠ authority.** Provider, device, DNS, storage, or infrastructure possession does not automatically create sovereign authority.
4. **Registration/lineage ≠ ownership/economic value.** Asset registration and derivation history do not automatically establish title, rights, or economic value.

## Normative starting points

After this glossary, implement from:

- `protocol/ENTITY_PROTOCOL_1_0_INTEROPERABILITY_PROFILE.md`
- `protocol/CANONICALIZATION_AND_CRYPTOGRAPHY.md`
- `profiles/CLEAN_ROOM_RULES.md`
- `conformance/IMPLEMENTATION_INTERFACE.md`
- `vectors/VECTOR_MANIFEST.json`
- `conformance/PASS_CRITERIA.md`
- `schemas/`
