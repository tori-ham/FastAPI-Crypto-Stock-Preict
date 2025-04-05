import traceback
from fastapi import APIRouter, HTTPException

from core.alpha_vantage_client import getPricesForInterval
from core.predictor import predictTrend
from core.cache import getCachedPrices, setCachedPrices

from models.PredictStockModel import PredictStockTrendRequest

router = APIRouter()

@router.get("/stockTrend")
def predictStockTrend(
    requestData : PredictStockTrendRequest
) :
    try:
        symbol = requestData.symbol.upper()
        
        cached = getCachedPrices(symbol)
        if cached :
            prices = cached
        else :
            prices = getPricesForInterval(symbol)
            setCachedPrices(symbol, prices)
        prediction = predictTrend(prices)
        return {
            "symbol" : requestData.symbol,
            "prediction" : "UP" if prediction == 1 else "DOWN",
            "last_price" : prices[-1]
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code = 400,
            detail = str(e)
        )