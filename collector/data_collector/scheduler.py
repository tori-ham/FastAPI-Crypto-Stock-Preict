from apsheduler.schedulers.blocking import BlockingScheduler

from config import STOCK_SYMBOLS, CRYPTO_SYMBOLS
from stock_collector import collectStock
from crypto_collector import collectCrypto

scheduler = BlockingScheduler()

@scheduler.scheduled_job("interval", minutes = 5)
def scheduledJob():
    for symbol in STOCK_SYMBOLS:
        collectStock(symbol)
    for symbol in CRYPTO_SYMBOLS:
        collectCrypto(symbol)

if __name__ == "__main__":
    print("Starting Scheduler...")
    scheduler.start()