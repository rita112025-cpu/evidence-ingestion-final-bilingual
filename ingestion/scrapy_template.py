
import scrapy
from pathlib import Path
import hashlib, datetime, json

class EvidenceSpider(scrapy.Spider):
    name = "evidence_spider"
    def __init__(self, start_urls=None, output_dir="./evidence", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls or []
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    def parse(self, response):
        raw_path = self.output_dir / f"{hashlib.sha256(response.url.encode()).hexdigest()[:16]}.html"
        raw_path.write_bytes(response.body)
        text = response.css("body ::text").getall()
        md = "\n".join([t.strip() for t in text if t.strip()])
        derived = self.output_dir / f"{raw_path.stem}.md"
        derived.write_text(md, encoding="utf-8")
        evidence = {
            "source_path": str(raw_path.resolve()),
            "source_url": response.url,
            "sha256": hashlib.sha256(response.body).hexdigest(),
            "file_size": len(response.body),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "revision": "v1",
            "extraction_tool": "scrapy",
            "derived_path": str(derived.resolve()),
        }
        (self.output_dir / f"{raw_path.stem}.evidence.json").write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")
        yield evidence
