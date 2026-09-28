# ENTITY Protocol 1.0 — Implementer Object Map

This page gives a new clean-room implementer a **navigation map**, not a replacement specification. The schemas and protocol profile remain authoritative.

## Suggested reading order

```text
Entity identity
  ↓
Signature verification
  ↓
Principal / device / installation / application binding
  ↓
Asset + event envelopes
  ↓
Relationships and lineage
  ↓
Domain + name claim
  ↓
Node authorization / revocation
  ↓
Service / resolution / snapshot
  ↓
Portable domain export
```

## Object families

| Public schema / concept | Plain-language purpose in the phase-one kit | Main implementation question |
| --- | --- | --- |
| `entity_identity` / `sovereign-entity-manifest-v2` | Signed root identity manifest for an Entity, including Entity ID, aliases, verification methods, signing-key state and recovery/crypto metadata. | Is this the valid signed root identity, and which verification method is active? |
| `signature_record` / `entity-signature-record-v2` | Signature metadata used by other signed protocol objects. | Does the expected key/suite/signature validly cover the canonical object required by the profile? |
| `principal_binding` / `entity-principal-binding-v1` | Binds Principal, Application, Device and Installation Entity IDs and a bounded set of delegated actions. | Do the binding hash, principal signature, four manifests and required relationships all agree? |
| `principal_binding_bundle` | Package used by the conformance vectors to carry the binding together with the related manifests/relationship evidence needed to verify it. | Can the implementation validate the complete binding context instead of trusting IDs in isolation? |
| `relationship` | Signed/scoped relationship evidence with type, scope, status and evidence origin. | Is the required relationship present, active and scoped as required? |
| `asset_envelope` / `entity-open-sdk-asset-envelope-v1.1` | Hash-addressed asset registration envelope for software, data, models, knowledge or evidence without embedding raw content. | Is the asset envelope structurally/semantically valid while preserving controller, lineage and non-ownership boundaries? |
| `event_envelope` / `entity-open-sdk-event-envelope-v1` | Hash-addressed event envelope without embedding the raw payload. | Is the event type allowed, the payload commitment valid, and the event free of generic authority/ownership/payment claims the profile forbids? |
| `domain` / `entity-domain-v1` | Domain object bound to an Entity root; the public schema does not require BTG hosting, DNS, or a registrar. | Does the Domain ID/root binding resolve to the expected Entity without turning infrastructure into authority? |
| `name_claim` / `entity-name-claim-v1` | Signed normalized-name claim associated with a Domain and Entity root. | Is the name claim valid while preserving the explicit rules that first-seen is not ownership and DNS possession is not authority? |
| `node_authorization` / `entity-node-authorization-v1` | Scoped authorization for a node, including its key, permitted services and network/publication/data scopes, timing and version. | Is this node currently authorized for the requested scope? |
| `node_revocation` / `entity-node-revocation-v1` | Signed revocation event for a previously authorized node. | Has authorization been revoked, and from what effective time? |
| `revoked_node_bundle` | Conformance bundle for evaluating authorization together with revocation evidence. | Does the implementation reject a node once the applicable revocation takes effect? |
| `service_manifest` / `entity-service-manifest-v1` | Signed service/presence material used in the Domain verification sequence. | Is the advertised service/presence signed, current, and within an authorized node context? |
| `resolution_proof` / `entity-resolution-proof-v1` | Proof material used when resolving/interpreting an ENTITY Domain. | Does resolution preserve the Entity-root/Domain binding and the required signed state rather than trusting a locator alone? |
| `domain_snapshot` | Snapshot of Domain state used by the public Domain/export vectors. | Can the implementation interpret the captured Domain state and its commitments consistently? |
| `domain_export` / `entity-domain-export-package-v1` | Portable Domain package intended to remain interpretable without the originating BTG runtime. | Do package, snapshot and identity commitments recompute correctly, bind to one Entity root, and verify without proprietary BTG database or DNS dependence? |
| `transaction_evidence` | Evidence object included in the public schema set for transaction-related evidence representation. | Can the implementation parse/validate the supplied evidence object according to its schema without treating evidence as automatic external truth or authority? |

## What to validate first vs. later

### First: structural parsing
Use `schemas/` to reject objects that do not meet the required JSON structure, constants, patterns and controlled values.

### Second: canonicalization and cryptography
Use `protocol/CANONICALIZATION_AND_CRYPTOGRAPHY.md` to construct the bytes/hashes/signatures exactly as the sealed profile requires.

### Third: semantic/authority rules
Use `protocol/ENTITY_PROTOCOL_1_0_INTEROPERABILITY_PROFILE.md` for rules that JSON Schema cannot establish by itself—for example active verification methods, root-vs-alias authority, principal binding relationships, revocation, anti-rollback sequencing and fail-closed handling.

### Fourth: vectors
Use `vectors/VECTOR_MANIFEST.json` and the valid/invalid vectors as the observable conformance campaign. Do not weaken a rule or alter an expected vector merely to obtain a pass.

## Phase-one success boundary

Phase one is **file/vector conformance** against the sealed kit. It does not by itself establish live interoperability. The published clean-room challenge identifies live bidirectional interoperability with a BTG ENTITY node as a later phase.
