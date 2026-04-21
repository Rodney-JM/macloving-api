import hashlib
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select

from app.domain.models.couple_models.refresh_token import RefreshToken
from app.infra.repositories.base import BaseRepository

class RefreshTokenRepository(BaseRepository[RefreshToken]):
    model = RefreshToken
    
    @staticmethod
    def _hash(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()
    
    async def get_valid_token(self, raw_token: str) -> RefreshToken | None:
        token_hash = self._hash(raw_token)
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked == False,
                RefreshToken.expires_at > now
            )
        )
        return result.scalar_one_or_none()
    
    async def revoke_all_for_user(self, user_id: UUID) -> None:
        tokens = await self.get_all(filters=[RefreshToken.user_id==user_id, RefreshToken.revoked == False])
        for t in tokens:
            t.revoked = True
        
        await self.session.flush()
        
    def create(
        self, 
        *,
        user_id: UUID,
        raw_token: str,
        expires_at: datetime,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> RefreshToken:
        token = RefreshToken(
            user_id=user_id,
            token_hash=self._hash(raw_token),
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip_address
        )
        
        self.session.add(token)
        return token