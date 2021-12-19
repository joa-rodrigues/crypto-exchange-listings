#!/bin/bash

cd /media/usbdrive/dev/crypto-exchange-listings/exchange-scrappers/
PATH=$PATH:/usr/local/bin
export PATH

scrapy crawl  coinbase_spider