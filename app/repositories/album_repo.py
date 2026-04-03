from sqlalchemy.orm import Session
from app.models.album import Album

class AlbumRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, album_id: str) -> Album | None:
        return self.db.get(Album, album_id)
    
    def list_by_couple(self, couple_id: str, skip: int = 0, limit: int = 20) -> tuple[list[Album], int]:
        q = self.db.query(Album).filter(Album.couple_id == couple_id)
        total = q.count()
        items = q.order_by(Album.created_at.desc()).offset(skip).limit(limit).all()
        return items, total
    
    def create(self, couple_id: str, title: str, description: str | None) -> Album:
        album = Album(couple_id = couple_id, title=title, description = description)
        self.db.add(album)
        self.db.commit()
        self.db.refresh(album)
        return album
    
    def update(self, album: Album, **kwargs) -> Album:
        allowed_fields = {"title", "description"}
        
        for k, v in kwargs.items():
            if k in allowed_fields and v is not None:
                setattr(album, k,v)
        self.db.commit()
        self.db.refresh(album)
        return album
    
    def delete(self, album: Album) -> None:
        self.db.delete(album)
        self.db.commit()