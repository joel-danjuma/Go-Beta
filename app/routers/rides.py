from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, crud, utils, oauth2
from typing import List


router = APIRouter(prefix="/rides", tags=["Rides"])


# get all rides
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Ride])
def get_rides(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    rides = crud.get_all_rides(db)
    return rides


# get one ride by id
@router.get("/{id}", response_model=schemas.Ride)
def get_ride_by_id(id: int, db: Session = Depends(get_db)):
    ride = crud.get_ride_by_id(id, db)
    if not ride.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ride with id: {id} was not found.",
        )
    return ride.first()


# create a new ride
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Ride)
def create_ride(ride: schemas.CreateRide, db: Session = Depends(get_db)):
    db_ride = crud.get_ride_by_id(ride.id, db)
    if db_ride:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The ride already exists",
        )
    new_ride = crud.create_ride(ride, db)
    return new_ride


# update a ride
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Ride)
def update_ride(id: int, ride: schemas.CreateRide, db: Session = Depends(get_db)):
    db_ride = crud.get_ride_by_id(id, db)
    if not db_ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ride with id: {id} was not found.",
        )
    updated_ride = crud.update_ride(id, ride, db)
    return updated_ride


# delete a ride
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ride(id: int, db: Session = Depends(get_db)):
    db_ride = crud.get_ride_by_id(id, db)
    if not db_ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ride with id: {id} was not found.",
        )
    crud.delete_ride(id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# get all rides for a user
@router.get(
    "/user/{id}", status_code=status.HTTP_200_OK, response_model=List[schemas.Ride]
)
def get_rides_by_user_id(id: int, db: Session = Depends(get_db)):
    rides = crud.get_rides_by_user_id(id, db)
    if not rides:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"rides for user with id: {id} were not found.",
        )
    return rides


# get all rides for a provider
@router.get(
    "/provider/{id}", status_code=status.HTTP_200_OK, response_model=List[schemas.Ride]
)
def get_rides_by_provider_id(id: int, db: Session = Depends(get_db)):
    rides = crud.get_rides_by_provider_id(id, db)
    if not rides:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"rides for provider with id: {id} were not found.",
        )
    return rides
