from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas import UserCreate, UserOut
from app.services.reward_service import get_user_stats, award_points

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(
        name      = payload.name,
        avatar    = payload.avatar or "star",
        age_group = payload.age_group or "creator",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    award_points(db, user.id, "login", "account created")
    db.refresh(user)
    return user


@router.patch("/{user_id}/age-group", response_model=UserOut)
def update_age_group(user_id: int, age_group: str, db: Session = Depends(get_db)):
    """Switch a user's mode at any time."""
    if age_group not in ("toddler", "explorer", "creator"):
        raise HTTPException(status_code=400, detail="Invalid age_group. Use: toddler, explorer, creator")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.age_group = age_group
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}/stats")
def user_stats(user_id: int, db: Session = Depends(get_db)):
    stats = get_user_stats(db, user_id)
    if not stats:
        raise HTTPException(status_code=404, detail="User not found")
    user = stats["user"]
    return {
        "id":               user.id,
        "name":             user.name,
        "avatar":           user.avatar,
        "age_group":        user.age_group,
        "points":           user.points,
        "level":            user.level,
        "next_level_points": stats["next_level_points"],
        "level_progress":   stats["level_progress"],
        "recent_activities": [
            {"type": a.activity_type, "content": a.content,
             "points": a.points_earned, "timestamp": a.timestamp.isoformat()}
            for a in stats["recent_activities"]
        ],
    }