from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, crud, utils, oauth2
from typing import List

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

#get all admin users
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Admin])
def get_admin_users(db: Session = Depends(get_db),  current_user : int = Depends(oauth2.get_current_admin)):
    admin = crud.get_all_admin_users(db)
    return admin

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Admin)
def create_admin(admin: schemas.CreateAdmin, db: Session = Depends(get_db)):
    admin.password = utils.hash(admin.password)
    db_admin = crud.get_admin_by_email(admin.email, db).first()
    if db_admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin account already exists")
    new_admin = crud.create_admin(admin,db)
    return new_admin



