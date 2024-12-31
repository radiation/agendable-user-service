import os

from app.api.routes import auth_routes, user_routes
from fastapi import FastAPI

app = FastAPI(title="User Service", version="1.0.0")

# Access the secret key
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables!")

# Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "User Service is running"}
