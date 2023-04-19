from . import models, schemas
from sqlalchemy.orm import Session


# POSTS
def create_post(user_id: int, post: schemas.CreatePost, db: Session):
    new_post = models.Post(owner_id=user_id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all_posts(user_id: int, db: Session):
    return db.query(models.Post).filter(models.Post.owner_id == user_id).all()


def get_post_by_id(id: int, db: Session):
    return db.query(models.Post).filter(models.Post.id == id)


# USERS
def create_user(user: schemas.CreateUser, db: Session):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    return db.query(models.User).all()


def get_users_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email)


def get_users_by_id(id: int, db: Session):
    return db.query(models.User).filter(models.User.id == id)


# PROVIDERS
def create_provider(provider: schemas.CreateProvider, db: Session):
    new_provider = models.Provider(**provider.dict())
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return new_provider


def get_all_providers(db: Session):
    return db.query(models.Provider).all()


def get_provider_by_id(id: int, db: Session):
    return db.query(models.Provider).filter(models.Provider.id == id)


def get_provider_by_email(email: str, db: Session):
    return db.query(models.Provider).filter(models.Provider.email == email)


# ADMIN
def create_admin(admin: schemas.CreateAdmin, db: Session):
    new_admin = models.Admin(**admin.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


def get_all_admin_users(db: Session):
    return db.query(models.Admin).all()


def get_admin_by_id(id: int, db: Session):
    return db.query(models.Admin).filter(models.Admin.id == id)


def get_admin_by_email(email: str, db: Session):
    return db.query(models.Admin).filter(models.Admin.email == email)


# BOOKINGS
def get_all_bookings(db: Session):
    return db.query(models.Booking).all()


def get_bookings_by_id(id: int, db: Session):
    return db.query(models.Booking).filter(models.Booking.id == id).first()


def get_bookings_by_user_id(id: int, db: Session):
    return db.query(models.Booking).filter(models.Booking.user_id == id).all()


def get_booking_by_user(user_id: int, db: Session):
    return db.query(models.Booking).filter(models.Booking.owner_id == user_id)


# RIDES
def get_ride_by_id(ride_id: int, db: Session):
    return db.query(models.Ride).filter(models.Ride.id == ride_id)
