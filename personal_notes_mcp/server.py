from pathlib import Path
from mcp.server.fastmcp import FastMCP
import frontmatter
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,  # önemli: stdout DEĞİL!
    format='%(asctime)s [%(levelname)s] %(message)s'
)

NOTES_DIR = Path.home() / "claude-notes"
NOTES_DIR.mkdir(exist_ok=True)

mcp = FastMCP("personal-notes")

@mcp.tool()
def create_note(title: str, content: str, tags: list[str] = []) -> str:
    """Create new note with optional tags"""
    slug = title.lower().replace(" ", "-")
    path = NOTES_DIR / f"{slug}.md"
    post = frontmatter.Post(content,title=title, tags = tags)
    path.write_text(frontmatter.dumps(post), encoding="utf-8")
    return f"Note created : {path.name}"


@mcp.tool()
def search_notes(query: str) -> list[dict]:
    """Search all notes by substring match."""
    results=[]
    for path in NOTES_DIR.glob("*.md"):
        post = frontmatter.load(path)
        if query.lower() in post.content.lower() or query.lower() in post.get("title", "").lower():
            results.append({
                "file": path.name,
                "title": post.get("title",""),
                "preview": post.content[:200]
            })
    return results


@mcp.tool()
def list_notes() -> list[str]:
    """List all note filenames."""
    return [p.name for p in NOTES_DIR.glob(".md")]


if __name__ == "__main__":
    try:
        mcp.run()
    except Exception as e:
        logging.exception("Server crashed")
        raise