"""Remotely control your Binance account via their API : https://binance-docs.github.io/apidocs/spot/en"""
"""
Thanks to :
https://github.com/whittlem/pycryptobot/tree/main/models/exchange/binance
"""

import requests
import json


class BinancePublicAPI():

    def __init__(self, api_url="https://api.binance.com") -> None:
        """Binance API object model

        Parameters
        ----------
        api_url
            Binance API URL
        """

        # options
        self.debug = False
        self.die_on_api_error = False

        valid_urls = [
            "https://api.binance.com",
            "https://api.binance.us",
            "https://testnet.binance.vision",
        ]

        # validate Binance API
        if api_url not in valid_urls:
            raise ValueError("Binance API URL is invalid")

        self._api_url = api_url

    def get_exchangeInfo(self):
        """Retrieves the exchange time"""

        try:
            resp = self.authAPI("GET", "/api/v3/exchangeInfo")
            return resp['symbols']
        except Exception as e:
            return None

    def authAPI(self, method: str, uri: str, payload: str = {}) -> dict:
        """Initiates a REST API call to exchange"""

        if not isinstance(method, str):
            raise TypeError("Method is not a string.")

        if not method in ["GET", "POST"]:
            raise TypeError("Method not GET or POST.")

        if not isinstance(uri, str):
            raise TypeError("URI is not a string.")

        try:
            resp = requests.get(f"{self._api_url}{uri}", params=payload)

            if resp.status_code != 200:
                resp_message = resp.json()["msg"]
                message = f"{method} ({resp.status_code}) {self._api_url}{uri} - {resp_message}"
                if self.die_on_api_error:
                    raise Exception(message)
                else:
                    return {}

            resp.raise_for_status()
            return resp.json()

        except requests.ConnectionError as err:
            return self.handle_api_error(err, "ConnectionError")

        except requests.exceptions.HTTPError as err:
            return self.handle_api_error(err, "HTTPError")

        except requests.Timeout as err:
            return self.handle_api_error(err, "Timeout")

        except json.decoder.JSONDecodeError as err:
            return self.handle_api_error(err, "JSONDecodeError")
