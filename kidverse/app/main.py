import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, Query
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

from app.db.session import engine, get_db
from app.db.base import Base
import app.models.user
import app.models.activity
from app.api.v1.api_router import api_router
from app.models.user import User


def _uid(user_id) -> int:
    try:
        return int(user_id) if user_id else 0
    except (ValueError, TypeError):
        return 0


def _run_migrations():
    """Add new columns to existing tables without breaking old data."""
    with engine.connect() as conn:
        # Add age_group column if it doesn't exist (SQLite safe)
        migrations = [
            "ALTER TABLE users ADD COLUMN age_group VARCHAR(20) DEFAULT 'creator'",
            "ALTER TABLE users ADD COLUMN email VARCHAR(255)",
            "ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)",
            "ALTER TABLE users ADD COLUMN phone VARCHAR(20)",
            "ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT 0",
            "ALTER TABLE users ADD COLUMN otp_code VARCHAR(6)",
            "ALTER TABLE users ADD COLUMN otp_expires_at DATETIME",
        ]
        for sql in migrations:
            try:
                conn.execute(text(sql))
                conn.commit()
            except Exception:
                pass  # Column already exists — that's fine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    _run_migrations()
    yield


app = FastAPI(
    title="KidVerse",
    description="An AI-powered age-adaptive creative platform for kids 🌟",
    version="3.0.0",
    lifespan=lifespan,
)

# ── Static & Templates ────────────────────────────────────────────────────────

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(os.path.join(STATIC_DIR, "drawings"), exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# ── API ───────────────────────────────────────────────────────────────────────

app.include_router(api_router, prefix="/api/v1")

# ── Page routes ───────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, user_id: str = Query(default="0")):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"user_id": _uid(user_id)}
    )


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={}
    )


@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request, user_id: str = Query(default="0"),
                    db: Session = Depends(get_db)):
    uid  = _uid(user_id)
    user = db.query(User).filter(User.id == uid).first() if uid else None
    age_group = user.age_group if user else "creator"
    return templates.TemplateResponse(
        request=request, name="chat.html",
        context={"user_id": uid, "age_group": age_group}
    )


@app.get("/story", response_class=HTMLResponse)
async def story_page(request: Request, user_id: str = Query(default="0"),
                     db: Session = Depends(get_db)):
    uid  = _uid(user_id)
    user = db.query(User).filter(User.id == uid).first() if uid else None
    age_group = user.age_group if user else "creator"
    return templates.TemplateResponse(
        request=request, name="story.html",
        context={"user_id": uid, "age_group": age_group}
    )


@app.get("/draw", response_class=HTMLResponse)
async def draw_page(request: Request, user_id: str = Query(default="0"),
                    db: Session = Depends(get_db)):
    uid  = _uid(user_id)
    user = db.query(User).filter(User.id == uid).first() if uid else None
    age_group = user.age_group if user else "creator"
    return templates.TemplateResponse(
        request=request, name="draw.html",
        context={"user_id": uid, "age_group": age_group}
    )


@app.get("/games", response_class=HTMLResponse)
async def games_page(request: Request, user_id: str = Query(default="0"),
                     db: Session = Depends(get_db)):
    uid  = _uid(user_id)
    user = db.query(User).filter(User.id == uid).first() if uid else None
    age_group = user.age_group if user else "creator"
    return templates.TemplateResponse(
        request=request, name="games.html",
        context={"user_id": uid, "age_group": age_group}
    )


@app.get("/world", response_class=HTMLResponse)
async def world_page(request: Request, user_id: str = Query(default="0"),
                     db: Session = Depends(get_db)):
    uid  = _uid(user_id)
    user = db.query(User).filter(User.id == uid).first() if uid else None
    age_group = user.age_group if user else "creator"
    user_name = user.name if user else "Explorer"
    return templates.TemplateResponse(
        request=request, name="world3d.html",
        context={"user_id": uid, "age_group": age_group, "user_name": user_name}
    )


@app.get("/video-stories", response_class=HTMLResponse)
async def video_stories_page(request: Request, user_id: str = Query(default="0"),
                              db: Session = Depends(get_db)):
    uid  = _uid(user_id)
    user = db.query(User).filter(User.id == uid).first() if uid else None
    age_group = user.age_group if user else "creator"
    return templates.TemplateResponse(
        request=request, name="video_story.html",
        context={"user_id": uid, "age_group": age_group}
    )


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, user_id: str = Query(default="0"),
                          db: Session = Depends(get_db)):
    from app.services.reward_service import get_user_stats
    uid   = _uid(user_id)
    stats = get_user_stats(db, uid) if uid else {}
    user  = stats.get("user") if stats else None
    age_group = user.age_group if user else "creator"
    return templates.TemplateResponse(
        request=request, name="dashboard.html",
        context={
            "user":              user,
            "user_id":           uid,
            "age_group":         age_group,
            "stats":             stats,
            "level_progress":    stats.get("level_progress", 0),
            "next_level_points": stats.get("next_level_points", 50),
            "recent_activities": stats.get("recent_activities", []),
        },
    )


@app.get("/health")
def health():
    return {"status": "ok", "app": "KidVerse 🌟", "version": "3.0.0"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content=b"", media_type="image/x-icon")


@app.get("/toddler-hub", response_class=HTMLResponse)
async def toddler_hub(
    request: Request,
    user_id: str = Query(default="0"),
    db: Session = Depends(get_db),
):
    uid  = _uid(user_id)
    user = db.query(User).filter(User.id == uid).first() if uid else None
    return templates.TemplateResponse(
        request=request,
        name="toddler_hub.html",
        context={
            "user_id":   uid,
            "user_name": user.name if user else "Little Star",
            "age_group": "toddler",
        },
    )


@app.get("/toddler-3d", response_class=HTMLResponse)
async def toddler_3d(
    request: Request,
    user_id: str = Query(default="0"),
    db: Session = Depends(get_db),
):
    uid  = _uid(user_id)
    user = db.query(User).filter(User.id == uid).first() if uid else None
    return templates.TemplateResponse(
        request=request,
        name="toddler_3d.html",
        context={
            "user_id":   uid,
            "user_name": user.name if user else "Little Star",
        },
    )