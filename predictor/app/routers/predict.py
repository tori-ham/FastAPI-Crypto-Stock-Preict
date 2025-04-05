import traceback
from fastapi import APIRouter, HTTPException

from core.alpha_vantage_client import getPricesForInterval
from core.predictor import predictTrend

from models.PredictStockModel import PredictStockTrendRequest

router = APIRouter()

@router.get("/stockTrend")
def predictStockTrend(
    requestData : PredictStockTrendRequest
) :
    try:
        prices = getPricesForInterval(requestData.symbol)
        print("prices", prices)
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