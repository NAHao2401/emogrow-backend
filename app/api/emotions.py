from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.emotion import (
    EmotionResponse,
    EmotionFlashcardResponse,
    FlashcardInteractionRequest,
    ChildFlashcardLearningResponse,
    ChildFlashcardProgressResponse
)
from app.services.emotion_service import (
    get_emotions,
    get_flashcards,
    get_flashcards_by_emotion,
    view_flashcard,
    flip_flashcard,
    view_explanation,
    complete_flashcard,
    get_child_progress
)

router = APIRouter(prefix="/emotions", tags=["Emotions"])

@router.get("", response_model=List[EmotionResponse])
def read_emotions(db: Session = Depends(get_db)):
    return get_emotions(db)

@router.get("/flashcards", response_model=List[EmotionFlashcardResponse])
def read_flashcards(db: Session = Depends(get_db)):
    return get_flashcards(db)

@router.get("/{emotion_id}/flashcards", response_model=List[EmotionFlashcardResponse])
def read_flashcards_by_emotion(emotion_id: int, db: Session = Depends(get_db)):
    return get_flashcards_by_emotion(emotion_id, db)

@router.post("/flashcards/view", response_model=ChildFlashcardLearningResponse)
def handle_view_flashcard(
    data: FlashcardInteractionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return view_flashcard(data, db, current_user)

@router.post("/flashcards/flip", response_model=ChildFlashcardProgressResponse)
def handle_flip_flashcard(
    data: FlashcardInteractionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return flip_flashcard(data, db, current_user)

@router.post("/flashcards/explanation", response_model=ChildFlashcardProgressResponse)
def handle_view_explanation(
    data: FlashcardInteractionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return view_explanation(data, db, current_user)

@router.post("/flashcards/complete", response_model=ChildFlashcardProgressResponse)
def handle_complete_flashcard(
    data: FlashcardInteractionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return complete_flashcard(data, db, current_user)

@router.get("/children/{child_id}/progress", response_model=List[ChildFlashcardProgressResponse])
def read_child_progress(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_child_progress(child_id, db, current_user)
