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

        # Save report currencies
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

            # Save removed currencies
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

        print("END LOOP")
