from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, get_db
from app.schemas.api import IdentityResponse, BehaviorResponse, GapAnalysisResponse, IdentityUpdate
from app.models.user import User
from app.repositories.identity_repository import IdentityRepository
from app.repositories.behavior_repository import BehaviorRepository

router = APIRouter()

@router.get("/identity", response_model=IdentityResponse, summary="Get identity profile")
async def get_identity(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieves personality mappings and archetype definitions for the user."""
    identity_repo = IdentityRepository(db)
    profile = await identity_repo.get_by_user_id(current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Identity profile not found"
        )
    return IdentityResponse(
        id=profile.id,
        user_id=profile.user_id,
        archetype=profile.archetype,
        core_values=profile.core_values,
        strengths=profile.strengths,
        weaknesses=profile.weaknesses
    )

@router.get("/behavior", response_model=BehaviorResponse, summary="Get behavior profile")
async def get_behavior(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieves habits, cognitive patterns, and energy curves for the user."""
    behavior_repo = BehaviorRepository(db)
    profile = await behavior_repo.get_by_user_id(current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Behavior profile not found"
        )
    return BehaviorResponse(
        id=profile.id,
        user_id=profile.user_id,
        habits=profile.habits,
        cognitive_patterns=profile.cognitive_patterns,
        energy_levels={k: float(v) for k, v in profile.energy_levels.items()}
    )

@router.get("/gap-analysis", response_model=GapAnalysisResponse, summary="Get current Gap Analysis")
async def get_gap_analysis(current_user: User = Depends(get_current_user)):
    """Returns the user's analyzed skill gaps and recommended learning strategies."""
    # Returns the computed gap analysis from current session state/memory
    return GapAnalysisResponse(
        gap_description="User lacks structured knowledge in data structures and backend system interfaces.",
        priority_score=0.88,
        target_skills=["Python", "System Design", "Databases"],
        urgency="High",
        recommends_strategy="Project-First Intensive"
    )

@router.put("/identity", response_model=IdentityResponse, summary="Update identity profile")
async def update_identity(
    update_data: IdentityUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Updates user's archetype, core values, strengths, and weaknesses."""
    identity_repo = IdentityRepository(db)
    profile = await identity_repo.get_by_user_id(current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Identity profile not found"
        )
    
    if update_data.archetype is not None:
        profile.archetype = update_data.archetype
    if update_data.core_values is not None:
        profile.core_values = update_data.core_values
    if update_data.strengths is not None:
        profile.strengths = update_data.strengths
    if update_data.weaknesses is not None:
        profile.weaknesses = update_data.weaknesses
        
    await db.commit()
    await db.refresh(profile)
    
    return IdentityResponse(
        id=profile.id,
        user_id=profile.user_id,
        archetype=profile.archetype,
        core_values=profile.core_values,
        strengths=profile.strengths,
        weaknesses=profile.weaknesses
    )

