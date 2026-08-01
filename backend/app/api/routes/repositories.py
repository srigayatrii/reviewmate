from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.services.repository_service import RepositoryService

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"]
)


@router.get("/sync")
async def sync_repositories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    service = RepositoryService(
        db=db,
        current_user=current_user
    )

    result = await service.sync_repositories()

    return result


@router.get("")
async def list_repositories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    service = RepositoryService(
        db=db,
        current_user=current_user
    )

    return await service.get_repositories()


@router.get("/sync")
async def sync_repositories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    service = RepositoryService(
        db=db,
        current_user=current_user
    )

    result = await service.sync_repositories()

    return result

@router.get("/{repository_id}")
async def get_repository(
    repository_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    service = RepositoryService(
        db=db,
        current_user=current_user
    )

    return await service.get_repository(repository_id)


@router.post("/{repository_id}/connect")
async def connect_repository(
    repository_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    service = RepositoryService(
        db=db,
        current_user=current_user
    )

    return await service.connect_repository(repository_id)

@router.post("/{repository_id}/disconnect")
async def disconnect_repository(
    repository_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    service = RepositoryService(
        db=db,
        current_user=current_user
    )

    return await service.disconnect_repository(repository_id)