
import hashlib, pathlib, datetime, json, mimetypes

def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def make_evidence_record(source_path: pathlib.Path, derived_path: pathlib.Path, extraction_tool: str, source_url=None, revision="v1", extra_params=None):
    stat = source_path.stat() if source_path.exists() else None
    return {
        "source_path": str(source_path.resolve()),
        "source_url": source_url,
        "sha256": sha256_file(source_path) if source_path.exists() and source_path.is_file() else None,
        "file_size": stat.st_size if stat else None,
        "mime_type": mimetypes.guess_type(str(source_path))[0],
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "revision": revision,
        "extraction_tool": extraction_tool,
        "derived_path": str(derived_path.resolve()),
        "extraction_params": extra_params or {},
        "notes": "Extraction Layer is derived, Evidence Layer is baseline"
    }

def save_evidence(record: dict, evidence_path: pathlib.Path):
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    with open(evidence_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
