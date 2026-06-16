import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0,str(Path(__file__).parent))

from db import init_db, upsert_note

NOTES_DIR = Path.home() / "claude-notes"
DB_PATH = Path(__file__).parent / "notes.db"

def backfill():
    
    conn = init_db(DB_PATH)

    md_files = list(NOTES_DIR.glob("*.md"))
    print(f"Found {len(md_files)} markdown files in {NOTES_DIR}")

    if not md_files:
        print("No files to backfill")
        conn.close()
        return
    
    error_count = 0
    success_count = 0

    for file in sorted(md_files):
        
        try:
            filename=file.name
            content = file.read_text(encoding="utf-8")
            note_id = upsert_note(conn=conn, filename=filename, content=content)
            print(f"✓ {filename} (id={note_id}, {len(content)} chars)")
            success_count += 1
        
        except Exception as e:
            print(f"✗ {file.name}: {e}")
            error_count += 1



    #test (daha sonra kapat)
    print("=====VECTOR SEARCH=====")
    from db import vector_search

    seach_result = vector_search(conn=conn,query="Ilk Notum",k=5)
    print(f"search_result={len(seach_result)}")
    for r in seach_result:
        print(f"{r}")
    #test end


    conn.close()

    # Özet
    print(f"\n=== BACKFILL SUMMARY ===")
    print(f"Success: {success_count}")
    print(f"Errors: {error_count}")
    print(f"DB: {DB_PATH}")

if __name__ == "__main__":
    print("it is starting")
    backfill()
    