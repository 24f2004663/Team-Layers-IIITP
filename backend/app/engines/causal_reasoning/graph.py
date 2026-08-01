from typing import List, Dict
from pydantic import BaseModel, Field

class CausalEdge(BaseModel):
    source: str
    target: str
    strength: float

class CausalGraph(BaseModel):
    """Represents a DAG mapping chain relationships of behavior causes."""
    nodes: List[str] = Field(default_factory=list)
    edges: List[CausalEdge] = Field(default_factory=list)
