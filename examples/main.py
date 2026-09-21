
import argparse
from pathlib import Path
from ingestion.markitdown_wrapper import ingest_file
from ingestion.crawl4ai_wrapper import ingest_url_sync

def main():
    parser = argparse.ArgumentParser(description="Evidence-First Ingestion")
    parser.add_argument("--input", type=str, default="./sample_docs")
    parser.add_argument("--url", type=str, help="Optional URL")
    parser.add_argument("--output", type=str, default="./evidence/output")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    if args.url:
        print(f"[Crawl4AI] {args.url}")
        derived, ev = ingest_url_sync(args.url, out)
        print(f" -> {derived}")
    input_path = Path(args.input)
    if input_path.exists():
        files = [input_path] if input_path.is_file() else list(input_path.glob("**/*.*"))
        for f in files:
            if f.suffix.lower() in [".pdf",".docx",".pptx",".xlsx",".html",".txt"]:
                print(f"[MarkItDown] {f}")
                try:
                    derived, ev = ingest_file(f, out)
                    print(f" -> {derived}")
                except Exception as e:
                    print(f" skip {f}: {e}")

if __name__ == "__main__":
    main()
