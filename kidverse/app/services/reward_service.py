from sqlalchemy.orm import Session
from app.models.user import User
from app.models.activity import Activity
from datetime import datetime

LEVEL_THRESHOLDS = [0, 50, 150, 300, 500, 750, 1000, 1500, 2000, 3000]

POINTS_MAP = {
    "chat": 5,
    "story": 15,
    "drawing": 10,
    "login": 2,
}


def compute_level(points: int) -> int:
    level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if points >= threshold:
            level = i + 1
    return min(level, len(LEVEL_THRESHOLDS))


def award_points(db: Session, user_id: int, activity_type: str, content: str = "") -> int:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return 0

    pts = POINTS_MAP.get(activity_type, 5)

    user.points += pts
    user.level = compute_level(user.points)

    activity = Activity(
        user_id=user_id,
        activity_type=activity_type,
        content=content[:200] if content else "",
        points_earned=pts,
        timestamp=datetime.utcnow(),
    )
    db.add(activity)
    db.commit()
    db.refresh(user)

    return pts


def get_user_stats(db: Session, user_id: int) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {}

    next_level_pts = LEVEL_THRESHOLDS[min(user.level, len(LEVEL_THRESHOLDS) - 1)]
    prev_level_pts = LEVEL_THRESHOLDS[user.level - 1]
    progress = 0
    if next_level_pts > prev_level_pts:
        progress = int(
            (user.points - prev_level_pts) / (next_level_pts - prev_level_pts) * 100
        )

    activities = (
        db.query(Activity)
        .filter(Activity.user_id == user_id)
        .order_by(Activity.timestamp.desc())
        .limit(10)
        .all()
    )

    return {
        "user": user,
        "next_level_points": next_level_pts,
        "level_progress": min(progress, 100),
        "recent_activities": activities,
    }
