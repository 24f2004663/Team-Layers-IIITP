from typing import Any, Dict, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.graph.memory_contracts import ProgressMemoryManager
from app.repositories.progress_repository import ProgressRepository
from app.repositories.goal_repository import GoalRepository
from app.infrastructure.logging.logger import logger

class SQLProgressMemoryManager(ProgressMemoryManager):
    """Memory manager bridge for Progress histories and Goal completion logs."""

    def __init__(self, db: AsyncSession):
        """Initializes the manager.
        
        Args:
            db: Active database AsyncSession.
        """
        self.progress_repo = ProgressRepository(db)
        self.goal_repo = GoalRepository(db)

    async def load(self, user_id: UUID) -> Dict[str, Any]:
        """Loads progress memory profile for user.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            Dict[str, Any]: Progress indicators and active goal summaries.
        """
        records = await self.progress_repo.get_by_user_id(user_id)
        active_goals = await self.goal_repo.get_by_user_id(user_id)
        
        latest_record = records[-1] if records else None
        
        return {
            "growth_score": latest_record.growth_score if latest_record else 0.0,
            "milestone_completion_rate": latest_record.milestone_completion_rate if latest_record else 0.0,
            "habit_adherence": latest_record.habit_adherence if latest_record else 0.0,
            "goals_count": len(active_goals),
        }

    async def save(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Saves progress log.
        
        Args:
            user_id: Target user UUID.
            data: Data payload to save.
            
        Returns:
            bool: True if success, False otherwise.
        """
        try:
            db_data = {
                "user_id": user_id,
                "growth_score": data.get("growth_score", 0.0),
                "milestone_completion_rate": data.get("milestone_completion_rate", 0.0),
                "habit_adherence": data.get("habit_adherence", 0.0),
            }
            await self.progress_repo.create(db_data)
            return True
        except Exception as e:
            logger.error("ProgressMemoryManager save failed", error=str(e), user_id=str(user_id))
            return False

    async def update(self, user_id: UUID, data: Dict[str, Any]) -> bool:
        """Updates active progress memory.
        
        Args:
            user_id: Target user UUID.
            data: Update payload.
            
        Returns:
            bool: True if success, False otherwise.
        """
        return await self.save(user_id, data)

    async def delete(self, user_id: UUID) -> bool:
        """Deletes active progress records.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            bool: True if success, False otherwise.
        """
        records = await self.progress_repo.get_by_user_id(user_id)
        for record in records:
            await self.progress_repo.delete(record.id, soft=True)
        return True

    async def search(self, user_id: UUID, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries and searches active user goals matching query strings.
        
        Args:
            user_id: Target user UUID.
            query: String query to find.
            limit: Maximum count.
            
        Returns:
            List[Dict[str, Any]]: Matching elements.
        """
        goals = await self.goal_repo.get_by_user_id(user_id)
        matches = []
        q = query.lower()
        for goal in goals:
            if q in goal.title.lower() or (goal.description and q in goal.description.lower()):
                matches.append({"goal_id": str(goal.id), "title": goal.title, "status": goal.status})
        return matches[:limit]

    async def summarize(self, user_id: UUID) -> str:
        """Summarizes progress in text format.
        
        Args:
            user_id: Target user UUID.
            
        Returns:
            str: Summary.
        """
        data = await self.load(user_id)
        return f"User growth score is {data.get('growth_score', 0.0)}. Milestone completion rate is {data.get('milestone_completion_rate', 0.0)*100}%."
