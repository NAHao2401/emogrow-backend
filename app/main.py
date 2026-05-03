from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.api.auth import router as auth_router
from app.api.children import router as children_router
from app.api.journal import router as journal_router
from app.core.exceptions import AppException
from app.core.error_handler import (
    app_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)
from app.db.base import Base
from app.db.session import engine, SessionLocal
from sqlalchemy import text
import logging

# import models so they are registered with SQLAlchemy metadata
from app.models import user, child
import app.models.emotion
import app.models.emotion_diary
import app.models.emotion_jar
import app.models.emotion_jar_item
import app.models.knowledge_bookshelf_item


Base.metadata.create_all(bind=engine)


def _seed_default_emotions():
    db = SessionLocal()
    try:
        from app.models.emotion import Emotion

        count = db.query(Emotion).count()
        if count == 0:
            defaults = [
                {"name": "Vui", "emoji": "😊", "color_code": "#FFD700", "description": "Cảm xúc vui vẻ"},
                {"name": "Buồn", "emoji": "😢", "color_code": "#1E90FF", "description": "Cảm xúc buồn"},
                {"name": "Sợ", "emoji": "😨", "color_code": "#800080", "description": "Cảm xúc sợ hãi"},
                {"name": "Tức", "emoji": "😡", "color_code": "#FF4500", "description": "Cảm xúc tức giận"},
                {"name": "Lo", "emoji": "😟", "color_code": "#FFA500", "description": "Cảm xúc lo lắng"},
            ]

            for e in defaults:
                emo = Emotion(
                    name=e["name"],
                    emoji=e["emoji"],
                    color_code=e["color_code"],
                    description=e["description"],
                )
                db.add(emo)

            db.commit()
    finally:
        db.close()


_seed_default_emotions()


def _migrate_emotion_diaries_table():
    """Ensure emotion_diaries table has columns for emotion_name and emotion_emoji
    and that emotion_id is nullable. This helps older DBs created before model
    changes to continue working without manual migrations.
    """
    statements = [
        "ALTER TABLE emotion_diaries ADD COLUMN IF NOT EXISTS emotion_name VARCHAR(100);",
        "ALTER TABLE emotion_diaries ADD COLUMN IF NOT EXISTS emotion_emoji VARCHAR(10);",
        "ALTER TABLE emotion_diaries ADD COLUMN IF NOT EXISTS emotion_color VARCHAR(20);",
        # Drop NOT NULL constraint on emotion_id if it exists
        ("DO $$ BEGIN\n"
         "IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='emotion_diaries' AND column_name='emotion_id') THEN\n"
         "    BEGIN\n"
         "        ALTER TABLE emotion_diaries ALTER COLUMN emotion_id DROP NOT NULL;\n"
         "    EXCEPTION WHEN undefined_column THEN NULL; END;\n"
         "END IF;\n"
         "END$$;")
    ]

    try:
        with engine.begin() as conn:
            for stmt in statements:
                try:
                    conn.execute(text(stmt))
                except Exception as e:
                    # Log and continue; don't let migration failure break startup
                    logging.warning("Migration statement failed: %s; error: %s", stmt, e)
    except Exception as e:
        logging.exception("Failed to run migrations for emotion_diaries: %s", e)


_migrate_emotion_diaries_table()

app = FastAPI(title="EMOGROW Backend API")

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(auth_router)
app.include_router(children_router)
app.include_router(journal_router)


@app.get("/")
def root():
    return {"message": "EMOGROW Backend is running"}