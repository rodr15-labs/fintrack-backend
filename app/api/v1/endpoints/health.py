from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check():
    """
    Endpoint to verify the health of the API.
    Returns a simple JSON response indicating the status and environment.
    """
    return {
        "status": "available",
        "environment": "development",
    }
