from pathlib import Path
from dotenv import load_dotenv
from db import init_db, embed, _serialize_embedding

load_dotenv(Path(__file__).parent.parent / ".env")

conn = init_db(Path(__file__).parent / "notes.db")

# 1) Query embed et
query = "makarna tarifii"
query_vec = embed(query, input_type="query")
query_blob = _serialize_embedding(query_vec)

print(f"Query: '{query}'")
print(f"Query embedding length: {len(query_vec)}")
print(f"Query blob size: {len(query_blob)}")

# 2) Virtual table'dan direkt sorgula
print("\n=== Raw virtual table query ===")
try:
    results = conn.execute(
        f"""
        SELECT 
            note_id,
            distance
        FROM note_embeddings
        WHERE embedding MATCH ?
        ORDER BY distance ASC
        LIMIT 3
        """, 
        (query_blob,)
    ).fetchall()
    print(f"Results found: {len(results)}")
    for r in results:
        print(f"  note_id={r['note_id']}, distance={r['distance']:.4f}")
except Exception as e:
    print(f"Error: {e}")

# 3) Normal notes tablosundan not oku
print("\n=== Notes in database ===")
notes = conn.execute("SELECT id, filename, content FROM notes").fetchall()
for n in notes:
    print(f"  id={n['id']}, filename={n['filename']}, content={n['content'][:50]}...")

conn.close()