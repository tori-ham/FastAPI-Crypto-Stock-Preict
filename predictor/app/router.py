from fastapi import APIRouter
from app.routers import predict

router = APIRouter()
router.include_router( predict.router, prefix="/predict", tags=["predict"] )