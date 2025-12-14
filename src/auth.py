from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Form
from utils import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from tmp_db import (
    get_redis,
    get_db,
    Users,
    user_schemas,
    auth_schemas,
    fake_users_store,
    fake_redis_store
)
import json

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", summary="регистрация")
async def register_user(
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
) -> str:
    for user in fake_users_store:
        if user.email == email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="exist",
            )

    user = Users(
        first_name=first_name,
        last_name=last_name,
        email=email,
        hashed_password=get_password_hash(password),
    )

    fake_users_store.append(user)

    data = {
        "first_name": first_name,
        "last_name": last_name
    }
    fake_redis_store[email] = json.dumps(data)

    return "ok"


@router.post(
    "/login",
    summary="create tokens",
    response_model=auth_schemas.TokenResponse,  # Теперь это правильная Pydantic модель
)
async def login(
        response: Response,
        email: str = Form(...),
        password: str = Form(...),
):
    user = None
    for u in fake_users_store:
        if u.email == email:
            user = u
            break

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    jwt_data = {"sub": user.email}
    access_token = create_access_token(jwt_data)
    refresh_token = create_refresh_token(jwt_data)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # в секундах
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,  # в секундах
    )

    # Теперь возвращаем Pydantic модель
    return auth_schemas.TokenResponse(
        message="Login successful",
        token_type="bearer"
    )


@router.post('/logout')
async def logout(response: Response):
    response.set_cookie(key="access_token", value="deleted", max_age=0)
    response.set_cookie(key="refresh_token", value="deleted", max_age=0)
    return 'ok'


@router.get('/test-users')
async def get_test_users():
    return [{"email": u.email, "first_name": u.first_name, "last_name": u.last_name} for u in fake_users_store]