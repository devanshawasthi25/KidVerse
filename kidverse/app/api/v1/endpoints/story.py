from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import StoryRequest, StoryResponse
from app.services.ai_service import call_ai, get_story_prompt, get_story_max_tokens
from app.services.reward_service import award_points
from app.models.user import User

router = APIRouter(prefix="/story", tags=["story"])


def _resolve_age_group(request: StoryRequest, db: Session) -> str:
    if request.user_id:
        user = db.query(User).filter(User.id == request.user_id).first()
        if user:
            return user.age_group
    return request.age_group


@router.post("/create", response_model=StoryResponse)
async def create_story(request: StoryRequest, db: Session = Depends(get_db)):
    if not request.theme.strip() or not request.character.strip():
        return StoryResponse(title="Oops!", story="Please give me a theme and a character! 🌟", points_earned=0)

    age_group  = _resolve_age_group(request, db)
    system     = get_story_prompt(age_group)
    max_tokens = get_story_max_tokens(age_group)

    # Build age-appropriate prompt
    if age_group == "toddler":
        prompt = f"Write a tiny 3-sentence bedtime story about a {request.character} who loves {request.theme}."
    elif age_group == "explorer":
        prompt = (f"Write a fun short story for a 7-year-old. "
                  f"Main character: {request.character}. Theme: {request.theme}. Keep it simple and exciting!")
    else:
        prompt = (f"Write a short story for children with this theme: '{request.theme}'. "
                  f"The main character is: {request.character}. Make it fun, imaginative, and age-appropriate!")

    raw = await call_ai(user_message=prompt, system_prompt=system,
                        max_tokens=max_tokens, age_group=age_group)

    # Parse title
    title      = f"The Adventure of {request.character.title()}"
    story_text = raw
    if raw.startswith("TITLE:"):
        lines = raw.split("\n", 2)
        if len(lines) >= 2:
            title      = lines[0].replace("TITLE:", "").strip()
            story_text = "\n".join(lines[1:]).strip()

    points_earned = 0
    if request.user_id:
        points_earned = award_points(db, request.user_id, "story", f"Theme: {request.theme}")

    return StoryResponse(title=title, story=story_text, points_earned=points_earned, mode=age_group)