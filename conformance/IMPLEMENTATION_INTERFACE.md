# Candidate Implementation Interface

The black-box runner invokes your implementation as an external process:

```text
<CANDIDATE> verify --kind <KIND> --input <PATH>
```

It MUST write one JSON object to stdout:

```json
{
  "protocol": "ENTITY-1.0",
  "implementation": "YourProject-0.1.0",
  "accepted": true,
  "reason_category": "valid",
  "facts": {}
}
```

- exit `0`: candidate evaluated the vector;
- non-zero: crash/indeterminate;
- `accepted` is mandatory boolean;
- `reason_category` should match the public category when practical;
- `facts` may include lineage/non-authority conclusions.

Required kinds:
`entity_manifest`, `principal_binding_bundle`, `asset_envelope`, `event_envelope`, `asset_lineage_bundle`, `domain_snapshot`, `node_authorization`, `service_manifest`, `resolution_proof`, `domain_export`, `revoked_node_bundle`.

For evidence, candidate SHOULD also support `<CANDIDATE> describe` returning implementation/version/language/source commit/build SHA-256.
