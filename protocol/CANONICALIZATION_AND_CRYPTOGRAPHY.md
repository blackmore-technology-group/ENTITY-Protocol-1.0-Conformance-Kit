# ENTITY 1.0 Canonicalization and Cryptography

## JSON canonical form

For signed/hash-committed JSON objects in this kit:

1. Encoding is UTF-8.
2. Object keys are emitted in ascending lexicographic key order.
3. There is no whitespace between tokens.
4. Key/value separator is `:`.
5. Item separator is `,`.
6. Strings remain Unicode and are emitted as UTF-8 rather than ASCII-only escaping.
7. `NaN`, `Infinity` and non-JSON values are invalid.
8. Published vectors use ASCII object keys to avoid collation ambiguity.

Equivalent pseudocode:

```text
UTF8(JSON(value, sort_keys=true, separators=(",", ":"), ensure_ascii=false))
```

## SHA-256

Hex digests are lowercase 64-character SHA-256 values.

## Base64url

Ed25519 keys and signatures use URL-safe Base64 without `=` padding unless a schema explicitly says otherwise.

## Entity identifiers

`ent2` matches `^ent2-[a-z2-7]{52}$`.

An `ent2` identifier is a persistent opaque Entity root identifier. It is not derived from an alias, provider account, device ID, DNS name or current signing key.

Legacy `ent1` matches `^ent1-[a-z2-7]{52}$` and is:

```text
"ent1-" + lowercase_base32_no_padding(SHA256(raw_ed25519_public_key))
```

## Manifest signature — sovereign-entity-manifest-v2

A v2 manifest contains a top-level `signature` object with `key_id`, suite `ENTITY-SIG-ED25519-v1`, and a base64url signature.

Verification:
1. Remove the top-level `signature`.
2. Find `verification_methods[]` with matching `key_id`.
3. Method status MUST be `active`.
4. Method suite MUST be `ENTITY-SIG-ED25519-v1`.
5. Ed25519-verify over canonical JSON bytes of the remaining manifest.
6. `entity_id` MUST match ENTITY identifier syntax.
7. Alias/display-name fields are not authority.

## Signature record — entity-signature-record-v2

For node authorization, service manifests, relationships and exports, the signature record contains `signature_schema`, `entity_id`, `key_id`, `suite`, `signed_at_ms`, `payload_sha256`, and `signature`.

Verification:
1. Compute `SHA256(canonical_json(payload))`; it MUST equal `payload_sha256`.
2. Resolve the referenced active verification method from the signer's valid Entity manifest.
3. Remove `signature` from the signature record.
4. Ed25519-verify canonical JSON bytes of the remaining signature record.
5. Signature-record `entity_id` MUST equal the expected signer.

## Alias rule

Aliases are presentation/routing hints only. Verification uses the canonical Entity root.

## Sovereign Domain crypto

- Entity signatures: Ed25519
- Hash: SHA-256
- Direct-session key agreement: X25519 + HKDF-SHA256
- Session AEAD: AES-256-GCM

Direct-session crypto is exercised in live interoperability, not required for the offline phase-one PASS.
