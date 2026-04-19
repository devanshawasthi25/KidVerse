"""
AI-powered game question generator and answer evaluator.
Generates age-appropriate learning questions for all three age groups.
"""

import random
import uuid
from typing import Optional

from app.services.ai_service import call_ai

# ── Pre-built Question Banks (fallback when AI unavailable) ───────────────────

TODDLER_QUESTIONS = [
    {
        "question_text": "Which animal says 'MOO'? 🐄",
        "question_type": "audio_visual",
        "options": ["🐄 Cow", "🐱 Cat", "🐶 Dog"],
        "correct": "🐄 Cow",
        "emoji_hint": "🐄",
        "audio_cue": "Moooooo!",
    },
    {
        "question_text": "What color is the sun? ☀️",
        "question_type": "audio_visual",
        "options": ["🟡 Yellow", "🔵 Blue", "🔴 Red"],
        "correct": "🟡 Yellow",
        "emoji_hint": "☀️",
        "audio_cue": "Look up! The sun is bright!",
    },
    {
        "question_text": "Which one is a CIRCLE? ⭕",
        "question_type": "audio_visual",
        "options": ["⭕ Circle", "⬛ Square", "🔺 Triangle"],
        "correct": "⭕ Circle",
        "emoji_hint": "⭕",
        "audio_cue": "Round and round! It's a circle!",
    },
    {
        "question_text": "What sound does a duck make? 🦆",
        "question_type": "audio_visual",
        "options": ["🦆 Quack", "🐶 Woof", "🐱 Meow"],
        "correct": "🦆 Quack",
        "emoji_hint": "🦆",
        "audio_cue": "Quack quack quack!",
    },
    {
        "question_text": "How many eyes do you have? 👀",
        "question_type": "audio_visual",
        "options": ["✌️ Two", "☝️ One", "🤟 Three"],
        "correct": "✌️ Two",
        "emoji_hint": "👀",
        "audio_cue": "Let's count! One... Two!",
    },
    {
        "question_text": "Which fruit is RED? 🍎",
        "question_type": "audio_visual",
        "options": ["🍎 Apple", "🍌 Banana", "🍊 Orange"],
        "correct": "🍎 Apple",
        "emoji_hint": "🍎",
        "audio_cue": "Yummy! Red and crunchy!",
    },
    {
        "question_text": "Which animal has a long trunk? 🐘",
        "question_type": "audio_visual",
        "options": ["🐘 Elephant", "🐰 Bunny", "🐸 Frog"],
        "correct": "🐘 Elephant",
        "emoji_hint": "🐘",
        "audio_cue": "It's big and grey with a looong trunk!",
    },
    {
        "question_text": "What shape is a star? ⭐",
        "question_type": "audio_visual",
        "options": ["⭐ Star", "🔵 Circle", "⬛ Square"],
        "correct": "⭐ Star",
        "emoji_hint": "⭐",
        "audio_cue": "Twinkle twinkle! It has pointy ends!",
    },
]

EXPLORER_QUESTIONS = [
    {
        "question_text": "What planet do we live on?",
        "question_type": "mcq",
        "options": ["🌍 Earth", "🔴 Mars", "🪐 Saturn", "🌙 Moon"],
        "correct": "🌍 Earth",
        "emoji_hint": "🌍",
    },
    {
        "question_text": "How many legs does a spider have?",
        "question_type": "mcq",
        "options": ["8 legs", "6 legs", "4 legs", "10 legs"],
        "correct": "8 legs",
        "emoji_hint": "🕷️",
    },
    {
        "question_text": "What is 7 + 5?",
        "question_type": "mcq",
        "options": ["12", "11", "13", "10"],
        "correct": "12",
        "emoji_hint": "🔢",
    },
    {
        "question_text": "Which animal is known as the 'King of the Jungle'?",
        "question_type": "mcq",
        "options": ["🦁 Lion", "🐘 Elephant", "🐯 Tiger", "🐻 Bear"],
        "correct": "🦁 Lion",
        "emoji_hint": "🦁",
    },
    {
        "question_text": "What do plants need to grow?",
        "question_type": "mcq",
        "options": ["☀️ Sunlight & Water", "🍕 Pizza", "📺 TV", "🎮 Video Games"],
        "correct": "☀️ Sunlight & Water",
        "emoji_hint": "🌱",
    },
    {
        "question_text": "What is the largest ocean on Earth?",
        "question_type": "mcq",
        "options": ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"],
        "correct": "Pacific Ocean",
        "emoji_hint": "🌊",
    },
    {
        "question_text": "Fill in the blank: The opposite of HOT is ___?",
        "question_type": "mcq",
        "options": ["Cold", "Warm", "Big", "Fast"],
        "correct": "Cold",
        "emoji_hint": "🧊",
    },
    {
        "question_text": "Which season comes after summer?",
        "question_type": "mcq",
        "options": ["🍂 Autumn/Fall", "❄️ Winter", "🌸 Spring", "☀️ Summer"],
        "correct": "🍂 Autumn/Fall",
        "emoji_hint": "🍂",
    },
]

