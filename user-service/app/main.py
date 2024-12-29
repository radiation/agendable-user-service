import os

from app.api.routes import auth, users
from fastapi import FastAPI

app = FastAPI(title="User Service", version="1.0.0")

# Access the secret key
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables!")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "User Service is running"}
