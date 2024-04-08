from fastapi import APIRouter
from .distance import router as distance_router

router = APIRouter(
    prefix="/sensor",
    tags=["sensor"],
    responses={404: {"description": "Not found"}},
)

# router.include_router(distance_router)
