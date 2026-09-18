# Release Signer Trust Boundary

The file `ENTITY_RELEASE_SIGNER_PUBLIC.json` is the public cryptographic identity used to verify the sealed conformance-kit signature.

A successful signature check proves:
- the kit manifest was signed by possession of the private key corresponding to the published release-signer Entity;
- the signed artifact hashes have not changed.

It does **not by itself** prove that an unknown copy of this public signer manifest belongs to Blackmore Technology Group. External trust in the signer should be established by at least one independently pinned channel, such as:
- the official `blackmore-technology-group` GitHub repository/release/tag;
- the previously published signed ENTITY distribution trust reference;
- another BTG-controlled public channel or independent archival/pinning record.

The internal prerequisite distribution recorded the release-signer trust-root file SHA-256 as:

`d8d50870f7288df757d292e000c46becc4bc36763a32d453f7973733ba5a5730`

The Git repository may normalize text line endings, so this kit additionally signs the hash of the exact trust-manifest bytes contained in the sealed kit.
