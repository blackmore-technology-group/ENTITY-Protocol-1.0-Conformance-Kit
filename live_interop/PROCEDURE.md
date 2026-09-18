# Phase-Two Live Bidirectional Interoperability Procedure

Do this only after phase-one vectors pass.

## Independent → BTG
1. Independent implementation creates/loads its own Entity root.
2. It publishes valid node/service objects.
3. BTG verifies the independent identity/node/service.
4. Independent side initiates a protocol request.
5. BTG responds.
6. Independent side verifies the response and authority binding.

## BTG → Independent
1. BTG supplies an ENTITY identity/domain/service object set.
2. Independent implementation verifies current root/node/service authority.
3. BTG initiates a request.
4. Independent implementation responds with its independently generated signed result.
5. BTG verifies the result.

## Principal/device test
Both sides independently evaluate the same Principal → Device → Installation → Application bundle, then repeat with wrong app, modified device, altered principal, bad signature, revoked installation and mismatched hash.

## Provenance test
Independent side must conclude content commitment valid, principal/controller lineage valid, producer binding valid, ownership not inferred, economic value not inferred, and recover parent derivation.

## Sovereign export survival
Create/export an Entity with the BTG reference runtime, stop/remove access to the originating runtime for the test, and give the independent party only the sovereign export plus this kit. The independent party verifies the tested export scope without requiring BTG runtime/database interpretation.

Full interoperability requires both communication directions to pass.
