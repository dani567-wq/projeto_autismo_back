from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.users.models import User
from app.shared.db.database import get_session
from app.shared.security import get_current_user

# Aliases de dependency para reduzir repetição nas assinaturas
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
