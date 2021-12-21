"""Remotely control your Binance account via their API : https://binance-docs.github.io/apidocs/spot/en"""
"""
Thanks to :
https://github.com/whittlem/pycryptobot/tree/main/models/exchange/coinbase_pro
"""

import requests
import json


class PublicAPI():

    def __init__(self) -> None:
        # options
        self.debug = False
        self.die_on_api_error = False
        self._api_url = "https://api.pro.coinbase.com/"

    def get_currencies(self):
        """Retrieves currencies"""
        resp = self.authAPI("GET", f"currencies")
        return resp

    def authAPI(self, method: str, uri: str, payload: str = "") -> dict:
        """Initiates a REST API call"""

        if not isinstance(method, str):
            raise TypeError("Method is not a string.")

        if not method in ["GET", "POST"]:
            raise TypeError("Method not GET or POST.")

        if not isinstance(uri, str):
            raise TypeError("URI is not a string.")

        try:
            if method == "GET":
                resp = requests.get(self._api_url + uri)
            elif method == "POST":
                resp = requests.post(self._api_url + uri, json=payload)

            if resp.status_code != 200:
                resp_message = resp.json()["message"]
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
