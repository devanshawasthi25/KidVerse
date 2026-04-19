import os
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

import bcrypt
from sqlalchemy.orm import Session

from app.models.user import User

# ── Config ────────────────────────────────────────────────────────────────────

SMTP_HOST     = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT     = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER     = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
JWT_SECRET    = os.getenv("JWT_SECRET", "kidverse-super-secret-key-change-me")

OTP_EXPIRY_MINUTES = 5


# ── Password Hashing ─────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


# ── OTP ───────────────────────────────────────────────────────────────────────

def generate_otp() -> str:
    return "".join(random.choices(string.digits, k=6))


def is_dev_mode() -> bool:
    """Check if SMTP is not configured (dev mode)."""
    return not SMTP_USER or not SMTP_PASSWORD


def send_otp_email(to_email: str, otp_code: str) -> bool:
    """Send OTP via email using SMTP. Returns True on success."""
    if not SMTP_USER or not SMTP_PASSWORD:
        # Dev mode: print OTP to console (ASCII-safe for Windows)
        try:
            print(f"\n{'='*50}")
            print(f"  [EMAIL OTP] for {to_email}: {otp_code}")
            print(f"  (Set SMTP_USER & SMTP_PASSWORD in .env for real emails)")
            print(f"{'='*50}\n")
        except Exception:
            pass  # Console encoding issue on Windows
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "KidVerse - Your Verification Code"
        msg["From"]    = SMTP_USER
        msg["To"]      = to_email

        html = f"""
        <html>
        <body style="font-family: 'Nunito', Arial, sans-serif; background: #F7F9F4; padding: 40px;">
            <div style="max-width: 480px; margin: 0 auto; background: white; border-radius: 24px;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.07); padding: 40px; text-align: center;">
                <div style="font-size: 4rem; margin-bottom: 16px;">🌟</div>
                <h1 style="color: #2F2F2F; font-size: 1.8rem; margin-bottom: 8px;">KidVerse Verification</h1>
                <p style="color: #6B7280; font-size: 1.1rem; margin-bottom: 24px;">
                    Here's your one-time verification code:
                </p>
                <div style="background: linear-gradient(135deg, #FF9A8B, #FF7A68); color: white;
                            font-size: 2.5rem; font-weight: 900; letter-spacing: 8px;
                            padding: 20px 32px; border-radius: 16px; display: inline-block;
                            margin-bottom: 24px;">
                    {otp_code}
                </div>
                <p style="color: #6B7280; font-size: 0.9rem;">
                    This code expires in {OTP_EXPIRY_MINUTES} minutes.<br>
                    If you didn't request this, please ignore this email.
                </p>
                <hr style="border: none; border-top: 2px solid #EAF3FF; margin: 24px 0;">
                <p style="color: #C7EDE6; font-size: 0.85rem;">
                    🌱 Safe · 🎓 Educational · 😊 Fun — KidVerse
                </p>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"[AUTH] Email send failed: {e}")
        return False


# ── User Auth Operations ──────────────────────────────────────────────────────

def create_authenticated_user(
    db: Session,
    email: str,
    password: str,
    name: str,
    avatar: str = "star",
    age_group: str = "creator",
    phone: str = None,
) -> tuple[User, str]:
    """Create user with hashed password & generate OTP. Returns (user, otp_code)."""

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise ValueError("An account with this email already exists")

    otp = generate_otp()
    user = User(
        name          = name,
        email         = email,
        password_hash = hash_password(password),
        avatar        = avatar or "star",
        age_group     = age_group or "creator",
        phone         = phone,
        is_verified   = False,
        otp_code      = otp,
        otp_expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Send OTP
    send_otp_email(email, otp)

    return user, otp


def authenticate_user(db: Session, email: str, password: str) -> User:
    """Verify email + password. Returns user or raises ValueError."""
    user = db.query(User).filter(User.email == email.lower().strip()).first()
    if not user:
        raise ValueError("No account found with this email")
    if not user.password_hash:
        raise ValueError("This account was created without a password. Please sign up again.")
    if not verify_password(password, user.password_hash):
        raise ValueError("Incorrect password")
    return user


def verify_user_otp(db: Session, email: str, otp_code: str) -> User:
    """Verify OTP code. Returns user or raises ValueError."""
    user = db.query(User).filter(User.email == email.lower().strip()).first()
    if not user:
        raise ValueError("No account found with this email")
    if user.is_verified:
        raise ValueError("Account is already verified")
    if not user.otp_code:
        raise ValueError("No OTP was generated. Please request a new one.")
    if user.otp_expires_at and datetime.utcnow() > user.otp_expires_at:
        raise ValueError("OTP has expired. Please request a new one.")
    if user.otp_code != otp_code:
        raise ValueError("Invalid OTP code")

    user.is_verified = True
    user.otp_code = None
    user.otp_expires_at = None
    db.commit()
    db.refresh(user)
    return user


def resend_otp(db: Session, email: str) -> str:
    """Generate and send a new OTP. Returns the OTP code."""
    user = db.query(User).filter(User.email == email.lower().strip()).first()
    if not user:
        raise ValueError("No account found with this email")
    if user.is_verified:
        raise ValueError("Account is already verified")

    otp = generate_otp()
    user.otp_code = otp
    user.otp_expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    db.commit()

    send_otp_email(email, otp)
    return otp
