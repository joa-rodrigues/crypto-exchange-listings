import scrapy

class CryptoCurrencyItem(scrapy.Item):
    value = scrapy.Field()


