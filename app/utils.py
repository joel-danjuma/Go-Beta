from passlib.context import CryptContext
from fastapi import HTTPException, status

# import requests

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# create a function called send_booking_to_provider that takes a provider and a new booking and sends the new booking to the provider
# def send_booking_to_provider(provider, new_booking):
#     # create a new booking object
#     booking = {
#         "id": new_booking.id,
#         "ride_id": new_booking.ride_id,
#         "owner_id": new_booking.owner_id,
#         "reserved_seats": new_booking.reserved_seats,
#         "status": new_booking.status,
#     }
#     # send the booking to the provider
#     response = requests.post(f"{provider.service_url}/bookings/new", json=booking)
#     # check if the response is ok
#     if response.status_code != 200:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Could not send booking to provider",
#         )
#     # return the response
#     return response
