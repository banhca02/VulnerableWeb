from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud import quiz as crud_quiz
from app.schemas.quiz import QuizCreate, QuizOut
from app.deps.deps import get_db


router = APIRouter()


@router.get("/doquiz/{classID}/{name}", response_model=QuizOut)
def load_quiz(classID: int,name: str, db: Session = Depends(get_db)):
    result = crud_quiz.get_quiz_by_name(db, classID, name)
    if result is None:
        # Ném ra lỗi HTTP 404 với thông báo chi tiết
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return result

