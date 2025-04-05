from pydantic import BaseModel

class SimplePredictAssetTrendRequest(BaseModel):
    symbol : str

class SimpleAssetRequest(BaseModel):
    asset : str