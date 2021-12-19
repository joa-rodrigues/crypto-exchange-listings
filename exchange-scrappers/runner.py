from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.CoinbaseSpider import CoinbaseSpider

process = CrawlerProcess(get_project_settings())
scheduler = TwistedScheduler()
scheduler.add_job(process.crawl, 'interval', args=[CoinbaseSpider], seconds=60)
scheduler.start()
process.start(False)
