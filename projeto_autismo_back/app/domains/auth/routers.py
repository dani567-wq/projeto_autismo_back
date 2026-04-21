from fastapi import APIRouter
from sqlalchemy import select

from app.dependencies import CurrentUser, OAuth2Form, Session
from app.domains.auth.schemas import Token
from app.domains.users.models import User
from app.shared.errors import errors
from app.shared.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2Form, session: Session):
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.password):
        raise errors.INCORRECT_CREDENTIALS

    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: CurrentUser):
    new_access_token = create_access_token(data={'sub': user.email})
    return {'access_token': new_access_token, 'token_type': 'bearer'}
