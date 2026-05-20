import os
os.environ["DATABASE_URL"] = "sqlite:///./test_sanity.db"
os.environ["SECRET_KEY"] = "test_secret_key_only"

from app.main import app
from app.models.review import EmotionLog, StickerCollection, ChildReadBook
from app.schemas.review import (
    EmotionLogCreateRequest, EmotionLogResponse,
    ProgressResponse, BookReadResponse
)

def test_routes():
    paths = [r.path for r in app.routes]
    checks = [
        "/review/children/{child_id}/emotion-statistics",
        "/review/children/{child_id}/logs",
        "/review/children/{child_id}/stickers",
        "/review/children/{child_id}/books/{book_id}/read",
        "/review/children/{child_id}/progress",
    ]
    for c in checks:
        assert c in paths, f"Missing: {c}"
    print("[OK] All routes registered")

def test_models():
    assert EmotionLog.__tablename__ == "emotion_logs"
    assert StickerCollection.__tablename__ == "sticker_collections"
    assert ChildReadBook.__tablename__ == "child_read_books"
    assert hasattr(EmotionLog, "source"), "EmotionLog missing source"
    assert hasattr(EmotionLog, "note"), "EmotionLog missing note"
    print("[OK] All models OK")

def test_schemas():
    r = EmotionLogCreateRequest(
        child_id=1, emotion_type="happy",
        intensity=5, note="test note", source="lesson"
    )
    assert r.source == "lesson"
    assert r.note == "test note"

    p = ProgressResponse(read_book_ids=["1","2"], unlocked_sticker_ids=["stk_1"])
    assert len(p.read_book_ids) == 2
    assert len(p.unlocked_sticker_ids) == 1
    print("[OK] Schemas OK")

if __name__ == "__main__":
    test_routes()
    test_models()
    test_schemas()
    print("\n[OK] All sanity checks passed")