from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, crud, utils, oauth2
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])


# get all users
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def get_users(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    users = crud.get_all_users(db)
    return users


# get one user by id
@router.get("/{id}", response_model=schemas.User)
def get_users_by_id(id: int, db: Session = Depends(get_db)):
    user = crud.get_users_by_id(id, db)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found.",
        )
    return user.first()


# get a users email by id
@router.get("/email/{id}")
def get_users_email_by_id(id: int, db: Session = Depends(get_db)):
    user = crud.get_users_by_id(id, db)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found.",
        )
    return user.first().email


# get a users id by email
@router.get("/{id}/email")
def get_users_id_by_email(email: str, db: Session = Depends(get_db)):
    user = crud.get_users_by_email(email, db).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found.",
        )
    return user.id


# create a new user
@router.post(
    "/sign-up", status_code=status.HTTP_201_CREATED, response_model=schemas.User
)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    db_user = crud.get_users_by_email(user.email, db).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The user already exists"
        )
    new_user = crud.create_user(user, db)
    return new_user


# delete a user by its id
@router.delete("users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    if current_user != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot perform this action",
        )
    user = crud.get_users_by_id(id, db)
    if user.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist.",
        )
    user.delete(synchronize_session=False)
    db.commit()


# update users email by its id
@router.put("/email/{id}", response_model=schemas.User)
def update_users_email_by_id(
    id: int,
    user: schemas.UpdateUserEmail,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    user_query = crud.get_users_by_id(id, db)
    if user_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found",
        )
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()


# update users password by email
@router.put("/password/{email}", response_model=schemas.User)
def update_users_password_by_email(
    email: str,
    user: schemas.CreateUser,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    user.password = utils.hash(user.password)
    user_query = crud.get_users_by_email(user.email, db)
    if user_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found",
        )
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    # print("New user password is: " + user_query.first().password) for testing purposes only, never reaveal user password!!
    return user_query.first()
