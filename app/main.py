from fastapi import FastAPI

from app.api.routes import auth_routes, group_routes, role_routes, user_routes
from app.exceptions import (
    ForbiddenError,
    NotFoundError,
    ValidationError,
    forbidden_exception_handler,
    generic_exception_handler,
    not_found_exception_handler,
    validation_exception_handler,
)

app = FastAPI(title="User Service", version="1.0.0")

# Register exception handlers
app.add_exception_handler(ForbiddenError, forbidden_exception_handler)
app.add_exception_handler(NotFoundError, not_found_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(group_routes.router, prefix="/groups", tags=["groups"])
app.include_router(role_routes.router, prefix="/roles", tags=["roles"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "User Service is running"}
