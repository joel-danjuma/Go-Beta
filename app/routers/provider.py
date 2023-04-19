from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas, crud, oauth2, utils
from typing import List

router = APIRouter(prefix="/provider", tags=["Provider"])


# get all providers
@router.get("/", response_model=List[schemas.Provider])
def get_providers(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_provider),
):
    # if current_user.role not in ["admin", "provider"]:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot perform this action")
    providers = crud.get_all_providers(db)
    return providers


# create a new provider
@router.post(
    "/sign-up", status_code=status.HTTP_201_CREATED, response_model=schemas.Provider
)
def create_provider(provider: schemas.CreateProvider, db: Session = Depends(get_db)):
    provider.password = utils.hash(provider.password)
    db_provider = crud.get_provider_by_email(provider.email, db).first()
    if db_provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The provider already exists",
        )
    new_provider = crud.create_provider(provider, db)
    return new_provider
