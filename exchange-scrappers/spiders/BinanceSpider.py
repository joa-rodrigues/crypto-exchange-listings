import json

import scrapy


class BinanceSpider(scrapy.Spider):
    name = 'binance_spider'

    custom_settings = {
        'ITEM_PIPELINES': {
            'exchange-scrappers.pipelines.BinanceScrapper': 400
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            "exchange-scrappers.middlewares.BinanceMiddleware": 1,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        }
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'referer': 'https://www.paris-turf.com/programme-courses'
    }

    def start_requests(self):
        yield scrapy.Request(url="http://", meta=None, dont_filter=True, callback=self.parse_it)

    def parse_it(self, response):
        data = json.loads(response.text)

        table_item = []
        for crypto_currency in data:
            crypto_currency_dict = {
                "baseAsset": crypto_currency["baseAsset"],
                "quoteAsset": crypto_currency["quoteAsset"],
                "symbol": crypto_currency["symbol"]
            }
            table_item.append(crypto_currency_dict)

        parse_items = {
            'value': table_item
        }

        yield parse_items
