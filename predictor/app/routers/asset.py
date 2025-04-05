import traceback
from fastapi import APIRouter, HTTPException

from core.binance_client import getBinanceSymbolPairs

from models.SimplePredictAssetModel import SimpleAssetRequest

router = APIRouter()

@router.get("/cryptoList")
def cryptoAssetSymbols(
    requestData : SimpleAssetRequest
):
    return {
        "symbols" : getBinanceSymbolPairs(requestData.asset.upper())
    }