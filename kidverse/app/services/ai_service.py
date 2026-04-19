import os
import re
import httpx
from typing import Optional

# ── Config ────────────────────────────────────────────────────────────────────

AI_PROVIDER    = os.getenv("AI_PROVIDER",    "claude")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CLAUDE_MODEL   = "claude-3-haiku-20240307"
OPENAI_MODEL   = "gpt-3.5-turbo"

# ── Safety ────────────────────────────────────────────────────────────────────

BLOCKED_KEYWORDS = [
    "kill","murder","blood","gore","sex","porn","nude","naked",
    "drugs","weapon","bomb","terror","suicide","hate","racist",
    "violence","alcohol","cigarette","gambling","hack","cheat",
]

# Extra blocked for toddlers (anything abstract/scary)
TODDLER_EXTRA_BLOCKED = [
    "scary","monster","ghost","death","die","dead","dark","evil",
    "stranger","fight","angry","hurt","pain",
]

# ── System Prompts (per age group) ────────────────────────────────────────────

SYSTEM_PROMPTS = {
    "toddler": """You are Cosmo, a gentle, loving friend for very young children (ages 1–4).
Rules you MUST follow:
- Use ONLY 1–3 very simple words per sentence. Examples: "Wow! Big dog!" or "So fluffy! 🐶"
- Use LOTS of emojis — one per sentence minimum
- ONLY talk about: animals, colors, shapes, simple sounds, happy things
- NEVER use scary, sad, complex, or adult words
- Respond like you're clapping and smiling with joy
- Max 2 sentences per response
""",

    "explorer": """You are Cosmo, a fun and encouraging guide for children aged 5–9.
Your style:
- Use simple, clear sentences (max 10 words each)
- Be enthusiastic and encouraging — use 1–2 emojis per message
- Explain things step by step
- Ask 1 simple follow-up question to keep them curious
- NEVER use scary, violent, or adult themes
- Max 4 sentences per response
""",

    "creator": """You are Cosmo, a friendly and inspiring AI companion for children aged 10–14.
Your personality:
- Warm, encouraging, and enthusiastic
- Use age-appropriate language — smart but not complex
- Add fun emojis occasionally 🌟
- Celebrate creativity and curiosity
- Give clear responses (max 4–5 sentences for chat)
Rules:
- NEVER discuss violence, scary content, or adult themes
- NEVER give personal advice on sensitive topics — suggest a trusted adult
- Always be positive and uplifting
""",
}

STORY_PROMPTS = {
    "toddler": """You are Cosmo, a bedtime story helper for babies and toddlers (ages 1–4).
Write a story that is:
- ONLY 3–4 simple sentences total
- Uses big font words — animals, colors, hugs, sleep
- Ends with sleeping or a big hug
- Format: TITLE: [Title]\n[Story — 3 sentences max]
- NO scary words, NEVER complex sentences
""",

    "explorer": """You are Cosmo, a storyteller for curious kids aged 5–9.
Write a story that is:
- 80–130 words
- Has a simple hero, a small problem, and a happy ending
- Uses simple vocabulary, vivid and fun
- Adds 1 moral lesson (friendship, kindness, bravery)
- Format: TITLE: [Title]\n[Story]
""",

    "creator": """You are Cosmo, a creative storyteller for children aged 10–14.
Write stories that are:
- 150–250 words long
- Structured: clear beginning, middle, happy ending
- Full of wonder, friendship, and adventure
- Vivid but age-appropriate language
- Subtle moral lessons (kindness, courage, honesty)
- Format: TITLE: [Title]\n[Story]
- NEVER include scary, violent, or adult content.
""",
}

# ── Toddler Play Data ─────────────────────────────────────────────────────────

import random

TODDLER_PLAY_DATA = [
    {"type":"animal","name":"cat",      "sound":"meow",    "color":"orange",   "emoji":"🐱","fun_fact":"Cats purr when happy!"},
    {"type":"animal","name":"dog",      "sound":"woof",    "color":"brown",    "emoji":"🐶","fun_fact":"Dogs wag their tails!"},
    {"type":"animal","name":"duck",     "sound":"quack",   "color":"yellow",   "emoji":"🦆","fun_fact":"Ducks love the water!"},
    {"type":"animal","name":"cow",      "sound":"moo",     "color":"white",    "emoji":"🐄","fun_fact":"Cows give us milk!"},
    {"type":"animal","name":"frog",     "sound":"ribbit",  "color":"green",    "emoji":"🐸","fun_fact":"Frogs can jump very high!"},
    {"type":"animal","name":"elephant", "sound":"trumpet", "color":"grey",     "emoji":"🐘","fun_fact":"Elephants have big ears!"},
    {"type":"animal","name":"lion",     "sound":"roar",    "color":"golden",   "emoji":"🦁","fun_fact":"Lions have fluffy manes!"},
    {"type":"animal","name":"bunny",    "sound":"squeak",  "color":"white",    "emoji":"🐰","fun_fact":"Bunnies have soft fur!"},
    {"type":"animal","name":"fish",     "sound":"blub",    "color":"blue",     "emoji":"🐠","fun_fact":"Fish swim in the sea!"},
    {"type":"animal","name":"pig",      "sound":"oink",    "color":"pink",     "emoji":"🐷","fun_fact":"Pigs love to play in mud!"},
    {"type":"shape", "name":"circle",   "sound":"whoosh",  "color":"red",      "emoji":"🔴","fun_fact":"Circles are perfectly round!"},
    {"type":"shape", "name":"star",     "sound":"twinkle", "color":"yellow",   "emoji":"⭐","fun_fact":"Stars shine in the sky!"},
    {"type":"shape", "name":"heart",    "sound":"thump",   "color":"pink",     "emoji":"💖","fun_fact":"Hearts mean love!"},
    {"type":"color", "name":"rainbow",  "sound":"wow",     "color":"rainbow",  "emoji":"🌈","fun_fact":"Rainbows have 7 colors!"},
    {"type":"color", "name":"sunshine", "sound":"yay",     "color":"yellow",   "emoji":"☀️","fun_fact":"Sunshine makes flowers grow!"},
]


