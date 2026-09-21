
from pathlib import Path
import datetime
from .utils.evidence import save_evidence

TASK_TEMPLATE = "目標: {goal}\nURL: {url}\n請完成操作後，擷取頁面主要內容為 Markdown 並儲存。"

async def ingest_with_browser(url: str, goal: str, output_dir: Path, revision="v1"):
    from browser_use import Agent
    agent = Agent(task=TASK_TEMPLATE.format(url=url, goal=goal))
    result = await agent.run()
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_name = url.replace("https://","").replace("/","_")[:80] + "_browser"
    derived = output_dir / f"{safe_name}.md"
    content = str(result.final_result() if hasattr(result, 'final_result') else result)
    derived.write_text(content, encoding="utf-8")
    evidence = {
        "source_path": url,
        "source_url": url,
        "sha256": None,
        "file_size": len(content.encode()),
        "mime_type": "text/markdown",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "revision": revision,
        "extraction_tool": "browser-use",
        "derived_path": str(derived.resolve()),
        "extraction_params": {"tool": "browser-use/browser-use", "license": "MIT", "goal": goal},
        "notes": "Browser automation is Extraction Layer, keep login logs as evidence if needed"
    }
    save_evidence(evidence, output_dir / f"{safe_name}.evidence.json")
    return derived, evidence
