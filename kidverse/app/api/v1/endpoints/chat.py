from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import ChatRequest, ChatResponse
from app.services.ai_service import call_ai, SYSTEM_PROMPTS, get_random_play
from app.services.reward_service import award_points
from app.models.user import User

router = APIRouter(prefix="/chat", tags=["chat"])


def _resolve_age_group(request: ChatRequest, db: Session) -> str:
    """Get age_group from request or from user record in DB."""
    if request.user_id:
        user = db.query(User).filter(User.id == request.user_id).first()
        if user:
            return user.age_group
    return request.age_group


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    age_group = _resolve_age_group(request, db)

    # ── Toddler: no chat, return playful card as text ──────────────────────
    if age_group == "toddler":
        card = get_random_play()
        reply = f"{card['emoji']} {card['name'].title()}! {card['name'].title()} says {card['sound']}! {card['emoji']}"
        points_earned = 0
        if request.user_id:
            points_earned = award_points(db, request.user_id, "chat", "toddler-play")
        return ChatResponse(reply=reply, points_earned=points_earned, mode="toddler")

    # ── Explorer: simplified AI ────────────────────────────────────────────
    if age_group == "explorer":
        reply = await call_ai(
            user_message=request.message,
            system_prompt=SYSTEM_PROMPTS["explorer"],
            max_tokens=200,
            age_group="explorer",
        )
        points_earned = 0
        if request.user_id:
            points_earned = award_points(db, request.user_id, "chat", request.message[:100])
        return ChatResponse(reply=reply, points_earned=points_earned, mode="explorer")

    # ── Creator: full AI ───────────────────────────────────────────────────
    reply = await call_ai(
        user_message=request.message,
        system_prompt=SYSTEM_PROMPTS["creator"],
        max_tokens=300,
        age_group="creator",
    )
    points_earned = 0
    if request.user_id:
        points_earned = award_points(db, request.user_id, "chat", request.message[:100])
    return ChatResponse(reply=reply, points_earned=points_earned, mode="creator")