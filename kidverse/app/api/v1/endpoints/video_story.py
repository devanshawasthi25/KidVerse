from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import VideoAnswerRequest, VideoAnswerResponse
from app.services.video_service import list_stories, get_story_detail, check_video_answer
from app.services.reward_service import award_points
from app.models.user import User

router = APIRouter(prefix="/video-story", tags=["video-story"])


@router.get("/list")
def get_video_stories(
    age_group: str = Query(default="creator"),
    user_id: int = Query(default=0),
    db: Session = Depends(get_db),
):
    """Get available video stories for user's age group."""
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            age_group = user.age_group
    return {"stories": list_stories(age_group)}


@router.get("/{story_id}")
def get_video_story(story_id: str):
    """Get full video story details with checkpoints."""
    story = get_story_detail(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.post("/answer", response_model=VideoAnswerResponse)
def submit_video_answer(payload: VideoAnswerRequest, db: Session = Depends(get_db)):
    """Submit answer for a video checkpoint."""
    result = check_video_answer(payload.story_id, payload.checkpoint_idx, payload.answer)

    if result["correct"] and payload.user_id:
        pts = award_points(
            db, payload.user_id, "story",
            f"video-checkpoint:{payload.story_id}:{payload.checkpoint_idx}"
        )
        result["points_earned"] = pts

    return VideoAnswerResponse(
        correct=result["correct"],
        feedback=result["feedback"],
        points_earned=result["points_earned"],
        correct_answer=result["correct_answer"],
    )


@router.post("/complete")
def complete_video_story(
    story_id: str,
    user_id: int = Query(default=0),
    db: Session = Depends(get_db),
):
    """Mark a video story as completed and award bonus points."""
    story = get_story_detail(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    bonus = 0
    if user_id:
        bonus = award_points(db, user_id, "story", f"video-complete:{story_id}")

    return {
        "message": f"🎉 You completed '{story['title']}'!",
        "bonus_points": bonus,
    }
