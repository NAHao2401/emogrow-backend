from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.emotion import (
    EmotionCreateRequest,
    EmotionUpdateRequest,
    EmotionResponse,
    EmotionFlashcardCreateRequest,
    EmotionFlashcardUpdateRequest,
    EmotionFlashcardResponse,
    ChildFlashcardProgressResponse,
    FlashcardInteractionRequest,
    ChildFlashcardLearningResponse
)
from app.services.emotion_service import (
    create_emotion,
    get_all_emotions,
    update_emotion,
    delete_emotion,
    create_flashcard,
    get_all_flashcards,
    get_flashcards_by_emotion,
    update_flashcard,
    delete_flashcard,
    view_flashcard,
    flip_flashcard,
    view_flashcard_explanation,
    complete_flashcard,
    get_child_flashcard_progress
)

router = APIRouter(prefix="/emotions", tags=["Emotions"])


@router.post("", response_model=EmotionResponse)
def create_new_emotion(
    data: EmotionCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_emotion(data, db, current_user)


@router.get("", response_model=List[EmotionResponse])
def get_emotions(
    db: Session = Depends(get_db)
):
    return get_all_emotions(db)


@router.put("/{emotion_id}", response_model=EmotionResponse)
def update_existing_emotion(
    emotion_id: int,
    data: EmotionUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_emotion(emotion_id, data, db, current_user)


@router.delete("/{emotion_id}", response_model=MessageResponse)
def delete_existing_emotion(
    emotion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_emotion(emotion_id, db, current_user)


@router.post("/flashcards", response_model=EmotionFlashcardResponse)
def create_new_flashcard(
    data: EmotionFlashcardCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_flashcard(data, db, current_user)


@router.get("/flashcards", response_model=List[EmotionFlashcardResponse])
def get_flashcards(
    db: Session = Depends(get_db)
):
    return get_all_flashcards(db)


@router.get("/{emotion_id}/flashcards", response_model=List[EmotionFlashcardResponse])
def get_flashcards_of_emotion(
    emotion_id: int,
    db: Session = Depends(get_db)
):
    return get_flashcards_by_emotion(emotion_id, db)


@router.put("/flashcards/{flashcard_id}", response_model=EmotionFlashcardResponse)
def update_existing_flashcard(
    flashcard_id: int,
    data: EmotionFlashcardUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_flashcard(flashcard_id, data, db, current_user)


@router.delete("/flashcards/{flashcard_id}", response_model=MessageResponse)
def delete_existing_flashcard(
    flashcard_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_flashcard(flashcard_id, db, current_user)


@router.post("/flashcards/view", response_model=ChildFlashcardLearningResponse)
def view_emotion_flashcard(
    data: FlashcardInteractionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return view_flashcard(data.child_id, data.flashcard_id, db, current_user)


@router.post("/flashcards/flip", response_model=ChildFlashcardProgressResponse)
def flip_emotion_flashcard(
    data: FlashcardInteractionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return flip_flashcard(data.child_id, data.flashcard_id, db, current_user)


@router.post("/flashcards/explanation", response_model=ChildFlashcardProgressResponse)
def view_emotion_flashcard_explanation(
    data: FlashcardInteractionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return view_flashcard_explanation(
        data.child_id,
        data.flashcard_id,
        db,
        current_user
    )


@router.post("/flashcards/complete", response_model=ChildFlashcardProgressResponse)
def complete_emotion_flashcard(
    data: FlashcardInteractionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return complete_flashcard(data.child_id, data.flashcard_id, db, current_user)


@router.get(
    "/children/{child_id}/progress",
    response_model=List[ChildFlashcardProgressResponse]
)
def get_child_progress(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_child_flashcard_progress(child_id, db, current_user)