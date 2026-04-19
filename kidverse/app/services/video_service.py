"""Video story service — retrieves stories and checks checkpoint answers."""

from app.services.video_story_data import get_stories_by_age, get_story_by_id, get_all_stories
import random


def list_stories(age_group: str = "creator") -> list[dict]:
    """Get all stories for an age group (without full checkpoint data)."""
    stories = get_stories_by_age(age_group)
    return [
        {
            "id":          s["id"],
            "title":       s["title"],
            "description": s["description"],
            "thumbnail":   s["thumbnail"],
            "video_url":   s["video_url"],
            "duration":    s["duration"],
            "age_group":   s["age_group"],
            "total_points": s["total_points"],
            "checkpoint_count": len(s["checkpoints"]),
        }
        for s in stories
    ]


def get_story_detail(story_id: str) -> dict | None:
    """Get full story with checkpoints."""
    story = get_story_by_id(story_id)
    if not story:
        return None
    return story


def check_video_answer(story_id: str, checkpoint_idx: int, answer: str) -> dict:
    """Check answer for a video story checkpoint."""
    story = get_story_by_id(story_id)
    if not story:
        return {"correct": False, "feedback": "Story not found!", "correct_answer": ""}

    if checkpoint_idx < 0 or checkpoint_idx >= len(story["checkpoints"]):
        return {"correct": False, "feedback": "Invalid checkpoint!", "correct_answer": ""}

    cp = story["checkpoints"][checkpoint_idx]
    correct_answer = cp["correct_answer"]

    # For open_ended, check if answer contains any accepted keywords
    if cp["question_type"] == "open_ended":
        accepted = [a.strip().lower() for a in correct_answer.split(",")]
        is_correct = any(keyword in answer.strip().lower() for keyword in accepted)
    else:
        is_correct = answer.strip() == correct_answer.strip()

    age_group = story["age_group"]

    if is_correct:
        feedbacks = {
            "toddler": random.choice(["🎉 YAY! You're so smart!", "⭐ WOW! Amazing!", "🌟 GREAT JOB!"]),
            "explorer": random.choice([
                "🎉 Awesome! You really know your stuff!",
                "⭐ Correct! The video continues...",
                "🌟 Great answer! Keep watching!",
            ]),
            "creator": random.choice([
                "🎉 Excellent work! Great critical thinking!",
                "⭐ Spot on! Your knowledge is impressive!",
                "🌟 Perfect! Keep going, you're doing great!",
            ]),
        }
    else:
        feedbacks = {
            "toddler": "Almost! The answer is " + correct_answer + "! 🌈 Try the next one!",
            "explorer": f"Not quite! It's {correct_answer}. Let's keep watching and learning! 📚",
            "creator": f"Good try! The answer is {correct_answer}. Remember this for next time! 💪",
        }

    points = 5 if is_correct else 0

    return {
        "correct":        is_correct,
        "feedback":       feedbacks.get(age_group, feedbacks["creator"]),
        "points_earned":  points,
        "correct_answer": correct_answer,
    }
