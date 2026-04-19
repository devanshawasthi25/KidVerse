from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import (
    SignupRequest, LoginRequest, OTPVerifyRequest, OTPSendRequest, AuthResponse
)
from app.services.auth_service import (
    create_authenticated_user, authenticate_user,
    verify_user_otp, resend_otp, is_dev_mode
)
from app.services.reward_service import award_points

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    """Register a new user with email + password. Sends OTP for verification."""
    try:
        user, otp = create_authenticated_user(
            db=db,
            email=payload.email,
            password=payload.password,
            name=payload.name,
            avatar=payload.avatar,
            age_group=payload.age_group,
            phone=payload.phone,
        )
        response = {
            "user_id": user.id,
            "name": user.name,
            "age_group": user.age_group,
            "verified": False,
        }
        if is_dev_mode():
            response["message"] = f"Account created! Your OTP is: {otp} (Dev mode — no email configured)"
            response["dev_otp"] = otp
        else:
            response["message"] = "Account created! Check your email for the verification code."
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Login with email + password."""
    try:
        user = authenticate_user(db, payload.email, payload.password)
        # Award login points
        award_points(db, user.id, "login", "user-login")
        return {
            "user_id": user.id,
            "name": user.name,
            "age_group": user.age_group,
            "message": "Welcome back!",
            "verified": user.is_verified,
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/verify-otp")
def verify_otp(payload: OTPVerifyRequest, db: Session = Depends(get_db)):
    """Verify a user's OTP code."""
    try:
        user = verify_user_otp(db, payload.email, payload.otp_code)
        # Award points for verification
        award_points(db, user.id, "login", "email-verified")
        return {
            "user_id": user.id,
            "name": user.name,
            "age_group": user.age_group,
            "message": "Email verified successfully!",
            "verified": True,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/send-otp")
def send_otp(payload: OTPSendRequest, db: Session = Depends(get_db)):
    """Send or resend an OTP to the user's email."""
    try:
        otp = resend_otp(db, payload.email)
        response = {"message": "A new verification code has been sent to your email."}
        if is_dev_mode():
            response["message"] = f"Your new OTP is: {otp} (Dev mode)"
            response["dev_otp"] = otp
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me")
def get_me(user_id: int, db: Session = Depends(get_db)):
    """Get current user info (using user_id query param for now)."""
    from app.models.user import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "avatar": user.avatar,
        "age_group": user.age_group,
        "points": user.points,
        "level": user.level,
        "verified": user.is_verified,
    }
