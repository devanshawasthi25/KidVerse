from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import GameQuestionResponse, GameAnswerRequest, GameAnswerResponse
from app.services.game_service import get_question, check_answer
from app.services.reward_service import award_points
from app.models.user import User

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/question", response_model=GameQuestionResponse)
def get_game_question(
    age_group: str = Query(default="creator"),
    user_id: int = Query(default=0),
    db: Session = Depends(get_db),
):
    """Get a random age-appropriate game question."""
    # Resolve age group from user if logged in
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            age_group = user.age_group

    q = get_question(age_group, user_id)
    # Don't send correct_answer to client
    return GameQuestionResponse(
        question_id=q["question_id"],
        question_text=q["question_text"],
        question_type=q["question_type"],
        options=q["options"],
        emoji_hint=q.get("emoji_hint"),
        difficulty=q.get("difficulty", "easy"),
        age_group=age_group,
    )


@router.post("/answer", response_model=GameAnswerResponse)
def submit_answer(payload: GameAnswerRequest, db: Session = Depends(get_db)):
    """Submit an answer and get feedback + points."""
    # Resolve age group
    age_group = payload.age_group
    if payload.user_id:
        user = db.query(User).filter(User.id == payload.user_id).first()
        if user:
            age_group = user.age_group

    result = check_answer(age_group, payload.question_id, payload.answer)

    # Award points if correct and user is logged in
    if result["correct"] and payload.user_id:
        pts = award_points(db, payload.user_id, "chat", f"game-correct:{payload.question_id}")
        result["points_earned"] = pts

    return GameAnswerResponse(
        correct=result["correct"],
        feedback=result["feedback"],
        points_earned=result["points_earned"],
        correct_answer=result["correct_answer"],
    )


@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    """Top 10 players by points."""
    users = db.query(User).order_by(User.points.desc()).limit(10).all()
    return {
        "leaderboard": [
            {
                "rank": i + 1,
                "name": u.name,
                "avatar": u.avatar,
                "points": u.points,
                "level": u.level,
                "age_group": u.age_group,
            }
            for i, u in enumerate(users)
        ]
    }
