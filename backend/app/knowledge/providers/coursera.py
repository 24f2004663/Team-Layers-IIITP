from typing import List, Optional
from app.knowledge.providers.base import KnowledgeProvider
from app.knowledge.models import GrowthOpportunity, OpportunityType
from app.knowledge.context import KnowledgeQuery

class CourseraProvider(KnowledgeProvider):
    """Integration provider wrapper for Coursera / online courses discovery."""

    async def search(self, query: KnowledgeQuery) -> List[GrowthOpportunity]:
        raise NotImplementedError("Coursera API search not implemented yet.")

    async def fetch(self, opportunity_id: str) -> Optional[GrowthOpportunity]:
        raise NotImplementedError("Coursera API fetch not implemented yet.")

    async def health(self) -> bool:
        return True

    def supports(self, opportunity_type: OpportunityType) -> bool:
        return opportunity_type in (OpportunityType.COURSE, OpportunityType.CERTIFICATION)

    def get_provider_name(self) -> str:
        return "Coursera"
