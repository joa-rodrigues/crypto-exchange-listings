from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.CoinbaseSpider import CoinbaseSpider
from spiders.BinanceSpider import BinanceSpider

process = CrawlerProcess(get_project_settings())
scheduler = TwistedScheduler()
scheduler.add_job(process.crawl, 'interval', args=[CoinbaseSpider, BinanceSpider], seconds=60)
scheduler.start()
process.start(False)
