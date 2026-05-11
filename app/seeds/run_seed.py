from app.db.session import SessionLocal

# Import model để SQLAlchemy đăng ký đầy đủ relationship
from app.models import user, child, emotion

from app.seeds.seed_emotion_flashcards import seed_emotion_flashcards


def run_seed():
    db = SessionLocal()

    try:
        seed_emotion_flashcards(db)

    finally:
        db.close()


if __name__ == "__main__":
    run_seed()