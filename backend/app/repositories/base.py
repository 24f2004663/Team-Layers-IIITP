from typing import Generic, TypeVar, Type, List, Optional, Any, Dict
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, exists
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """Generic async repository implementing standard CRUD operations with soft delete support."""

    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        """Initializes the repository.
        
        Args:
            model: The SQLAlchemy model class.
            db_session: Active database AsyncSession.
        """
        self.model = model
        self.db = db_session

    async def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """Creates a new record.
        
        Args:
            obj_in: Attributes to initialize the model.
            
        Returns:
            ModelType: The created database record.
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def get(self, id: UUID, include_deleted: bool = False) -> Optional[ModelType]:
        """Retrieves a single record by its UUID.
        
        Args:
            id: The primary key UUID.
            include_deleted: If true, will retrieve soft deleted objects.
            
        Returns:
            Optional[ModelType]: The found model object or None.
        """
        query = select(self.model).where(self.model.id == id)
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        result = await self.db.execute(query)
        return result.scalars().first()

    async def list(self, skip: int = 0, limit: int = 100, include_deleted: bool = False) -> List[ModelType]:
        """Lists records with pagination support.
        
        Args:
            skip: Count of records to offset.
            limit: Maximum count of records to fetch.
            include_deleted: If true, lists soft-deleted objects.
            
        Returns:
            List[ModelType]: List of found records.
        """
        query = select(self.model).offset(skip).limit(limit)
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, id: UUID, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """Updates an existing active record.
        
        Args:
            id: Target record ID.
            obj_in: Fields and values to update.
            
        Returns:
            Optional[ModelType]: The updated record or None.
        """
        db_obj = await self.get(id)
        if not db_obj:
            return None
        
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
            
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def delete(self, id: UUID, soft: bool = True) -> bool:
        """Deletes a record.
        
        Args:
            id: Target record ID.
            soft: If true, performs a soft delete setting deleted_at timestamp.
            
        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        db_obj = await self.get(id)
        if not db_obj:
            return False
            
        if soft:
            from datetime import timezone
            db_obj.deleted_at = datetime.now(timezone.utc)
            self.db.add(db_obj)
        else:
            await self.db.delete(db_obj)
            
        await self.db.flush()
        return True

    async def exists(self, id: UUID, include_deleted: bool = False) -> bool:
        """Checks if a record exists.
        
        Args:
            id: Target record ID.
            include_deleted: If true, checks soft-deleted objects as well.
            
        Returns:
            bool: True if exists, False otherwise.
        """
        query = select(exists().where(self.model.id == id))
        if not include_deleted:
            query = query.where(self.model.deleted_at.is_(None))
        result = await self.db.execute(query)
        return bool(result.scalar())
