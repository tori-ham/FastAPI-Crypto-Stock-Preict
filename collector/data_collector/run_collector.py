# load for STOCK, CRYPTO
from config import STOCK_SYMBOLS, CRYPTO_SYMBOLS
# load for NEWS
from config import NEWS_RSS_COUNTRIES, NEWS_RSS_NICKNAMES, NEWS_RSS_QUERY
from stock_collector import collectStock, collectStockToParquet
from crypto_collector import collectCrypto, collectCryptoToParquet
from news_collector import collectNews, summaryNews, analyzeSummarySentiment
from eco_ind_collector import getEconomicIndicatorData

if __name__ == "__main__":
    # for symbol in STOCK_SYMBOLS:
    #     collectStock(symbol)
    # for symbol in CRYPTO_SYMBOLS:
    #     collectCrypto(symbol)
    # collectStockToParquet("TSLA")
    # collectCryptoToParquet("BTCUSDT")
    # for country in NEWS_RSS_COUNTRIES:
    #     for i in range(1, 3):
    #         k = f"{country}_{i}"
    #         collectNews(NEWS_RSS_QUERY[k], country, NEWS_RSS_NICKNAMES[k])
    #         summaryNews(country)
    #         analyzeSummarySentiment(country)
    getEconomicIndicatorData()