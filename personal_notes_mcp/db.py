import os
import struct
import sqlite3
import voyageai
import sqlite_vec

from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv() # .env dosyasindaki degiskenleri yukler

# voyageai tek seferlik olusur
_voyage_client = voyageai.Client(os.getenv("VOYAGE_API_KEY"))

EMBEDDING_DIM = 1024

def init_db(path:str) -> sqlite3.Connection:
    
    conn = sqlite3.connect(path)

    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)

    conn.row_factory = sqlite3.Row

    conn.executescript(f"""
                       CREATE TABLE IF NOT EXISTS notes (
                              id             INTEGER    PRIMARY KEY AUTOINCREMENT,
                              filename       TEXT UNIQUE NOT NULL,
                              content        TEXT NOT NULL,
                              created_at     TEXT NOT NULL,
                              updated_at     TEXT NOT NULL
                       );

                       CREATE VIRTUAL TABLE IF NOT EXISTS note_embeddings USING vec0(
                              note_id INTEGER PRIMARY KEY,
                              embedding FLOAT({EMBEDDING_DIM})
                       )
                       """)
    
    conn.commit()
    return conn

def embed(text:str, input_type: str = 'document') -> list[float]:
    
    if not text or not text.strip():
        raise ValueError("Empty text cannot be embedded")
    
    result = _voyage_client.embed(
        texts=[text],
        model='voyage-3',
        input_type=input_type
    )

    return result.embeddings[0]

def _serialize_embedding(vec: list[float]) -> bytes:
    
    return struct.pack(f"{len(vec)}f", *vec)

def upsert_note(conn: sqlite3.Connection, filename: str, content: str) :
    
    if not filename or not filename.strip() or not content or not content.strip():
        raise ValueError("Empty filename or content cannot be embedded")
    
    now = datetime.now(timezone.utc).isoformat()

    # 1) notes tablosuna yaz
    cursor= conn.execute(
        """
        INSERT INTO notes (filename, content, created_at, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(filename) DO UPDATE SET
            content = excluded.content,
            updated_at = excluded.updated_at
        RETURNING id
        """,
    (filename, content, now, now),
    )

    note_id = cursor.fetchone()["id"]

    # 2) embeddingi hesapla
    vec = embed(content)
    blob = _serialize_embedding(vec=vec)

    # 3) note_embeddinge yaz
    conn.execute("DELETE FROM note_embeddings WHERE note_id = ?", (note_id,))
    conn.execute(
        "INSERT INTO note_embeddings (note_id, embedding) VALUES (?, ?)",
        (note_id, blob),
        )

    conn.commit()
    return note_id


def vector_search(
        conn: sqlite_vec.Connection,
        query: str,
        k: int = 5,
        threshold: float=2.0
) -> list[dict]:
    
    if not query or not query.strip():
        return[]
    
    k = max(1, min(k,1000))
    
    # 1) queryi embed et
    query_vec = embed(query, input_type='query')
    query_blob = _serialize_embedding(query_vec)

    embedding_results = conn.execute(
        f"""
        SELECT 
            note_id,
            distance
        FROM note_embeddings
        WHERE embedding MATCH ?
        ORDER BY distance ASC
        LIMIT {k}
        """,
        (query_blob,)
    ).fetchall()

    filtered = [r for r in embedding_results if r["distance"] <= threshold]

    final_results = []
    for row in filtered:
        note = conn.execute(
            "SELECT filename, content FROM notes WHERE id = ?",
            (row["note_id"],)
        ).fetchone()

        if note:
            final_results.append({
                "note_id": row["note_id"],
                "filename": note["filename"],
                "content": note["content"],
                "distance": row["distance"]
            })
    
    return final_results
    

if __name__ == "__main__":
    db_path = Path(__file__).parent / "notes.db"

    # if db_path.exists():
    #     db_path.unlink()
    #     print(f"Deleted old database: {db_path}")

    conn = init_db(db_path)

    # version = conn.execute("SELECT vec_version()").fetchone()[0]
    # print(f"sqlite-vec version: {version}")

    # tables = conn.execute(
    #     "SELECT name FROM sqlite_master WHERE type IN ('table', 'virtual_table') ORDER BY name"
    # ).fetchall()
    # print(f"Tables: {[t['name'] for t in tables]}")

    # # ← BURAYA EKLE
    # print("\n=== BEFORE UPSERT ===")
    # note_count = conn.execute("SELECT COUNT(*) AS c FROM notes").fetchone()["c"]
    # emb_count = conn.execute("SELECT COUNT(*) AS c FROM note_embeddings").fetchone()["c"]
    # print(f"Notes: {note_count}, Embeddings: {emb_count}")

    # upsert_note test
    # print("\nTesting upsert_note()...")
    # id1 = upsert_note(conn, "test1.md", "Carbonara tarifi: yumurta, peynir, guanciale, biber.")
    # id2 = upsert_note(conn, "test2.md", "Delphi VCL'de TStringList kullanımı ve performans notları.")
    # id3 = upsert_note(conn, "test3.md", "PBI 42123: index'leme stratejisi için Ahmet ile toplantı yapıldı.")
    # print(f"Inserted note IDs: {id1}, {id2}, {id3}")

    # # ← VE BURAYA EKLE
    # print("\n=== AFTER UPSERT ===")
    # note_count = conn.execute("SELECT COUNT(*) AS c FROM notes").fetchone()["c"]
    # emb_count = conn.execute("SELECT COUNT(*) AS c FROM note_embeddings").fetchone()["c"]
    # print(f"Notes: {note_count}, Embeddings: {emb_count}")

    # vector_search test
    print("\nTesting vector_search()...")
    results1 = vector_search(conn, "makarna tarifii", k=3)
    print(f"Query 'makarna tarifii' results: {len(results1)} found")
    for r in results1:
        print(f"  - {r['filename']}: distance={r['distance']:.4f}")