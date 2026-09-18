# Conformance Vectors

All identities, nodes, services, assets and signatures in this directory are synthetic test material and carry no production authority.

The vector set contains **11 valid** and **15 invalid** cases.

`VECTOR_MANIFEST.json` is authoritative for:
- vector ID;
- relative path;
- kind passed to the candidate CLI;
- expected accept/reject result;
- required semantic facts where applicable;
- SHA-256 of the frozen vector file.

Do not modify vectors during an independent implementation campaign. If a defect is found, report it and use a new/superseding kit version rather than silently replacing the tested input.
