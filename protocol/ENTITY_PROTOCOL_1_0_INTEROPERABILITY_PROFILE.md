# ENTITY Protocol 1.0 External Interoperability Profile

This profile is the fixed clean-room target for the first independent implementation.

## Required object families

A conforming phase-one verifier MUST understand:
- `sovereign-entity-manifest-v2`
- `entity-signature-record-v2`
- `entity-principal-binding-v1`
- binding relationship evidence
- `entity-open-sdk-asset-envelope-v1.1`
- `entity-open-sdk-event-envelope-v1`
- `entity-domain-v1`
- `entity-name-claim-v1`
- `entity-node-authorization-v1`
- `entity-node-revocation-v1`
- `entity-service-manifest-v1`
- `entity-resolution-proof-v1`
- `entity-domain-export-package-v1`

## Identity rules

- Entity root is authoritative; alias is not.
- `ent2` is opaque and persists across operational-key/provider replacement.
- A valid manifest signature proves cryptographic control by an active verification method; it does not by itself prove legal ownership of arbitrary assets or factual truth.
- Provider possession/hosting/storage does not create sovereign authority.

## Principal/device/installation/application binding

Validation MUST:
1. Validate all four required Entity manifests.
2. Remove `principal_signature` and `binding_sha256` to form the binding body.
3. Verify `binding_sha256 == SHA256(canonical_json(binding_body))`.
4. Verify the principal signature record over the binding body.
5. Confirm installation-manifest metadata matches principal/application/device IDs.
6. Confirm active relationships:
   - Principal → Installation: `SOVEREIGN_AUTHORITY`
   - Application → Installation: `PROCESSING_AUTHORITY`
   - Device → Installation: `POSSESSION`
7. Confirm relationship IDs referenced by binding match those records.
8. Treat relationships as scoped/revocable; possession does not imply ownership.
9. Reject changed principal, app, device, installation, hash, relationship or signature.

## Asset envelope

- schema: `entity-open-sdk-asset-envelope-v1.1`
- application/controller IDs are Entity IDs
- content SHA-256 is lowercase 64-hex
- kind ∈ SOFTWARE, DATA, MODEL, KNOWLEDGE, EVIDENCE
- `raw_content_included=false`
- registration does not infer ownership/economic value
- parent asset IDs preserve derivation lineage

## Event envelope

- schema: `entity-open-sdk-event-envelope-v1`
- `raw_payload_included=false`
- payload SHA-256 is lowercase 64-hex
- allowed prefixes: `application.`, `data.`, `model.`, `knowledge.`, `software.`, `evidence.`
- generic submission rejects: `ownership`, `licence`, `license`, `settlement`, `payment`, `capital`, `authority`, `consent`, `rights.verify`, `commodity`

## Sovereign Domain verification order

1. Verify Entity identity manifest.
2. Verify Domain ID/root binding.
3. Verify name claim if used.
4. Verify node authorization/revocation.
5. Verify service/presence signature and expiry.
6. Apply anti-rollback state.
7. Apply access/policy/licence requirements.
8. Establish authenticated transport for live interoperability.
9. Record usage/economic evidence only after authorization.

## Domain export

Validation MUST:
1. Require `entity-domain-export-package-v1`.
2. Recompute package SHA-256 excluding `package_sha256`.
3. Recompute snapshot/identity commitments in export manifest.
4. Confirm one Entity root binds export manifest, identity manifest and domain snapshot.
5. Verify Entity identity manifest.
6. Verify export-manifest signature record.
7. Require `proprietary_btg_database_required=false`.
8. Require `dns_required_for_interpretation=false`.

A valid export is interpretable without the originating BTG runtime.

## Failure rule

Unknown major versions or failed authority/signature/binding checks fail closed.
