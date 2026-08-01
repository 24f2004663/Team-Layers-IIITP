from typing import List
from pydantic import BaseModel, Field

class LearningContext(BaseModel):
    """The normalized conformed context required to curate personalized learning experiences."""

    topic: str = Field(..., description="The main focus topic (e.g. Python Programming)")
    subtopics: List[str] = Field(default_factory=list, description="Subtopic tags")
    required_skills: List[str] = Field(default_factory=list, description="Skills targeted by this focus")
    missing_skills: List[str] = Field(default_factory=list, description="Identified skill gaps")
    difficulty: str = Field(..., description="Target difficulty (Easy, Medium, Hard)")
    preferred_learning_style: str = Field(..., description="User learning style preference (Visual, Project-Based, Reading, Interactive, Research, Discussion)")
    available_time: int = Field(..., description="Available time limit in minutes")
    energy_level: str = Field(..., description="User current energy level (Low, Medium, High)")
    attention_span: int = Field(..., description="User focus attention span in minutes")
    prerequisites: List[str] = Field(default_factory=list, description="List of prerequisite skills")
    learning_goal: str = Field(..., description="Primary learning objective target statement")
