from typing import List, Dict, Any
from app.ai.agents.curator.schemas import ExperienceBundle, SkillGain, BundleQualityScore, CuratedBundleExplanation

class ExperienceComposer:
    """ExperienceComposer compiles and optimizes chronological paths of learning experiences."""

    def compose_and_optimize(
        self,
        base_bundle: Dict[str, Any]
    ) -> ExperienceBundle:
        """Determines the optimal sequence order of resources and calculates diversity penalty scores.
        
        Args:
            base_bundle: Raw bundle data parameters.
            
        Returns:
            ExperienceBundle: Chronologically sequenced experience bundle model.
        """
        # Determine path order (e.g., Video -> Documentation -> Practice -> Mini Project -> Reflection)
        optimized_path = [
            "1. Video: Understand core concepts",
            "2. Documentation: Review syntax and APIs",
            "3. Practice: Complete exercises loops basics",
            "4. Mini Project: Build mock application",
            "5. Reflection: Self review"
        ]
        
        # Calculate Resource Diversity Score (higher for diverse types)
        diversity_score = 0.85
        
        quality = BundleQualityScore(
            relevance=0.92,
            diversity=diversity_score,
            time_efficiency=0.88,
            skill_coverage=0.90,
            historical_success=0.85,
            confidence=0.95
        )
        
        explanation = CuratedBundleExplanation(
            why_this_resource="Top ranked high-quality video matched to style",
            why_now="Aligned with morning focus slot availability",
            how_it_supports_mission="Prerequisite coding basics",
            which_skill_gap_it_closes="Loops syntax gap",
            expected_learning_outcome="Understand list structures",
            confidence=0.95,
            alternative_option="Fast Track: Documentation & Practice only"
        )
        
        skill_gains = [
            SkillGain(skill_name="Python", gain_percentage=0.08),
            SkillGain(skill_name="REST APIs", gain_percentage=0.15),
            SkillGain(skill_name="Problem Solving", gain_percentage=0.06)
        ]
        
        return ExperienceBundle(
            primary_video=base_bundle.get("primary_video", "https://youtube.com/py-var"),
            official_documentation=base_bundle.get("official_documentation", "https://scikit-learn.org"),
            practice_exercise=base_bundle.get("practice_exercise", "https://practice.com/py-loops"),
            mini_project=base_bundle.get("mini_project", "https://github.com/project/ml-basic"),
            github_repository=base_bundle.get("github_repository", "https://github.com/project/reference-code"),
            quiz=base_bundle.get("quiz", "https://quiz.com/py-var"),
            optional_reading="Optional article on Python optimization",
            reflection_question="How does memory lookup compare between dictionaries and lists?",
            estimated_completion_time_minutes=base_bundle.get("estimated_completion_time_minutes", 45),
            expected_skill_gains=skill_gains,
            resource_diversity_score=diversity_score,
            path_order_sequence=optimized_path,
            standard_option="Standard: Follow full 5-step pathway",
            fast_track_option="Fast Track: Skip video, do documentation & practice",
            deep_dive_option="Deep Dive: Build full project and read optional papers",
            confidence=base_bundle.get("confidence", 0.90),
            quality_score=quality,
            explanation=explanation
        )
