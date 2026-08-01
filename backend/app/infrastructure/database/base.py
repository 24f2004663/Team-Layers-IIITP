# Import all models here so that Base.metadata is fully populated
# before Alembic runs autogenerate.
from app.models.base import Base
from app.models.user import User
from app.models.identity import IdentityProfile
from app.models.goal import Goal
from app.models.skill import Skill
from app.models.behavior import BehaviorProfile
from app.models.daily_plan import DailyPlan
from app.models.resource import Resource
from app.models.recommendation import Recommendation
from app.models.reflection import Reflection
from app.models.progress import Progress

__all__ = (
    "Base",
    "User",
    "IdentityProfile",
    "Goal",
    "Skill",
    "BehaviorProfile",
    "DailyPlan",
    "Resource",
    "Recommendation",
    "Reflection",
    "Progress",
)
