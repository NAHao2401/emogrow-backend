import psycopg2
import os
import sys
from pathlib import Path

# Add project root to sys.path to import settings
sys.path.append(str(Path(__file__).parent.parent))

try:
    from app.core.config import settings
    DATABASE_URL = settings.DATABASE_URL
except ImportError:
    from dotenv import load_dotenv
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")

print(f"Connecting to: {DATABASE_URL}")

def sync():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Table: emotion_logs
        cols_emotion_logs = [
            ("source", "VARCHAR(20) DEFAULT 'journal'"),
            ("note", "VARCHAR(500)"),
            ("audio_url", "VARCHAR(500)")
        ]
        
        for col, col_type in cols_emotion_logs:
            try:
                cur.execute(f"ALTER TABLE emotion_logs ADD COLUMN {col} {col_type};")
                print(f"Added column '{col}' to emotion_logs")
            except psycopg2.Error as e:
                conn.rollback()
                if "already exists" in str(e):
                    print(f"Column '{col}' already exists in emotion_logs")
                else:
                    print(f"Error adding '{col}' to emotion_logs: {e}")
            else:
                conn.commit()

        # Table: sticker_collections
        try:
            cur.execute("ALTER TABLE sticker_collections ADD COLUMN note VARCHAR(500);")
            print("Added column 'note' to sticker_collections")
        except psycopg2.Error as e:
            conn.rollback()
            if "already exists" in str(e):
                print("Column 'note' already exists in sticker_collections")
            else:
                print(f"Error adding 'note' to sticker_collections: {e}")
        else:
            conn.commit()

        cur.close()
        conn.close()
        print("\n[OK] Database sync complete. Restart your backend server.")
    except Exception as e:
        print(f"\n[ERROR] Connection failed: {e}")

if __name__ == "__main__":
    sync()
