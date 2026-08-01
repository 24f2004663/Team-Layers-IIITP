from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.api import UserRegister, TokenResponse, UserResponse
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.identity import IdentityProfile
from app.models.behavior import BehaviorProfile
from app.core.auth import hash_password, verify_password, create_access_token, create_refresh_token

router = APIRouter()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED, summary="Register a new user")
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    """Registers a new user account, creates their initial Identity and Behavior profiles, and returns tokens."""
    user_repo = UserRepository(db)
    existing_user = await user_repo.get_by_email(data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already registered"
        )
    
    # 1. Create and hash the user
    new_user = User(
        email=data.email,
        hashed_password=hash_password(password=data.password),
        full_name=data.full_name
    )
    db.add(new_user)
    await db.flush()  # Populates user id
    
    # 2. Setup Default Profiles
    identity = IdentityProfile(
        user_id=new_user.id,
        archetype=data.archetype or "Explorer",
        core_values=data.core_values,
        strengths=data.strengths,
        weaknesses=data.weaknesses
    )
    behavior = BehaviorProfile(
        user_id=new_user.id,
        habits={"reading": {"streak": 1, "completed_today": False}},
        cognitive_patterns=["Visual learning preferred"],
        energy_levels={"Morning": 0.85, "Afternoon": 0.50, "Evening": 0.70}
    )
    db.add(identity)
    db.add(behavior)
    await db.commit()
    
    # 3. Generate tokens
    access_token = create_access_token(data={"sub": str(new_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(new_user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/login", response_model=TokenResponse, summary="User login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Authenticates a user via email and password and returns access/refresh tokens."""
    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(form_data.username)  # OAuth2 uses username field
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
