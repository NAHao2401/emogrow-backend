from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.emotion import Emotion, EmotionFlashcard, ChildFlashcardProgress
from app.models.child import Child
from app.models.user import User
from app.schemas.emotion import FlashcardInteractionRequest
from datetime import datetime, timezone

def get_emotions(db: Session):
    return db.query(Emotion).all()

def get_flashcards(db: Session):
    return db.query(EmotionFlashcard).filter(EmotionFlashcard.is_active == True).all()

def get_flashcards_by_emotion(emotion_id: int, db: Session):
    return db.query(EmotionFlashcard).filter(
        EmotionFlashcard.emotion_id == emotion_id,
        EmotionFlashcard.is_active == True
    ).all()

def _get_or_create_progress(db: Session, child_id: int, flashcard_id: int, current_user: User):
    # Verify child belongs to user
    child = db.query(Child).filter(Child.child_id == child_id, Child.user_id == current_user.user_id).first()
    if not child:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Child not found or unauthorized")
        
    flashcard = db.query(EmotionFlashcard).filter(EmotionFlashcard.flashcard_id == flashcard_id).first()
    if not flashcard:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard not found")

    progress = db.query(ChildFlashcardProgress).filter(
        ChildFlashcardProgress.child_id == child_id,
        ChildFlashcardProgress.flashcard_id == flashcard_id
    ).first()

    if not progress:
        progress = ChildFlashcardProgress(
            child_id=child_id,
            flashcard_id=flashcard_id
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)

    return progress, flashcard

def view_flashcard(data: FlashcardInteractionRequest, db: Session, current_user: User):
    progress, flashcard = _get_or_create_progress(db, data.child_id, data.flashcard_id, current_user)
    
    progress.viewed_count += 1
    progress.last_viewed_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(progress)
    
    return {"flashcard": flashcard, "progress": progress}

def flip_flashcard(data: FlashcardInteractionRequest, db: Session, current_user: User):
    progress, flashcard = _get_or_create_progress(db, data.child_id, data.flashcard_id, current_user)
    
    progress.flip_count += 1
    progress.last_viewed_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(progress)
    
    return progress

def view_explanation(data: FlashcardInteractionRequest, db: Session, current_user: User):
    progress, flashcard = _get_or_create_progress(db, data.child_id, data.flashcard_id, current_user)
    
    progress.explanation_viewed_count += 1
    progress.last_viewed_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(progress)
    
    return progress

def complete_flashcard(data: FlashcardInteractionRequest, db: Session, current_user: User):
    progress, flashcard = _get_or_create_progress(db, data.child_id, data.flashcard_id, current_user)
    
    if not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = datetime.now(timezone.utc)
        
    progress.last_viewed_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(progress)
    
    return progress

def get_child_progress(child_id: int, db: Session, current_user: User):
    # Verify child belongs to user
    child = db.query(Child).filter(Child.child_id == child_id, Child.user_id == current_user.user_id).first()
    if not child:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Child not found or unauthorized")
        
    return db.query(ChildFlashcardProgress).filter(ChildFlashcardProgress.child_id == child_id).all()
