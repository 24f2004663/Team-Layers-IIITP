from typing import List, Optional
from app.knowledge.providers.base import KnowledgeProvider
from app.knowledge.models import GrowthOpportunity, OpportunityType
from app.knowledge.context import KnowledgeQuery

class CommunityProvider(KnowledgeProvider):
    """Integration provider wrapper for local and online communities and events discovery."""

    async def search(self, query: KnowledgeQuery) -> List[GrowthOpportunity]:
        raise NotImplementedError("Community search not implemented yet.")

    async def fetch(self, opportunity_id: str) -> Optional[GrowthOpportunity]:
        raise NotImplementedError("Community fetch not implemented yet.")

    async def health(self) -> bool:
        return True

    def supports(self, opportunity_type: OpportunityType) -> bool:
        return opportunity_type in (OpportunityType.COMMUNITY, OpportunityType.EVENT)

    def get_provider_name(self) -> str:
        return "Community"
