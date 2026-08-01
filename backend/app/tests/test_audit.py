import pytest
from uuid import uuid4
from app.ai.runtime.container import container
from app.ai.framework.errors import ValidationError

@pytest.mark.asyncio
async def test_dicontainer_resolution():
    """Verify that DIContainer resolves all core registries and registered agents correctly."""
    assert container.registry is not None
    assert container.agent_runtime is not None
    
    # Check that agents are registered
    assert "IdentityAgent" in container.registry.list()
    assert "LearningLoopAgent" in container.registry.list()

def test_validation_error_structure():
    """Verify that ValidationError returns structured messaging as required."""
    with pytest.raises(ValidationError) as exc_info:
        raise ValidationError("Test error message context")
    assert "Test error" in str(exc_info.value)
