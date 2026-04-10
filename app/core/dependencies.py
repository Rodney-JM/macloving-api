from typing import Annotated
from uuid import UUID
from fastapi import Depends, Header, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import Settings
from app.core.exceptions