def get_random_play() -> dict:
    return random.choice(TODDLER_PLAY_DATA)


# ── Safety ────────────────────────────────────────────────────────────────────

def is_safe_input(text: str, age_group: str = "creator") -> tuple[bool, str]:
    lower = text.lower()
    blocked = BLOCKED_KEYWORDS[:]
    if age_group == "toddler":
        blocked += TODDLER_EXTRA_BLOCKED
    for kw in blocked:
        if re.search(r'\b' + kw + r'\b', lower):
            return False, kw
    return True, ""


def sanitize_response(text: str) -> str:
    for kw in BLOCKED_KEYWORDS:
        text = re.compile(r'\b' + kw + r'\b', re.IGNORECASE).sub("***", text)
    return text


def _mock_response(age_group: str) -> str:
    mocks = {
        "toddler": "🌟 Yay! So fun! 🎉",
        "explorer": "Hi there! 🌟 I'm Cosmo! Ask a grown-up to set up my AI key so I can help you explore! 🚀",
        "creator": "Hi! I'm Cosmo, your creative buddy! Ask a grown-up to set up the API key so we can create amazing things together! 🌟",
    }
    return mocks.get(age_group, mocks["creator"])


# ── API Callers ───────────────────────────────────────────────────────────────

async def call_claude(system: str, user_message: str, max_tokens: int = 500) -> str:
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": CLAUDE_API_KEY, "anthropic-version": "2023-06-01",
                     "content-type": "application/json"},
            json={"model": CLAUDE_MODEL, "max_tokens": max_tokens,
                  "system": system, "messages": [{"role": "user", "content": user_message}]},
        )
        resp.raise_for_status()
        return resp.json()["content"][0]["text"]


async def call_openai(system: str, user_message: str, max_tokens: int = 500) -> str:
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}",
                     "Content-Type": "application/json"},
            json={"model": OPENAI_MODEL, "max_tokens": max_tokens,
                  "messages": [{"role": "system", "content": system},
                                {"role": "user", "content": user_message}]},
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


# ── Main Entry ────────────────────────────────────────────────────────────────

async def call_ai(
    user_message:  str,
    system_prompt: Optional[str] = None,
    max_tokens:    int = 500,
    age_group:     str = "creator",
) -> str:
    """Route to AI with full age-adaptive safety + tone."""

    if not user_message or not user_message.strip():
        return "Please say something so I can help! 😊"

    # Toddlers should not use chat — return play prompt
    if age_group == "toddler":
        return "🎉 Let's play! Tap the big buttons below! 🐱🌈"

    safe, blocked = is_safe_input(user_message, age_group)
    if not safe:
        if age_group == "explorer":
            return "Hmm, let's talk about something fun instead! 🌈 Want to hear a story?"
        return "Hmm, I think we should talk about something fun instead! 🌈 How about we create a story or draw something together?"

    # Determine system prompt: caller can override, else use age-group default
    system = system_prompt or SYSTEM_PROMPTS.get(age_group, SYSTEM_PROMPTS["creator"])

    # Reduce tokens for younger modes
    if age_group == "explorer":
        max_tokens = min(max_tokens, 200)

    active_key = OPENAI_API_KEY if AI_PROVIDER == "openai" else CLAUDE_API_KEY
    if not active_key:
        return _mock_response(age_group)

    try:
        if AI_PROVIDER == "openai":
            reply = await call_openai(system, user_message, max_tokens)
        else:
            reply = await call_claude(system, user_message, max_tokens)
        return sanitize_response(reply)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return "🔑 Oops! The AI key needs to be set up. Ask a grown-up!"
        return "Oops, I had a little hiccup! 🌟 Try again in a moment."
    except Exception:
        return "I'm taking a tiny nap! 😴 Try again in a moment."


def get_story_prompt(age_group: str) -> str:
    return STORY_PROMPTS.get(age_group, STORY_PROMPTS["creator"])


def get_story_max_tokens(age_group: str) -> int:
    return {"toddler": 100, "explorer": 300, "creator": 600}.get(age_group, 600)