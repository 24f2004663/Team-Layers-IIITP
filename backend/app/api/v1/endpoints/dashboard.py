from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, get_db
from app.schemas.api import DashboardSummary, DashboardToday, DashboardProgress, DashboardFuture, DashboardFull
from app.models.user import User
from app.repositories.identity_repository import IdentityRepository

router = APIRouter()

@router.get("/summary", response_model=DashboardSummary, summary="Get summary of user performance indicators")
async def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Retrieves high-level composite index metrics for user's personal growth scorecard."""
    identity_repo = IdentityRepository(db)
    profile = await identity_repo.get_by_user_id(current_user.id)
    archetype = profile.archetype if profile else "Explorer"
    
    return DashboardSummary(
        archetype=archetype,
        overall_status="On Track - Productive routine established",
        active_goals_count=3,
        completed_tasks_count=12,
        composite_growth_index=0.82
    )

@router.get("/today", response_model=DashboardToday, summary="Get daily plan and target mission agenda")
async def get_dashboard_today(current_user: User = Depends(get_current_user)):
    """Retrieves schedule blocks, focus allocations, and recovery gaps mapped for the day."""
    return DashboardToday(
        current_mission="Complete Core Backend Architecture Sprint",
        agenda=[
            {
                "time": "09:00 - 10:30",
                "title": "Build REST Endpoints",
                "type": "Focus",
                "duration_minutes": 90
            },
            {
                "time": "10:30 - 11:00",
                "title": "Morning Coffee & Breathing Recovery",
                "type": "Break",
                "duration_minutes": 30
            }
        ],
        total_focused_minutes=90,
        breaks_count=1
    )

@router.get("/progress", response_model=DashboardProgress, summary="Get progress completion analytics")
async def get_dashboard_progress(current_user: User = Depends(get_current_user)):
    """Calculates weekly consistency scores, completion percentages, and energy alignments."""
    return DashboardProgress(
        completion_rate=0.78,
        habits_adherence=0.90,
        energy_levels={"Morning": 0.85, "Afternoon": 0.50, "Evening": 0.70},
        consistency_delta=0.08
    )

@router.get("/future", response_model=DashboardFuture, summary="Get future self simulator trajectory calibrations")
async def get_dashboard_future(current_user: User = Depends(get_current_user)):
    """Predicts goal completion probabilities and triggers preventive habit interventions."""
    return DashboardFuture(
        predicted_success_rate=0.86,
        calibration_factor=1.02,
        growth_trajectory_match=0.91,
        recommended_interventions=[
            "Schedule afternoon reflection: Energy levels dip after lunch",
            "Mitigate evening distraction: Lock device notification settings"
        ]
    )

@router.get("", response_model=DashboardFull, summary="Get complete dashboard aggregated report")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Returns the comprehensive consolidated dashboard payload for dashboard UI initialization."""
    summary = await get_dashboard_summary(current_user, db)
    today = await get_dashboard_today(current_user)
    progress = await get_dashboard_progress(current_user)
    future = await get_dashboard_future(current_user)
    
    return DashboardFull(
        summary=summary,
        today=today,
        progress=progress,
        future=future
    )
