from typing import List, Optional
from app.knowledge.providers.base import KnowledgeProvider
from app.knowledge.models import GrowthOpportunity, OpportunityType
from app.knowledge.context import KnowledgeQuery

class MentorProvider(KnowledgeProvider):
    """Integration provider wrapper for mentorship/coaching opportunities discovery."""

    async def search(self, query: KnowledgeQuery) -> List[GrowthOpportunity]:
        raise NotImplementedError("Mentor search not implemented yet.")

    async def fetch(self, opportunity_id: str) -> Optional[GrowthOpportunity]:
        raise NotImplementedError("Mentor fetch not implemented yet.")

    async def health(self) -> bool:
        return True

    def supports(self, opportunity_type: OpportunityType) -> bool:
        return opportunity_type == OpportunityType.MENTOR

    def get_provider_name(self) -> str:
        return "Mentor"
