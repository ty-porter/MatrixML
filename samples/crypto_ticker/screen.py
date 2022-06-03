from MatrixML.screen import MatrixScreen
import requests
import random


CRYPTO_TICKER_URL = "https://random-data-api.com/api/crypto_coin/random_crypto_coin"

class CryptoTickerScreen(MatrixScreen):

    def before_refresh(self):
        self.__fetch_data()

    def __fetch_data(self):
        response = requests.get(CRYPTO_TICKER_URL)

        self.data = response.json()

    def generate_price(self):
        return "${}".format(random.randrange(0, 9999) + round(random.random(), 2))
