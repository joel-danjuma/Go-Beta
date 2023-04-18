from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, crud, utils, oauth2

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post("/user", response_model=schemas.Token )
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
   user = crud.get_users_by_email(user_credentials.username, db).first()
   if not user:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
   if not utils.verify(user_credentials.password, user.password):
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials") 
   access_token = oauth2.create_access_token(data = {"user_id": user.id})
   return {"access_token" : access_token, "token_type" : "bearer"} 

@router.post("/provider", response_model=schemas.Token )
def provider_login(provider_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
   provider = crud.get_provider_by_email(provider_credentials.username, db).first()
   if not provider:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
   if not utils.verify(provider_credentials.password, provider.password):
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials") 
   access_token = oauth2.create_access_token(data = {"provider_id": provider.id})
   return {"access_token" : access_token, "token_type" : "bearer"} 

@router.post("/admin", response_model=schemas.Token )
def admin_login(admin_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
   admin = crud.get_admin_by_email(admin_credentials.username, db).first()
   if not admin:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
   if not utils.verify(admin_credentials.password, admin.password):
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials") 
   access_token = oauth2.create_access_token(data = {"admin_id": admin.id})
   return {"access_token" : access_token, "token_type" : "bearer"} 
