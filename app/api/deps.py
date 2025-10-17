"""API dependencies."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user, get_user_permissions
from app.db.session import get_db

DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[dict, Depends(get_current_user)]
UserPermissions = Annotated[list, Depends(get_user_permissions)]
