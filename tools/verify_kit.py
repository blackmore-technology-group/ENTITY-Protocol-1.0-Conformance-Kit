#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import base64
import hashlib
import json
import sys

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ROOT = Path(__file__).resolve().parents[1]
SIGNED = ROOT / "SIGNED_KIT_MANIFEST.json"
TRUST = ROOT / "trust" / "ENTITY_RELEASE_SIGNER_PUBLIC.json"
SUMS = ROOT / "SHA256SUMS.txt"

LOCAL_VENV_DIR_NAMES = {".venv", "venv"}


def is_local_workspace_artifact(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if not parts:
        return False
    top = ROOT / parts[0]
    return parts[0] in LOCAL_VENV_DIR_NAMES and (top / "pyvenv.cfg").is_file()


def canonical_json(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def b64url_decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verification_method(manifest: dict, key_id: str) -> dict | None:
    for method in manifest.get("verification_methods") or []:
        if method.get("key_id") == key_id:
            return method
    return None


def verify_trust_manifest(manifest: dict) -> None:
    body = dict(manifest)
    sig = dict(body.pop("signature"))
    method = verification_method(body, str(sig.get("key_id") or ""))
    if not method or method.get("status") != "active":
        raise ValueError("trust manifest signing method unavailable/inactive")
    if method.get("suite") != "ENTITY-SIG-ED25519-v1" or sig.get("suite") != "ENTITY-SIG-ED25519-v1":
        raise ValueError("trust manifest suite mismatch")
    pub = Ed25519PublicKey.from_public_bytes(b64url_decode(str(method["public_key"])))
    pub.verify(b64url_decode(str(sig["signature"])), canonical_json(body))


def verify_signature_record(trust: dict, payload: dict, record: dict) -> None:
    if record.get("signature_schema") != "entity-signature-record-v2":
        raise ValueError("unsupported kit signature record")
    if record.get("entity_id") != trust.get("entity_id"):
        raise ValueError("kit signer Entity ID mismatch")
    digest = sha256_bytes(canonical_json(payload))
    if record.get("payload_sha256") != digest:
        raise ValueError("kit signature payload commitment mismatch")
    method = verification_method(trust, str(record.get("key_id") or ""))
    if not method or method.get("status") != "active":
        raise ValueError("kit signer key unavailable/inactive")
    if method.get("suite") != "ENTITY-SIG-ED25519-v1" or record.get("suite") != "ENTITY-SIG-ED25519-v1":
        raise ValueError("kit signature suite mismatch")
    signed_record = dict(record)
    signature = str(signed_record.pop("signature"))
    pub = Ed25519PublicKey.from_public_bytes(b64url_decode(str(method["public_key"])))
    pub.verify(b64url_decode(signature), canonical_json(signed_record))


def verify_sha256sums(strict_worktree: bool = False) -> None:
    if not SUMS.is_file():
        raise ValueError("SHA256SUMS.txt missing")
    listed = set()
    for raw in SUMS.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        digest, rel = raw.split("  ", 1)
        listed.add(rel)
        path = ROOT / rel
        if not path.is_file():
            raise ValueError(f"checksummed file missing: {rel}")
        if sha256_file(path) != digest:
            raise ValueError(f"SHA256SUMS mismatch: {rel}")
    actual = set()
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if not strict_worktree and is_local_workspace_artifact(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel == "SHA256SUMS.txt":
            continue
        actual.add(rel)
    extras = sorted(actual - listed)
    missing = sorted(listed - actual)
    if extras:
        raise ValueError("unsealed extra file(s): " + ", ".join(extras))
    if missing:
        raise ValueError("checksummed file(s) absent: " + ", ".join(missing))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify the signed ENTITY Protocol 1.0 conformance kit.")
    parser.add_argument("--strict-worktree", action="store_true", help="Treat recognized local virtual-environment files as unsealed extras.")
    args = parser.parse_args(argv)

    errors = []
    try:
        trust = json.loads(TRUST.read_text(encoding="utf-8"))
        verify_trust_manifest(trust)
        signed = json.loads(SIGNED.read_text(encoding="utf-8"))
        signature = dict(signed.get("signature") or {})
        body = {k: v for k, v in signed.items() if k != "signature"}
        if body.get("release_signer_entity_id") != trust.get("entity_id"):
            raise ValueError("signed manifest release signer does not match public trust Entity")
        if body.get("public_trust_root_sha256") != sha256_file(TRUST):
            raise ValueError("public trust-root hash mismatch")
        verify_signature_record(trust, body, signature)
        for artifact in body.get("artifacts") or []:
            rel = artifact["path"]
            path = ROOT / rel
            if not path.is_file():
                raise ValueError(f"signed artifact missing: {rel}")
            if sha256_file(path) != artifact["sha256"]:
                raise ValueError(f"signed artifact hash mismatch: {rel}")
            if path.stat().st_size != artifact["bytes"]:
                raise ValueError(f"signed artifact size mismatch: {rel}")
        verify_sha256sums(args.strict_worktree)
    except Exception as exc:
        errors.append(str(exc))

    result = {
        "schema": "entity-external-conformance-kit-verification-v1",
        "valid": not errors,
        "errors": errors,
        "signed_manifest": SIGNED.name,
        "public_trust_manifest": TRUST.relative_to(ROOT).as_posix(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
