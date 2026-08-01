import os
from typing import Dict
from app.ai.prompts.loader import PromptLoader
from app.ai.prompts.version import VersionedPrompt
from app.infrastructure.logging.logger import logger

class PromptRegistry:
    """Registry resolving, caching, and serving versioned prompt templates with automatic fallback support."""

    def __init__(self, loader: PromptLoader):
        """Initializes the registry.
        
        Args:
            loader: The PromptLoader instance.
        """
        self.loader = loader
        self._cache: Dict[str, VersionedPrompt] = {}

    def get_prompt(self, agent_folder: str, version: str = "v1") -> VersionedPrompt:
        """Retrieves or loads template from cache, falling back to earlier versions if not found.
        
        Args:
            agent_folder: Subfolder target name.
            version: Target version key (e.g. 'v2').
            
        Returns:
            VersionedPrompt: Loaded versioned template.
            
        Raises:
            FileNotFoundError: If prompt files do not exist and fallback fails.
        """
        cache_key = f"{agent_folder}:{version}"
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        try:
            prompt = self.loader.load_prompt(agent_folder, version)
            self._cache[cache_key] = prompt
            return prompt
        except FileNotFoundError as e:
            if version == "v1":
                raise e
            # Automatic fallback: try to load v1 if v2 or other version fails
            logger.warning(f"Prompt version '{version}' not found for agent '{agent_folder}'. Falling back to 'v1'.", error=str(e))
            fallback_prompt = self.loader.load_prompt(agent_folder, "v1")
            # Cache the fallback result for this key as well to prevent repeated hits
            self._cache[cache_key] = fallback_prompt
            return fallback_prompt
