from pathlib import Path
from dotenv import load_dotenv
from db import init_db

# .env yükle
load_dotenv(Path(__file__).parent.parent / ".env")

conn = init_db(Path(__file__).parent / "notes.db")
rows = conn.execute('SELECT note_id, LENGTH(embedding) as emb_size FROM note_embeddings').fetchall()

if not rows:
    print("No embeddings found")
else:
    for r in rows:
        print(f'note_id={r[0]}, embedding_size={r[1]}')

conn.close()