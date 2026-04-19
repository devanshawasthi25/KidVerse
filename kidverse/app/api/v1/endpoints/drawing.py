import os
import base64
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import DrawingSaveRequest, DrawingSaveResponse
from app.services.reward_service import award_points

router = APIRouter(prefix="/drawing", tags=["drawing"])

DRAWINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "static", "drawings")
os.makedirs(DRAWINGS_DIR, exist_ok=True)


@router.post("/save", response_model=DrawingSaveResponse)
async def save_drawing(request: DrawingSaveRequest, db: Session = Depends(get_db)):
    if not request.image_data or not request.image_data.strip():
        raise HTTPException(status_code=400, detail="No image data provided")

    img_data = request.image_data
    if "," in img_data:
        img_data = img_data.split(",", 1)[1]

    try:
        img_bytes = base64.b64decode(img_data)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image data")

    filename = f"drawing_{uuid.uuid4().hex[:8]}.png"
    filepath = os.path.join(DRAWINGS_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(img_bytes)

    points_earned = 0
    if request.user_id:
        points_earned = award_points(
            db, request.user_id, "drawing", f"Drawing: {request.title}"
        )

    return DrawingSaveResponse(
        message="Your masterpiece has been saved! 🎨",
        filename=filename,
        points_earned=points_earned,
    )


@router.get("/list")
def list_drawings():
    if not os.path.exists(DRAWINGS_DIR):
        return {"drawings": []}
    files = [f for f in os.listdir(DRAWINGS_DIR) if f.endswith(".png")]
    return {"drawings": sorted(files, reverse=True)}