CREATOR_QUESTIONS = [
    {
        "question_text": "What is the chemical formula for water?",
        "question_type": "mcq",
        "options": ["H₂O", "CO₂", "O₂", "NaCl"],
        "correct": "H₂O",
        "emoji_hint": "💧",
        "difficulty": "medium",
    },
    {
        "question_text": "Who painted the Mona Lisa?",
        "question_type": "mcq",
        "options": ["Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh", "Michelangelo"],
        "correct": "Leonardo da Vinci",
        "emoji_hint": "🎨",
        "difficulty": "medium",
    },
    {
        "question_text": "What is the result of 15 × 12?",
        "question_type": "mcq",
        "options": ["180", "170", "190", "160"],
        "correct": "180",
        "emoji_hint": "🧮",
        "difficulty": "medium",
    },
    {
        "question_text": "Which programming concept repeats a block of code multiple times?",
        "question_type": "mcq",
        "options": ["Loop", "Variable", "Function", "Array"],
        "correct": "Loop",
        "emoji_hint": "🔄",
        "difficulty": "hard",
    },
    {
        "question_text": "What is the powerhouse of the cell?",
        "question_type": "mcq",
        "options": ["Mitochondria", "Nucleus", "Ribosome", "Cell Wall"],
        "correct": "Mitochondria",
        "emoji_hint": "🔬",
        "difficulty": "hard",
    },
    {
        "question_text": "If a triangle has angles of 60°, 60°, and 60°, what type is it?",
        "question_type": "mcq",
        "options": ["Equilateral", "Isosceles", "Scalene", "Right-angle"],
        "correct": "Equilateral",
        "emoji_hint": "📐",
        "difficulty": "medium",
    },
    {
        "question_text": "Write one word that means 'very happy':",
        "question_type": "open_ended",
        "options": [],
        "correct": "ecstatic,joyful,elated,delighted,thrilled,overjoyed,blissful",
        "emoji_hint": "😊",
        "difficulty": "easy",
    },
    {
        "question_text": "What force keeps us on the ground?",
        "question_type": "mcq",
        "options": ["Gravity", "Friction", "Magnetism", "Electricity"],
        "correct": "Gravity",
        "emoji_hint": "🍎",
        "difficulty": "easy",
    },
]

QUESTION_BANKS = {
    "toddler": TODDLER_QUESTIONS,
    "explorer": EXPLORER_QUESTIONS,
    "creator":  CREATOR_QUESTIONS,
}

# Track used questions per user to avoid repeats within a session
_used_questions = {}


def get_question(age_group: str = "creator", user_id: int = 0) -> dict:
    """Get a random age-appropriate question."""
    bank = QUESTION_BANKS.get(age_group, CREATOR_QUESTIONS)

    # Try to avoid repeats
    key = f"{user_id}_{age_group}"
    used = _used_questions.get(key, set())
    available = [i for i in range(len(bank)) if i not in used]
    if not available:
        _used_questions[key] = set()
        available = list(range(len(bank)))

    idx = random.choice(available)
    _used_questions.setdefault(key, set()).add(idx)

    q = bank[idx]
    qid = f"{age_group}_{idx}_{uuid.uuid4().hex[:6]}"

    return {
        "question_id":   qid,
        "question_text": q["question_text"],
        "question_type": q["question_type"],
        "options":       q["options"],
        "emoji_hint":    q.get("emoji_hint", ""),
        "difficulty":    q.get("difficulty", "easy"),
        "age_group":     age_group,
        "correct_answer": q["correct"],  # stored server-side, not sent to client fully
        "audio_cue":     q.get("audio_cue", ""),
    }


def check_answer(age_group: str, question_id: str, answer: str) -> dict:
    """Check if the answer is correct and return feedback."""
    # Parse question index from ID
    parts = question_id.split("_")
    if len(parts) < 2:
        return {"correct": False, "feedback": "Invalid question!", "correct_answer": ""}

    group = parts[0]
    try:
        idx = int(parts[1])
    except (ValueError, IndexError):
        return {"correct": False, "feedback": "Invalid question!", "correct_answer": ""}

    bank = QUESTION_BANKS.get(group, CREATOR_QUESTIONS)
    if idx >= len(bank):
        return {"correct": False, "feedback": "Question not found!", "correct_answer": ""}

    q = bank[idx]
    correct_answer = q["correct"]

    # For open_ended, check if answer contains any accepted words
    if q["question_type"] == "open_ended":
        accepted = [a.strip().lower() for a in correct_answer.split(",")]
        is_correct = answer.strip().lower() in accepted
    else:
        is_correct = answer.strip() == correct_answer.strip()

    # Age-appropriate feedback
    if is_correct:
        feedbacks = {
            "toddler": random.choice(["🎉 YAY! So smart!", "⭐ WOW! You did it!", "🌟 Amazing!"]),
            "explorer": random.choice([
                "🎉 Awesome job! You're super smart!",
                "⭐ Correct! Keep up the great work!",
                "🌟 You got it! You're a real explorer!",
            ]),
            "creator": random.choice([
                "🎉 Excellent! Your knowledge is impressive!",
                "⭐ Correct! You're really getting the hang of this!",
                "🌟 Perfect answer! Keep challenging yourself!",
            ]),
        }
    else:
        feedbacks = {
            "toddler": random.choice(["Almost! Try again! 💪", "Oops! Let's try once more! 🌈"]),
            "explorer": random.choice([
                f"Not quite! The answer is {correct_answer}. You'll get the next one! 💪",
                f"Close! It's actually {correct_answer}. Keep trying! 🌈",
            ]),
            "creator": random.choice([
                f"Not this time! The correct answer is {correct_answer}. Great effort though! 💪",
                f"Almost! It's {correct_answer}. You're learning with every question! 📚",
            ]),
        }

    points = 0
    if is_correct:
        points = {"toddler": 5, "explorer": 10, "creator": 15}.get(age_group, 10)

    return {
        "correct":        is_correct,
        "feedback":       feedbacks.get(age_group, feedbacks["creator"]),
        "points_earned":  points,
        "correct_answer": correct_answer,
    }
