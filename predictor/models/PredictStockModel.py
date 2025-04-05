from pydantic import BaseModel

class PredictStockTrendRequest(BaseModel):
    symbol : str