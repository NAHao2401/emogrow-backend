from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import os

from app.api.auth import router as auth_router
from app.api.children import router as children_router
from app.api.journal import router as journal_router
from app.api.upload import router as upload_router
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


Base.metadata.create_all(bind=engine)


def _seed_default_emotions():
    db = SessionLocal()
    try:
        from app.models.emotion import Emotion

        count = db.query(Emotion).count()
        if count == 0:
            defaults = [
                {"name": "Vui vẻ", "emoji": "😊", "color_code": "#FFD54F", "description": "Cảm xúc khi trẻ cảm thấy hạnh phúc, thoải mái và muốn cười."},
                {"name": "Buồn", "emoji": "😢", "color_code": "#64B5F6", "description": "Cảm xúc khi trẻ cảm thấy không vui, thất vọng hoặc mất mát."},
                {"name": "Tức giận", "emoji": "😡", "color_code": "#EF5350", "description": "Cảm xúc khi trẻ cảm thấy khó chịu, bực bội hoặc không hài lòng."},
                {"name": "Sợ hãi", "emoji": "😨", "color_code": "#9575CD", "description": "Cảm xúc khi trẻ cảm thấy lo lắng, bất an hoặc sợ một điều gì đó."},
                {"name": "Ngạc nhiên", "emoji": "😮", "color_code": "#FFB74D", "description": "Cảm xúc khi trẻ gặp điều bất ngờ hoặc chưa từng nghĩ tới."},
                {"name": "Lo lắng", "emoji": "😟", "color_code": "#4DB6AC", "description": "Cảm xúc khi trẻ cảm thấy bồn chồn, hồi hộp hoặc không yên tâm."},
                {"name": "Xấu hổ", "emoji": "😳", "color_code": "#F48FB1", "description": "Cảm xúc khi trẻ cảm thấy ngại ngùng, lúng túng hoặc mắc cỡ."},
                {"name": "Tự hào", "emoji": "😊", "color_code": "#81C784", "description": "Cảm xúc khi trẻ cảm thấy vui vì đã làm được điều tốt hoặc đạt thành quả."},
                {"name": "Yêu thương", "emoji": "🥰", "color_code": "#F06292", "description": "Cảm xúc khi trẻ cảm thấy được quan tâm, gần gũi hoặc muốn thể hiện tình cảm."},
                {"name": "Bình tĩnh", "emoji": "😌", "color_code": "#90CAF9", "description": "Cảm xúc khi trẻ cảm thấy thoải mái, nhẹ nhàng và không căng thẳng."},
                {"name": "Mệt mỏi", "emoji": "😴", "color_code": "#B0BEC5", "description": "Cảm xúc khi trẻ cảm thấy thiếu năng lượng, buồn ngủ hoặc cần nghỉ ngơi."},
                {"name": "Cô đơn", "emoji": "🥺", "color_code": "#A1887F", "description": "Cảm xúc khi trẻ cảm thấy một mình, thiếu sự chia sẻ hoặc cần được quan tâm."},
                {"name": "Bối rối", "emoji": "😕", "color_code": "#CE93D8", "description": "Cảm xúc khi trẻ chưa hiểu rõ điều gì đó hoặc không biết nên làm gì."},
                {"name": "Ghen tị", "emoji": "😒", "color_code": "#AED581", "description": "Cảm xúc khi trẻ cảm thấy không vui vì người khác có điều mình mong muốn."},
                {"name": "Hào hứng", "emoji": "🤩", "color_code": "#FF8A65", "description": "Cảm xúc khi trẻ cảm thấy rất vui, mong chờ hoặc thích thú với điều gì đó."},
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
        "ALTER TABLE emotion_diaries ADD COLUMN IF NOT EXISTS voice_url VARCHAR(255);",
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
app.include_router(upload_router)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root():
    return {"message": "EMOGROW Backend is running"}