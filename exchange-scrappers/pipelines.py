import datetime

import pymongo
import telepot
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class CoinbaseScrapper(object):

    def __init__(self):
        mongo_server = settings.get('MONGO_SERVER')

        mongo_url = f"mongodb://{mongo_server['host']}:{mongo_server['port']}/{mongo_server['database']}"
        client = pymongo.MongoClient(mongo_url)
        self.coinbase_crypto_lists = client.get_database().get_collection(mongo_server['coinbase_cryptos_lists'])
        self.coinbase_crypto_reports = client.get_database().get_collection(mongo_server['coinbase_cryptos_reports'])

    def process_item(self, items, spider):
        coinbase_currencies = items["value"]
        coinbase_currencies_keys = (o["id"] for o in coinbase_currencies)

        mongo_currencies = self.coinbase_crypto_lists.find()
        mongo_currencies_keys = (o["key"] for o in mongo_currencies)

        added_currencies = list(set(coinbase_currencies_keys) - set(mongo_currencies_keys))
        removed_currencies = list(set(mongo_currencies_keys) - set(coinbase_currencies_keys))

        # Add or update added currencies
        report = {
            "date": datetime.datetime.today(),
            "added": added_currencies,
            "removed": removed_currencies
        }
        self.coinbase_crypto_reports.insert_one(report)

        # Save added currencies
        for currency in added_currencies:
            self.coinbase_crypto_lists.find_one_and_update(
                {
                    "key": currency,
                },
                {"$set":
                    {
                        "key": currency,
                    }
                }, upsert=True
            )

            # Remove cryptos from database if necessary
            for currency in removed_currencies:
                self.mycol.delete_one(
                    {
                        "key": currency,
                    }
                )

        # send notification if added only
        if added_currencies:
            telegram_bot = settings.get('TELEGRAM_BOT')
            bot = telepot.Bot(telegram_bot['token'])

            message = f"""          
            <b>coinbase listed cryptos : </b> <i>{len(items["value"])}</i>
            <b>added : </b> <i>{added_currencies}</i>
            <b>removed : </b> <i>{removed_currencies}</i>
    
            """

            bot.sendMessage(
                telegram_bot['receiver_id'],
                parse_mode='html',
                text=message
            )

        print("END COINBASE LOOP")


class BinanceScrapper(object):

    def __init__(self):
        mongo_server = settings.get('MONGO_SERVER')

        mongo_url = f"mongodb://{mongo_server['host']}:{mongo_server['port']}/{mongo_server['database']}"
        client = pymongo.MongoClient(mongo_url)
        self.binance_crypto_lists = client.get_database().get_collection(mongo_server['binance_cryptos_lists'])
        self.binance_crypto_reports = client.get_database().get_collection(mongo_server['binance_cryptos_reports'])

    def process_item(self, items, spider):
        binance_pairs = items["value"]
        binance_pairs_keys = (o["symbol"] for o in binance_pairs)

        mongo_pairs = self.binance_crypto_lists.find()
        mongo_pairs_keys = (o["key"] for o in mongo_pairs)

        added_pairs = list(set(binance_pairs_keys) - set(mongo_pairs_keys))
        removed_pairs = list(set(mongo_pairs_keys) - set(binance_pairs_keys))

        # Save report currencies
        report = {
            "date": datetime.datetime.today(),
            "added": added_pairs,
            "removed": removed_pairs
        }
        self.binance_crypto_reports.insert_one(report)

        # Add or update added pairs
        for pair in added_pairs:
            self.binance_crypto_lists.find_one_and_update(
                {
                    "key": pair,
                },
                {"$set":
                    {
                        "key": pair,
                    }
                }, upsert=True
            )

            # Remove pairs from database id necessary
            for pair in removed_pairs:
                self.mycol.delete_one(
                    {
                        "key": pair,
                    }
                )

        # send notification if added only
        if added_pairs:
            telegram_bot = settings.get('TELEGRAM_BOT')
            bot = telepot.Bot(telegram_bot['token'])

            # The fist time we run there is more than 1000 pair, telegram message size is limited
            message = f"""          
                    <b>binance listed pairs : </b> <i>{len(items["value"])}</i>
                    <b>added : </b> <i>{added_pairs[:200]}</i>
                    <b>removed : </b> <i>{removed_pairs}</i>

                    """

            bot.sendMessage(
                telegram_bot['receiver_id'],
                parse_mode='html',
                text=message
            )

        print("END BINANCE LOOP")
