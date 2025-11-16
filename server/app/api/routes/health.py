from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["health"])
async def health_check() -> dict:
    """Simple health check endpoint."""
    return {"status": "healthy"}


