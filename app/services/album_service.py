from sqlalchemy.orm import Session
from app.repositories.album_repo import AlbumRepository
from app.repositories.couple_repo import CoupleRepository
from app.models.album import Album
from app.core.exceptions import NotFoundError, ForbiddenError
from app.schemas.common import PaginatedResponse
from app.schemas.album import AlbumResponse

class AlbumService:
    def __init__(self, db: Session):
        self.repo = AlbumRepository(db)
        self.couple_repo = CoupleRepository(db)
        
    
    def _get_couple_and_assert_member(self, user_id: str):
        couple = self.couple_repo.get_couple_of_user(user_id)
        if not couple:
            raise ForbiddenError("Você não pertence a nenhum casal")
        
        return couple
    
    def create(self, user_id: str, title: str, description: str | None) -> Album:
        couple = self._get_couple_and_assert_member(user_id)
        return self.repo.create(couple.id, title, description)
    
    def list(self, user_id: str, page: int, page_size: int) -> PaginatedResponse:
        couple = self._get_couple_and_assert_member(user_id)
        skip = (page -1) * page_size
        items, total = self.repo.list_by_couple(couple.id, skip, page_size)
        return PaginatedResponse(
            items=[AlbumResponse.model_validate(a) for a in items],
            total=total,
            page=page,
            page_size=page_size,
            has_next=(skip + page_size) < total
        )
        
    def get(self, user_id: str, album_id: str) -> Album:
        album = self.repo.get_by_id(album_id)
        if not album:
            raise NotFoundError("Album")
        if not self.couple_repo.user_is_member(album.couple_id, user_id):
            raise ForbiddenError()
        return album
    
    def update(self, user_id: str, album_id: str, **kwargs) -> Album:
        album = self.get(user_id, album_id)
        return self.repo.update(album, **kwargs)

    def delete(self, user_id: str, album_id:str) -> None:
        album = self.get(user_id, album_id)
        self.repo.delete(album)        