import json
from scrapy import signals
from scrapy.http import TextResponse
from exchanges.coinbase.api import PublicAPI as CBPublicAPI


class CoinbaseMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        api = CBPublicAPI()
        crypto_currencies = api.get_currencies()

        return TextResponse(
            url=request.url,
            status=200,
            body=json.dumps(crypto_currencies).encode('UTF-8'),
            request=request
        )

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
