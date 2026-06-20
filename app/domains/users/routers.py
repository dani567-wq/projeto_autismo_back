from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.dependencies import CurrentUser, Session
from app.domains.users.models import User
from app.domains.users.schemas import FilterPage, UserList, UserPublic, UserSchema
from app.shared.errors import errors
from app.shared.security import get_password_hash

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/me', response_model=UserPublic)
async def read_current_user(current_user: CurrentUser):
    return current_user


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: Session):
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise errors.USERNAME_TAKEN
        raise errors.EMAIL_TAKEN

    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password,
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
async def read_users(
    session: Session,
    filter_users: Annotated[FilterPage, Query()],
):
    query = await session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    )
    return {'users': query.all()}


@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise errors.INSUFFICIENT_PERMISSIONS

    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        await session.commit()
        await session.refresh(current_user)
        return current_user

    except IntegrityError:
        raise errors.USERNAME_OR_EMAIL_TAKEN


@router.delete('/{user_id}')
async def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise errors.INSUFFICIENT_PERMISSIONS

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted'}
