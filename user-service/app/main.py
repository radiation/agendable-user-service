from app.api.routes import auth, users
from fastapi import FastAPI

app = FastAPI(title="User Service", version="1.0.0")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

# Create database tables on startup
"""
@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)"""


@app.get("/")
async def root():
    return {"message": "User Service is running"}
