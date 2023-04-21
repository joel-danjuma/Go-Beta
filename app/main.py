from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, user, auth, provider, admin, ride, booking

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(provider.router)
app.include_router(admin.router)
app.include_router(ride.router)
app.include_router(booking.router)


# Root page for the api
@app.get("/")
def root():
    return {"Welcome to Go beta": "Ride as You want Am !!!!"}
