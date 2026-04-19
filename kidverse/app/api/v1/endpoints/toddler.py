from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.schemas import PlayResponse
from app.services.ai_service import get_random_play
from app.db.session import get_db
from app.services.reward_service import award_points

router = APIRouter(prefix="/toddler", tags=["toddler"])


class StarsRequest(BaseModel):
    user_id: int
    stars: int = 1


@router.get("/play", response_model=PlayResponse)
def toddler_play():
    """Random playful interaction card for toddlers."""
    return PlayResponse(**get_random_play())


@router.get("/play/{count}")
def toddler_play_batch(count: int = 3):
    """Multiple play cards at once (max 6)."""
    count = min(count, 6)
    return {"cards": [get_random_play() for _ in range(count)]}


@router.post("/stars")
def award_toddler_stars(payload: StarsRequest, db: Session = Depends(get_db)):
    """Award stars earned in toddler hub mini-games."""
    pts = award_points(
        db, payload.user_id, "chat",
        f"toddler-hub-stars:{payload.stars}"
    )
    return {"ok": True, "points_earned": pts}