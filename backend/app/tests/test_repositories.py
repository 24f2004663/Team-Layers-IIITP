import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.repositories.identity_repository import IdentityRepository
from app.repositories.behavior_repository import BehaviorRepository
from app.models.user import User
from app.models.identity import IdentityProfile
from app.models.behavior import BehaviorProfile

@pytest.mark.asyncio
async def test_repository_transaction_rollback(db_session: AsyncSession):
    """Verifies database transactions and rollback behavior on exception triggers."""
    user_repo = UserRepository(db_session)
    
    # 1. Start Transaction
    async with db_session.begin_nested():
        test_user = User(
            email="transaction_rollback_test@lifegps.com",
            hashed_password="hashed_pwd_sample",
            full_name="Rollback Tester"
        )
        await user_repo.save(test_user)
        
        # Verify inserted record exists inside nested transaction
        inserted_user = await user_repo.get_by_email("transaction_rollback_test@lifegps.com")
        assert inserted_user is not None
        
        # Trigger simulated exception to force rollback
        try:
            raise ValueError("Simulated database failure")
        except ValueError:
            # Explicit rollback on the nested transaction level
            await db_session.rollback()
            
    # Verify user record is completely rolled back and cleaned from database
    final_user = await user_repo.get_by_email("transaction_rollback_test@lifegps.com")
    assert final_user is None

@pytest.mark.asyncio
async def test_repository_crud_lifecycle(db_session: AsyncSession):
    """Verifies basic Async CRUD capabilities on user and profile repositories."""
    user_repo = UserRepository(db_session)
    identity_repo = IdentityRepository(db_session)
    
    # Create User & Identity Profile
    new_user = User(
        email="crud_test_user@lifegps.com",
        hashed_password="some_hashed_password",
        full_name="CRUD User"
    )
    await user_repo.save(new_user)
    
    identity = IdentityProfile(
        user_id=new_user.id,
        archetype="Architect",
        core_values=["integrity", "craftsmanship"],
        strengths=["problem-solving"],
        weaknesses=["perfectionism"]
    )
    await identity_repo.save(identity)
    
    # Read & Assert
    fetched_user = await user_repo.get(new_user.id)
    assert fetched_user is not None
    assert fetched_user.email == "crud_test_user@lifegps.com"
    
    fetched_identity = await identity_repo.get_by_user_id(new_user.id)
    assert fetched_identity is not None
    assert fetched_identity.archetype == "Architect"
    
    # Update
    identity.archetype = "Principal Architect"
    await identity_repo.update(identity.id, identity)
    
    updated_identity = await identity_repo.get(identity.id)
    assert updated_identity.archetype == "Principal Architect"
    
    # Delete
    await identity_repo.delete(identity.id)
    await user_repo.delete(new_user.id)
    
    deleted_user = await user_repo.get(new_user.id)
    assert deleted_user is None
