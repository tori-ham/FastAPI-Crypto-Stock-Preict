from fastapi import APIRouter
from app.routers import predict, asset

router = APIRouter()
router.include_router( predict.router, prefix="/predict", tags=["predict"] )
router.include_router( asset.router, prefix="/asset", tags=["asset"])