
from pathlib import Path
from markitdown import MarkItDown
from .utils.evidence import make_evidence_record, save_evidence

def ingest_file(input_path: Path, output_dir: Path, revision="v1"):
    output_dir.mkdir(parents=True, exist_ok=True)
    md = MarkItDown()
    result = md.convert(str(input_path))
    derived = output_dir / f"{input_path.stem}.md"
    derived.write_text(result.text_content, encoding="utf-8")
    evidence = make_evidence_record(
        source_path=input_path,
        derived_path=derived,
        extraction_tool="markitdown",
        revision=revision,
        extra_params={"tool": "microsoft/markitdown", "license": "MIT"}
    )
    save_evidence(evidence, output_dir / f"{input_path.stem}.evidence.json")
    return derived, evidence
