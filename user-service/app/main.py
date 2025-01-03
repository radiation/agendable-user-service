from app.api.routes import auth_routes, user_routes
from fastapi import FastAPI

app = FastAPI(title="User Service", version="1.0.0")

# Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "User Service is running"}
