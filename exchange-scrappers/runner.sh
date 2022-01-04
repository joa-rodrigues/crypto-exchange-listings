#!/bin/bash

cd /media/usbdrive/dev/crypto-exchange-listings/exchange-scrappers/
PATH=$PATH:/usr/local/bin
export PATH

export PYTHONPATH="${PYTHONPATH}:/media/usbdrive/dev/crypto-exchange-listings/exchange-scrappers/"

scrapy crawl  coinbase_spider
scrapy crawl  binance_spider