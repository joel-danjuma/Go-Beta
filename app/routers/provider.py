from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas, crud, oauth2, utils
from typing import List

router = APIRouter(
    prefix="/providers",
    tags=["Provider"]
)

#get all providers
@router.get("/", response_model=List[schemas.Provider])
def get_providers(db: Session = Depends(get_db),  current_provider: int = Depends(oauth2.get_current_provider)):
    providers = crud.get_all_providers(db)
    return providers

#create a new provider
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Provider)
def create_provider(provider: schemas.CreateProvider, db: Session = Depends(get_db)):
    provider.password = utils.hash(provider.password)
    db_provider = crud.get_provider_by_email(provider.email, db)
    if db_provider:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The provider already exists")
    new_provider = crud.create_provider(provider,db)
    return new_provider