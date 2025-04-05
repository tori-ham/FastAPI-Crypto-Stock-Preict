from apsheduler.schedulers.blocking import BlockingScheduler
from stock_collector import collectStock

scheduler = BlockingScheduler()

@scheduler.scheduled_job("interval", minutes = 5)
def scheduledJob():
    collectStock("TSLA")

if __name__ == "__main__":
    print("Starting Scheduler...")
    scheduler.start()