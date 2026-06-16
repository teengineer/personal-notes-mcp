import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pathlib import Path
from mcp.server.fastmcp import FastMCP
from db import vector_search, init_db, upsert_note
import frontmatter
import sys
import logging

from db import vector_search

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,  # önemli: stdout DEĞİL!
    format='%(asctime)s [%(levelname)s] %(message)s'
)

NOTES_DIR = Path.home() / "claude-notes"
NOTES_DIR.mkdir(exist_ok=True)
DB_PATH = Path(__file__).parent / "notes.db"

mcp = FastMCP("personal-notes")

conn = init_db(DB_PATH)

@mcp.tool()
def create_note(title: str, content: str, tags: list[str] = []) -> str:
    """Create new note with optional tags"""
    slug = title.lower().replace(" ", "-")
    path = NOTES_DIR / f"{slug}.md"
    post = frontmatter.Post(content,title=title, tags = tags)
    path.write_text(frontmatter.dumps(post), encoding="utf-8")

    # add new note to db
    upsert_note(conn=conn,filename=slug, content=content)

    return f"Note created : {path.name}"


# @mcp.tool()
# def search_notes(query: str) -> list[dict]:
#     """Search all notes by substring match."""
#     results=[]
#     for path in NOTES_DIR.glob("*.md"):
#         post = frontmatter.load(path)
#         if query.lower() in post.content.lower() or query.lower() in post.get("title", "").lower():
#             results.append({
#                 "file": path.name,
#                 "title": post.get("title",""),
#                 "preview": post.content[:200]
#             })
#     return results


@mcp.tool()
def list_notes() -> list[str]:
    """List all note filenames."""
    return [p.name for p in NOTES_DIR.glob("*.md")]

@mcp.tool()
def semantic_search_notes(query: str, limit: int = 5) -> list[dict]:
    logging.info(f"semantic_search_notes called: query='{query}', limit={limit}")

    results=[]

    try:
        logging.info(f"Calling vector_search...")
        search_results = vector_search(conn=conn,query=query, k=limit)
        logging.info(f"Got {len(search_results)} results")

        for result in search_results:
            results.append({
                "file": result["filename"],
                "content": result["content"]
            })
        logging.info(f"Returning {len(results)} results")

    except Exception as e:
        logging.error(f"Search error: {e}")
        return [{"file":"ERROR", "content":str(e)}]

    return results



if __name__ == "__main__":
    try:
        mcp.run()
    except Exception as e:
        logging.exception("Server crashed")
        raise

