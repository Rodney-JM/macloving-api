""" from sqlalchemy.orm import Session
from app.domain.models.memory import Memory

class MemoryRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, memory_id: str) -> Memory | None:
        return self.db.get(Memory, memory_id)
    
    def list_by_album(self, album_id: str, skip: int = 0, limit: int = 20) -> tuple[list[Memory], int]:
        q = self.db.query(Memory).filter(Memory.album_id == album_id)
        total = q.count()
        items = (
            q.order_by(Memory.memory_date.desc().nulls_last(), Memory.created_at.desc())
            .offset(skip).limit(limit).all()
        )
        
        return items, total
    
    def create(self, album_id: str, author_id: str, **kwargs) -> Memory:
        memory = Memory(album_id=album_id, author_id=author_id, **kwargs)
        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)
        return memory
    
    def update(self, memory: Memory, **kwargs) -> Memory:
        for k, v in kwargs.items():
            if v is not None:
                setattr(memory, k, v)
        self.db.commit()
        self.db.refresh(memory)
        return memory
    
    def delete(self, memory: Memory) -> None:
        self.db.delete(memory)
        self.db.commit() """