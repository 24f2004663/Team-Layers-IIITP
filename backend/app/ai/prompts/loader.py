import os
import yaml
from typing import Dict
from app.ai.prompts.base import PromptMetadata
from app.ai.prompts.version import VersionedPrompt

class PromptLoader:
    """Loader loading prompt templates and metadata YAML files from filesystem disks."""

    def __init__(self, base_dir: str):
        """Initializes the loader.
        
        Args:
            base_dir: The directory containing prompt packages (e.g. backend/app/ai/prompts).
        """
        self.base_dir = base_dir

    def load_prompt(self, agent_folder: str, version: str = "v1") -> VersionedPrompt:
        """Reads metadata.yaml and prompt text template from target subfolder.
        
        Args:
            agent_folder: Mapped subfolder name (e.g. 'identity').
            version: Target version key.
            
        Returns:
            VersionedPrompt: Fully loaded template container.
            
        Raises:
            FileNotFoundError: If prompt files do not exist.
        """
        folder_path = os.path.join(self.base_dir, agent_folder)
        meta_path = os.path.join(folder_path, "metadata.yaml")
        template_path = os.path.join(folder_path, f"{version}.md")
        
        if not os.path.exists(meta_path) or not os.path.exists(template_path):
            raise FileNotFoundError(f"Prompt template or metadata missing in folder: '{folder_path}'")
            
        # Parse YAML metadata
        with open(meta_path, "r", encoding="utf-8") as f:
            meta_dict = yaml.safe_load(f)
            
        # Parse template string
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
            
        metadata = PromptMetadata(**meta_dict)
        return VersionedPrompt(metadata=metadata, template=template_content)
