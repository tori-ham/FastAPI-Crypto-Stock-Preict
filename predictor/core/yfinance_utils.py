import yfinance as yf

def isValidYFinanceSymbol( symbol : str ) -> bool:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return "shortName" in info and info["regularMarketPrice"] is not None
    except Exception as e:
        return False