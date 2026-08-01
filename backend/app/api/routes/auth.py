import httpx

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.core.config import settings
from app.core.security import create_access_token, verify_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/github/login")
def github_login():
    github_auth_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        "&scope=repo,user"
    )

    return RedirectResponse(url=github_auth_url)


@router.get("/github/callback")
async def github_callback(
    code: str,
    db: Session = Depends(get_db)
):

    # Exchange authorization code for access token
    async with httpx.AsyncClient() as client:

        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={
                "Accept": "application/json"
            },
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code
            }
        )

    token_data = token_response.json()
    print(token_data)

    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=400,
            detail="Failed to obtain access token"
        )

    # Fetch GitHub user profile
    async with httpx.AsyncClient() as client:

        user_response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
        )

    github_user = user_response.json()

    # Check if user already exists
    user = db.query(User).filter(
        User.github_id == github_user["id"]
    ).first()

    # Create new user if not found
    if not user:

        user = User(
            github_id=github_user["id"],
            username=github_user["login"],
            email=github_user.get("email")
                   or f'{github_user["login"]}@github.local',
            avatar_url=github_user["avatar_url"],
            access_token=access_token
        )

        db.add(user)

    # Update existing user
    else:
        user.access_token = access_token
        user.avatar_url = github_user["avatar_url"]

    db.commit()
    db.refresh(user)

    access_token = create_access_token(
    data={
        "sub": str(user.id)
    }
)

    jwt_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )

    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username
        }
    }

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "github_id": current_user.github_id,
        "username": current_user.username,
        "email": current_user.email,
        "avatar_url": current_user.avatar_url,
        "is_active": current_user.is_active,
    }
