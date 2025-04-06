from config import STOCK_SYMBOLS, CRYPTO_SYMBOLS
from stock_collector import collectStock, collectStockToParquet
from crypto_collector import collectCrypto, collectCryptoToParquet

if __name__ == "__main__":
    # for symbol in STOCK_SYMBOLS:
    #     collectStock(symbol)
    # for symbol in CRYPTO_SYMBOLS:
    #     collectCrypto(symbol)
    collectStockToParquet("TSLA")
    collectCryptoToParquet("BTCUSDT")