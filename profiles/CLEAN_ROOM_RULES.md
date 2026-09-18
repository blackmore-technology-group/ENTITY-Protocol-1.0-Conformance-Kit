# Clean-Room Rules

Allowed inputs:
- this repository;
- ordinary public standards/libraries for JSON, SHA-256, Ed25519, X25519, HKDF-SHA256 and AES-GCM;
- public clarification/errata issued in this repository.

Not allowed as implementation inputs:
- source from `blackmore-technology-group/ENTITY`;
- copied/translated BTG Python classes/functions;
- BTG internal databases/state;
- private ENTITY keys;
- internal qualification runner code;
- unpublished implementation explanations.

Questions about specification meaning are allowed. Material clarifications must be recorded publicly before qualification relies on them.

A language other than Python is strongly preferred. The independent party MUST hash-identify its exact source/build used for final evidence.
