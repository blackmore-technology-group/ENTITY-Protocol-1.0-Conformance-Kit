#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import sys
import warnings

warnings.filterwarnings("ignore", message="jsonschema.RefResolver is deprecated.*", category=DeprecationWarning)
from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
VECTOR_MANIFEST = ROOT / "vectors" / "VECTOR_MANIFEST.json"

ALLOWED_PY = {
    "conformance/black_box_tests/run_conformance.py",
    "tools/validate_kit.py",
    "tools/verify_kit.py",
}
FORBIDDEN_SUFFIXES = {
    ".key", ".pem", ".p12", ".pfx", ".jks", ".keystore",
    ".sqlite", ".sqlite3", ".db", ".entitybackup", ".exe", ".dll",
    ".apk", ".ipa", ".aab",
}
FORBIDDEN_PATH_PARTS = {
    "01_Core_Runtime", "04_Entity_Registry", "10_NIKI", "11_ADAM", "12_BSIE",
    "production_state", "BTG_ENTITY_PRODUCTION_STATE",
}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".py", ".yml", ".yaml", ".cfg", ".toml", ".ini", ".csv"}
TEXT_NAMES = {"LICENSE", ".gitignore", ".editorconfig", ".gitattributes", "NOTICE"}
SPECIAL_FACTS = {
    "asset_lineage_bundle": {"ownership_inferred": False, "economic_value_inferred": False},
    "revoked_node_bundle": {"current_authority": False},
    "resolution_proof": {"resolver_is_authority": False, "dns_used_as_authority": False},
    "domain_export_package": {"proprietary_btg_database_required": False, "dns_required_for_interpretation": False},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cp1252_byte(ch: str):
    try:
        encoded = ch.encode("cp1252")
        if len(encoded) == 1:
            return encoded[0]
    except UnicodeEncodeError:
        pass
    code = ord(ch)
    if 0x80 <= code <= 0x9F:
        return code
    if code <= 0xFF:
        return code
    return None


def reconstructable_mojibake_count(text: str) -> int:
    count = 0
    i = 0
    while i < len(text):
        lead = cp1252_byte(text[i])
        length = 0
        if lead is not None:
            if 0xC2 <= lead <= 0xDF:
                length = 2
            elif 0xE0 <= lead <= 0xEF:
                length = 3
            elif 0xF0 <= lead <= 0xF4:
                length = 4
        if length and i + length <= len(text):
            vals = [cp1252_byte(c) for c in text[i:i + length]]
            if None not in vals and all(0x80 <= v <= 0xBF for v in vals[1:]):
                try:
                    bytes(vals).decode("utf-8")
                except UnicodeDecodeError:
                    pass
                else:
                    count += 1
                    i += length
                    continue
        i += 1
    return count


def check_clean_room(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden operational artifact: {rel}")
        if any(part in FORBIDDEN_PATH_PARTS for part in path.parts):
            errors.append(f"forbidden reference/internal path: {rel}")
        if path.name.startswith("canonical_") and path.suffix == ".py":
            errors.append(f"reference implementation source forbidden: {rel}")
        if path.suffix == ".py" and rel not in ALLOWED_PY:
            errors.append(f"unexpected Python implementation file: {rel}")


def check_text(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in TEXT_NAMES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as exc:
            errors.append(f"invalid UTF-8: {rel}: {exc}")
            continue
        if "\ufffd" in text:
            errors.append(f"Unicode replacement character: {rel}")
        if re.search(r"(?i)\\b[A-Z]:\\\\", text):
            errors.append(f"absolute Windows path leaked into public kit: {rel}")
        private_markers = tuple(
            "-----BEGIN " + kind + "PRIVATE KEY-----"
            for kind in ("", "RSA ", "EC ", "OPENSSH ")
        )
        if any(marker in text for marker in private_markers):
            errors.append(f"private-key block leaked into public kit: {rel}")
        n = reconstructable_mojibake_count(text)
        if n:
            errors.append(f"reconstructable mojibake ({n}): {rel}")


def check_json(errors: list[str]) -> dict[str, object]:
    parsed = {}
    for path in ROOT.rglob("*.json"):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        try:
            parsed[rel] = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            errors.append(f"invalid JSON: {rel}: {exc}")
    return parsed


def check_protocol_hashes(parsed: dict[str, object], errors: list[str]) -> None:
    version = parsed.get("PROTOCOL_VERSION.json")
    if not isinstance(version, dict):
        errors.append("PROTOCOL_VERSION.json missing/unreadable")
        return
    checks = {
        "protocol_freeze_sha256": "protocol/ENTITY_PROTOCOL_1_0_FREEZE.json",
        "domain_protocol_sha256": "protocol/ENTITY_DOMAIN_PROTOCOLS_v1.md",
        "principal_binding_profile_sha256": "profiles/PRINCIPAL_BINDING_PROFILE_v1.md",
        "public_trust_material_sha256": "trust/ENTITY_RELEASE_SIGNER_PUBLIC.json",
    }
    for field, rel in checks.items():
        actual = sha256(ROOT / rel)
        if version.get(field) != actual:
            errors.append(f"protocol hash mismatch {field}: expected={version.get(field)} actual={actual}")


def check_vectors(parsed: dict[str, object], errors: list[str]) -> None:
    manifest = parsed.get("vectors/VECTOR_MANIFEST.json")
    if not isinstance(manifest, dict) or not isinstance(manifest.get("vectors"), list):
        errors.append("vector manifest missing/invalid")
        return
    seen = set()
    valid = invalid = 0
    for item in manifest["vectors"]:
        vid = item.get("id")
        if not vid or vid in seen:
            errors.append(f"duplicate/missing vector id: {vid}")
        seen.add(vid)
        rel = item.get("path")
        path = ROOT / str(rel)
        if not path.is_file():
            errors.append(f"vector missing: {rel}")
            continue
        actual = sha256(path)
        if actual != item.get("sha256"):
            errors.append(f"vector hash mismatch: {rel}")
        accepted = (item.get("expected") or {}).get("accepted")
        if accepted is True:
            valid += 1
        elif accepted is False:
            invalid += 1
        else:
            errors.append(f"vector expectation not boolean: {vid}")
        required_facts = SPECIAL_FACTS.get(str(vid))
        if required_facts:
            facts = (item.get("expected") or {}).get("facts") or {}
            for key, val in required_facts.items():
                if facts.get(key) != val:
                    errors.append(f"semantic expected fact missing/mismatch {vid}.{key}")
    if valid != 11 or invalid != 15 or valid + invalid != 26:
        errors.append(f"unexpected vector counts valid={valid} invalid={invalid} total={valid+invalid}")


def validate_schema(instance_rel: str, schema_rel: str, errors: list[str]) -> None:
    instance = json.loads((ROOT / instance_rel).read_text(encoding="utf-8"))
    schema_path = SCHEMAS / schema_rel
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    resolver = RefResolver(base_uri=SCHEMAS.as_uri() + "/", referrer=schema)
    try:
        Draft202012Validator(schema, resolver=resolver).validate(instance)
    except Exception as exc:
        errors.append(f"schema validation failed {instance_rel} vs {schema_rel}: {exc}")


def check_valid_schemas(errors: list[str]) -> None:
    pairs = [
        ("vectors/valid/entity_manifest_v2.json", "entity_identity.schema.json"),
        ("vectors/valid/principal_binding_bundle.json", "principal_binding_bundle.schema.json"),
        ("vectors/valid/asset_envelope_v1_1.json", "asset_envelope.schema.json"),
        ("vectors/valid/event_envelope_v1.json", "event_envelope.schema.json"),
        ("vectors/valid/domain_snapshot.json", "domain_snapshot.schema.json"),
        ("vectors/valid/node_authorization.json", "node_authorization.schema.json"),
        ("vectors/valid/service_manifest.json", "service_manifest.schema.json"),
        ("vectors/valid/resolution_proof.json", "resolution_proof.schema.json"),
        ("vectors/valid/domain_export_package.json", "domain_export.schema.json"),
        ("vectors/valid/revoked_node_bundle.json", "revoked_node_bundle.schema.json"),
    ]
    for instance, schema in pairs:
        validate_schema(instance, schema, errors)


def main() -> int:
    errors: list[str] = []
    check_clean_room(errors)
    check_text(errors)
    parsed = check_json(errors)
    check_protocol_hashes(parsed, errors)
    check_vectors(parsed, errors)
    check_valid_schemas(errors)

    result = {
        "schema": "entity-conformance-kit-self-validation-v1",
        "valid": not errors,
        "errors": errors,
        "vector_total": 26,
        "reference_implementation_source_included": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
