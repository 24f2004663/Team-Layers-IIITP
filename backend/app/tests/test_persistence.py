import pytest
import pytest_asyncio
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.infrastructure.database.base import (
    Base,
    User,
    IdentityProfile,
    Goal,
    Skill,
    BehaviorProfile,
    DailyPlan,
    Resource,
    Recommendation,
    Reflection,
    Progress
)
from app.repositories.user_repository import UserRepository
from app.repositories.identity_repository import IdentityRepository
from app.ai.memory.identity.manager import SQLIdentityMemoryManager
from app.ai.memory.behavior.manager import SQLBehaviorMemoryManager
from app.ai.memory.progress.manager import SQLProgressMemoryManager
from app.ai.memory.semantic.manager import MockSemanticMemoryManager
from app.ai.memory.session.manager import MockSessionMemoryManager

# db_session fixture is resolved automatically from conftest.py

@pytest.mark.asyncio
async def test_database_connection_and_session_lifecycle(db_session: AsyncSession):
    """Verifies that the session can execute simple queries and transactions."""
    assert db_session.is_active
    # Basic execute check
    from sqlalchemy.sql import text
    res = await db_session.execute(text("SELECT 1"))
    assert res.scalar() == 1

@pytest.mark.asyncio
async def test_repository_crud_operations(db_session: AsyncSession):
    """Verifies CRUD lifecycle on UserRepository and IdentityRepository."""
    user_repo = UserRepository(db_session)
    identity_repo = IdentityRepository(db_session)
    
    # 1. Create User
    user_data = {
        "email": "test@lifegps.ai",
        "full_name": "Test User",
        "hashed_password": "secure_password"
    }
    user = await user_repo.create(user_data)
    assert user.id is not None
    assert user.email == "test@lifegps.ai"
    
    # 2. Get User
    fetched_user = await user_repo.get(user.id)
    assert fetched_user is not None
    assert fetched_user.full_name == "Test User"
    
    # 3. Create Identity Profile matching user
    profile_data = {
        "user_id": user.id,
        "archetype": "Growth Hacker",
        "core_values": ["Adaptability", "Learning"],
        "strengths": ["Perseverance"],
        "weaknesses": ["Patience"]
    }
    profile = await identity_repo.create(profile_data)
    assert profile.id is not None
    assert profile.user_id == user.id
    
    # 4. List and Update
    users = await user_repo.list()
    assert len(users) == 1
    
    await user_repo.update(user.id, {"full_name": "Updated User"})
    updated_user = await user_repo.get(user.id)
    assert updated_user.full_name == "Updated User"
    
    # 5. Delete and Exists check
    assert await user_repo.exists(user.id)
    await user_repo.delete(user.id, soft=True)
    assert not await user_repo.exists(user.id)  # Soft deleted is filtered out by default

@pytest.mark.asyncio
async def test_identity_memory_manager(db_session: AsyncSession):
    """Verifies interface compliance and CRUD on IdentityMemoryManager."""
    user_repo = UserRepository(db_session)
    user = await user_repo.create({"email": "identity@lifegps.ai"})
    
    manager = SQLIdentityMemoryManager(db_session)
    
    # Save profile
    save_success = await manager.save(user.id, {
        "archetype": "Achiever",
        "core_values": ["Discipline"],
        "strengths": ["Focus"],
        "weaknesses": ["Overwork"]
    })
    assert save_success
    
    # Load profile
    profile = await manager.load(user.id)
    assert profile["archetype"] == "Achiever"
    assert "Discipline" in profile["core_values"]
    
    # Search profile values
    results = await manager.search(user.id, "achieve")
    assert len(results) == 1
    assert results[0]["field"] == "archetype"
    
    # Summarize profile values
    summary = await manager.summarize(user.id)
    assert "Achiever" in summary

@pytest.mark.asyncio
async def test_mock_memory_managers():
    """Verifies Semantic and Session mock memory manager behaviors."""
    user_id = uuid4()
    
    # Semantic
    semantic_mgr = MockSemanticMemoryManager()
    await semantic_mgr.save(user_id, {"content": "Deep focus state is critical for growth."})
    nodes = await semantic_mgr.load(user_id)
    assert len(nodes["nodes"]) == 1
    
    search_res = await semantic_mgr.search(user_id, "focus")
    assert len(search_res) == 1
    
    # Session
    session_mgr = MockSessionMemoryManager()
    await session_mgr.save(user_id, {"chat_state": "active_chat"})
    session_data = await session_mgr.load(user_id)
    assert session_data["chat_state"] == "active_chat"
