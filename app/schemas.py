from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# POSTS
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    pass


# USERS
class UserBase(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr
    phone: str
    name: str
    created_at: datetime

    class Config:
        orm_mode = True


class CreateUser(UserBase):
    phone: str
    name: str


class UpdateUserPassword(BaseModel):
    password: str


class UpdateUserEmail(BaseModel):
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# RIDES
class Ride(BaseModel):
    id: int
    origin: str
    destination: str
    vehicle_type: str
    avaialble_seats: int
    provider_id: int
    depature_time: datetime
    arrival_time: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class CreateRide(BaseModel):
    origin: str
    destination: str
    vehicle_type: str
    avaialble_seats: int
    provider_id: int
    depature_time: datetime
    arrival_time: datetime


# PROVIDERS
class ProviderBase(BaseModel):
    email: EmailStr
    password: str


class Provider(BaseModel):
    id: int
    name: str
    address: str
    email: EmailStr
    government_id: str

    class Config:
        orm_mode = True


class CreateProvider(ProviderBase):
    name: str
    address: str
    government_id: str


# BOOKINGS
class Booking(BaseModel):
    id: int
    owner_id: int
    ride_id: int
    reserved_seats: int
    created_at: datetime

    class Config:
        orm_mode = True


class CreateBooking(BaseModel):
    owner_id: int
    ride_id: int
    reserved_seats: int


# AUTH
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str = None


# ADMIN
class Admin(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class CreateAdmin(BaseModel):
    email: EmailStr
    password: str
