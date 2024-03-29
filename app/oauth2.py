from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
from . import schemas, database, crud
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/user")
oauth2_scheme_provider = OAuth2PasswordBearer(tokenUrl="login/provider")
oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="login/admin")

load_dotenv()
secret_key = os.environ["SECRET_KEY"]
algorithm = os.environ["ALGORITHM"]
access_token_expire_minutes = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def verify_access_token(token: str, user_type: str, credentials_exception):
    try:
        payload = jwt.decode(token, secret_key, [algorithm])
        id: str = payload.get(f"{user_type}_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code =status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"})
    token_data = verify_access_token(token, "user", credentials_exception)
    user = crud.get_users_by_id(token_data.id, db).first()
    return user.id

def get_current_provider(token: str = Depends(oauth2_scheme_provider), db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code =status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"})
    token_data = verify_access_token(token, "provider", credentials_exception)
    provider = crud.get_provider_by_id(token_data.id, db).first()
    return provider.id

def get_current_admin(token: str = Depends(oauth2_scheme_admin), db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code =status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"})
    token_data = verify_access_token(token, "admin", credentials_exception)
    admin = crud.get_admin_by_id(token_data.id, db).first()
    return admin.id
