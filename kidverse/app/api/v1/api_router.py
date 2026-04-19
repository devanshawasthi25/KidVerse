from fastapi import APIRouter
from app.api.v1.endpoints import chat, story, drawing, users, toddler, auth, games, video_story

api_router = APIRouter()
api_router.include_router(chat.router)
api_router.include_router(story.router)
api_router.include_router(drawing.router)
api_router.include_router(users.router)
api_router.include_router(toddler.router)
api_router.include_router(auth.router)
api_router.include_router(games.router)
api_router.include_router(video_story.router)