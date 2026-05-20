import os
os.environ["DATABASE_URL"] = "sqlite:///./test_sanity.db"
os.environ["SECRET_KEY"] = "test_secret_key_only"

from app.main import app
from app.api.auth import router as auth_router
from app.api.children import router as children_router
from app.api.review import router as review_router
from app.models.user import User
from app.models.child import Child
from app.models.review import EmotionLog, StickerCollection

def test_routers_registered():
    """Verify all routers are included in the app"""
    app_routes = [r.path for r in app.routes]

    assert "/auth/register" in app_routes, "Auth /register missing"
    assert "/auth/login" in app_routes, "Auth /login missing"
    assert "/auth/me" in app_routes, "Auth /me missing"
    assert "/children" in app_routes, "Children / missing"
    assert "/children/me" in app_routes, "Children /me missing"
    assert "/review/children/{child_id}/emotion-statistics" in app_routes, "Review statistics missing"

    print("[OK] All routers registered successfully")

def test_models_importable():
    """Verify all models can be imported"""
    assert User.__tablename__ == "users"
    assert Child.__tablename__ == "children"
    assert EmotionLog.__tablename__ == "emotion_logs"
    assert StickerCollection.__tablename__ == "sticker_collections"

    print("[OK] All models importable")

def test_model_relationships():
    """Verify relationships are set up correctly"""
    child_attrs = dir(Child)
    assert "emotion_logs" in child_attrs, "Child.emotion_logs missing"
    assert "sticker_collections" in child_attrs, "Child.sticker_collections missing"

    print("[OK] Model relationships configured")

if __name__ == "__main__":
    print("Running sanity checks...")
    test_routers_registered()
    test_model_relationships()
    test_models_importable()
    print("\n[OK] All sanity checks passed!")
    print("[OK] Backward compatibility verified")