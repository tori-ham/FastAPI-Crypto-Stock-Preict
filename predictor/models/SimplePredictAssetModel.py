from pydantic import BaseModel

class SimplePredictAssetTrendRequest(BaseModel):
    symbol : str