"""API dependencies."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db

# Create a reusable dependency annotation
DatabaseSession = Annotated[Session, Depends(get_db)]

# Type annotation for cleaner dependency injection
CurrentUser = Annotated[dict, Depends(get_current_user)]
