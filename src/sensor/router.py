from fastapi import APIRouter

router = APIRouter(
    prefix="/sensor",
    tags=["sensor"],
    responses={404: {"description": "Not found"}},
)
