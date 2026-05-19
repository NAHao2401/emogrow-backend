from app.db.base import Base
from app.db.session import SessionLocal, engine

# Import model để SQLAlchemy đăng ký đầy đủ relationship
from app.models import user, child, emotion, review

from app.seeds.seed_emotion_flashcards import seed_emotion_flashcards


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        seed_emotion_flashcards(db)

    finally:
        db.close()


if __name__ == "__main__":
    run_seed()