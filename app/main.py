from fastapi import FastAPI, Depends
from app.core.config import settings
from app.core.dependencies import get_current_user
from app.api.routes import auth 

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {
        "app": settings.app_name,
        "environment": settings.env,
        "status": "running"
    }


@app.get("/protected")
def protected_route(
    current_user=Depends(get_current_user)
):
    return {
        "message": "Protected route accessed",
        "user": current_user,
    }
