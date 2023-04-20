from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, crud, utils, oauth2
from typing import List

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_bookings(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    bookings = crud.get_all_bookings
    return bookings


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_booking_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    booking = crud.get_booking_by_id(id, db)
    if booking.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id: {id} does not exist.",
        )
    return booking.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    booking = crud.get_booking_by_id(id, db)
    if booking.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id: {id} does not exist.",
        )
    booking.delete(synchronize_session=False)
    db.commit()


@router.get("/user/{id}", status_code=status.HTTP_200_OK)
def get_bookings_by_user_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    bookings = crud.get_bookings_by_user_id(id, db)
    if bookings.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id: {id} does not exist.",
        )
    return bookings


@router.post("/ride", status_code=status.HTTP_201_CREATED)
def book_ride(
    ride: schemas.Ride,
    booking: schemas.CreateBooking,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    response_model=schemas.Booking,
):
    ride = crud.get_ride_by_provider_id(ride.provider_id, db).first()
    if ride is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found"
        )
    if booking.reserved_seats > ride.available_seats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough available seats"
        )
    new_booking = crud.create_booking(booking, current_user, db)
    return new_booking
