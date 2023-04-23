from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, crud, utils, oauth2
from typing import List

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_bookings(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    bookings = crud.get_all_bookings(db)
    return bookings


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_booking_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    booking = crud.get_booking_by_id(id, db).first()
    if booking == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id: {id} does not exist.",
        )
    return booking


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    booking = crud.get_booking_by_id(id, db).first()
    if booking == None:
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
            detail=f"User:{id} has no bookings.",
        )
    return bookings


@router.post("/book_ride", status_code=status.HTTP_201_CREATED)
def book_ride(
    booking: schemas.CreateBooking,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    response_model=schemas.Booking,
):
    ride = crud.get_ride_by_id(booking.ride_id, db).first()
    if ride is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found"
        )
    ride.available_seats = int(ride.available_seats)
    if booking.reserved_seats > ride.available_seats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough available seats"
        )
    ride.available_seats -= booking.reserved_seats
    db.commit()
    new_booking = crud.create_booking(booking, current_user, db)
    return new_booking
