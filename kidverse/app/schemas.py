from pydantic import BaseModel, field_validator
from typing import Optional, Literal

AgeGroup = Literal["toddler", "explorer", "creator"]

# ── Chat ──────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message:   str
    user_id:   Optional[int] = None
    age_group: AgeGroup      = "creator"


class ChatResponse(BaseModel):
    reply:        str
    points_earned: int = 0
    mode:         str  = "creator"


# ── Story ─────────────────────────────────────────────────────────────────────

class StoryRequest(BaseModel):
    theme:     str
    character: str
    user_id:   Optional[int] = None
    age_group: AgeGroup      = "creator"


class StoryResponse(BaseModel):
    title:        str
    story:        str
    points_earned: int = 0
    mode:         str  = "creator"


# ── Drawing ───────────────────────────────────────────────────────────────────

class DrawingSaveRequest(BaseModel):
    image_data: str
    title:      Optional[str] = "My Drawing"
    user_id:    Optional[int] = None


class DrawingSaveResponse(BaseModel):
    message:      str
    filename:     str
    points_earned: int = 0


# ── Toddler Play ──────────────────────────────────────────────────────────────

class PlayResponse(BaseModel):
    type:        str
    name:        str
    sound:       str
    color:       str
    emoji:       str
    fun_fact:    str


# ── User ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    name:      str
    avatar:    Optional[str] = "star"
    age_group: AgeGroup      = "creator"


class UserOut(BaseModel):
    id:        int
    name:      str
    avatar:    str
    age_group: str
    points:    int
    level:     int

    class Config:
        from_attributes = True


# ── Auth ──────────────────────────────────────────────────────────────────────

class SignupRequest(BaseModel):
    email:     str
    password:  str
    name:      str
    avatar:    Optional[str] = "star"
    age_group: AgeGroup      = "creator"
    phone:     Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email address")
        return v.lower().strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class LoginRequest(BaseModel):
    email:    str
    password: str


class OTPVerifyRequest(BaseModel):
    email:    str
    otp_code: str


class OTPSendRequest(BaseModel):
    email: str


class AuthResponse(BaseModel):
    user_id:  int
    name:     str
    age_group: str
    message:  str
    verified: bool = False


# ── Games ─────────────────────────────────────────────────────────────────────

class GameQuestionResponse(BaseModel):
    question_id:   str
    question_text: str
    question_type: str          # visual, mcq, open_ended, audio_visual
    options:       list = []
    emoji_hint:    Optional[str] = None
    difficulty:    str = "easy"
    age_group:     str = "creator"


class GameAnswerRequest(BaseModel):
    user_id:     int
    question_id: str
    answer:      str
    age_group:   AgeGroup = "creator"


class GameAnswerResponse(BaseModel):
    correct:       bool
    feedback:      str
    points_earned: int = 0
    streak:        int = 0
    correct_answer: str = ""


# ── Video Story ───────────────────────────────────────────────────────────────

class VideoCheckpoint(BaseModel):
    timestamp:      float       # seconds into video
    question_text:  str
    question_type:  str         # audio_visual, multiple_choice, open_ended
    options:        list = []
    correct_answer: str
    audio_cue:      Optional[str] = None  # emoji/text for audio hint
    image_options:  list = []   # for visual questions


class VideoStoryOut(BaseModel):
    id:           str
    title:        str
    description:  str
    thumbnail:    str
    video_url:    str
    duration:     str
    age_group:    str
    checkpoints:  list[VideoCheckpoint] = []
    total_points: int = 0


class VideoAnswerRequest(BaseModel):
    user_id:       int
    story_id:      str
    checkpoint_idx: int
    answer:        str


class VideoAnswerResponse(BaseModel):
    correct:       bool
    feedback:      str
    points_earned: int = 0
    correct_answer: str = ""