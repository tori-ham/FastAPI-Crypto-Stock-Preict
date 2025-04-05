import traceback
from fastapi import APIRouter, HTTPException

from core.alpha_vantage_client import getPricesForInterval
from core.binance_client import getBinancePrices, getBinanceSymbolPairs
from core.predictor import predictSimpleTrend
from core.cache import getCachedPrices, setCachedPrices

from models.SimplePredictAssetModel import SimplePredictAssetTrendRequest

router = APIRouter()

@router.get("/stockTrend")
def predictStockTrend(
    requestData : SimplePredictAssetTrendRequest
) :
    try:
        symbol = requestData.symbol.upper()
        
        cached = getCachedPrices(symbol)
        if cached :
            prices = cached
        else :
            prices = getPricesForInterval(symbol)
            setCachedPrices(symbol, prices)
        prediction = predictSimpleTrend("stock", prices)
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

@router.get("/cryptoTrend")
def predictCryptoTrend(
    requestData : SimplePredictAssetTrendRequest
):
    try :
        symbol = requestData.symbol.upper()
        
        valid_symbols = getBinanceSymbolPairs("USDT")
        if symbol not in valid_symbols:
            raise HTTPException(
                status_code = 400,
                detail = f"Invalid Symbol : {symbol}"
            )
        
        cached = getCachedPrices(symbol)
        if cached:
            prices = cached
        else:
            prices = getBinancePrices(symbol)
            setCachedPrices(symbol, prices)
        prediction = predictSimpleTrend("crypto", prices)
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