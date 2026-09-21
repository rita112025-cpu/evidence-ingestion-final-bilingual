
from pathlib import Path
import asyncio, datetime
from .utils.evidence import save_evidence

async def ingest_url(url: str, output_dir: Path, revision="v1"):
    from crawl4ai import AsyncWebCrawler
    output_dir.mkdir(parents=True, exist_ok=True)
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        md_content = result.markdown if hasattr(result, 'markdown') else result.cleaned_html
        safe_name = url.replace("https://","").replace("http://","").replace("/","_")[:80]
        derived = output_dir / f"{safe_name}.md"
        derived.write_text(md_content, encoding="utf-8")
        evidence = {
            "source_path": url,
            "source_url": url,
            "sha256": None,
            "file_size": len(md_content.encode()),
            "mime_type": "text/markdown",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "revision": revision,
            "extraction_tool": "crawl4ai",
            "derived_path": str(derived.resolve()),
            "extraction_params": {"tool": "unclecode/crawl4ai", "license": "Apache-2.0"},
            "notes": "URL is baseline evidence, markdown is derived"
        }
        save_evidence(evidence, output_dir / f"{safe_name}.evidence.json")
        return derived, evidence

def ingest_url_sync(url: str, output_dir: Path, revision="v1"):
    return asyncio.run(ingest_url(url, output_dir, revision))
