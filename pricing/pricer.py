# Library imports
import ccxt
from kucoin.client import User
import logging
from typing import List

# Local Imports
import config
import pricing.helpers as hp

# Module logging
logger = logging.getLogger(__name__)


class Pricer:
    ################
    # Init
    ################
    def __init__(self, env):
        """
        Establish two KuCoin API connections (1): ccxt, (2) kucoin_sdk(official)
        :param env: dev/prod environment
        """
        # (1)
        self.ccxt = ccxt.kucoin({
            'apiKey': config.KUCOIN['key'][env],
            'secret': config.KUCOIN['secret'][env],
            'password': config.KUCOIN['passphrase'][env]
        })
        self.ccxt.set_sandbox_mode(config.KUCOIN['is_sandbox'][env])
        self.ccxt.load_markets()
        # (2)
        self.kucoin = User(
            config.KUCOIN['key'][env],
            config.KUCOIN['secret'][env],
            config.KUCOIN['passphrase'][env],
            is_sandbox=config.KUCOIN['is_sandbox'][env]
        )

    def get_orderbook(self, symbol: str):
        """
        Fetch entire KuCoin orderbook for given market symbol.
        :param symbol:
        :return: orderbook dict or None if fails. Format: {"price":{"asks":[[0.035916,3.5199122],[...
        """
        try:
            result = self.ccxt.fetch_order_book(symbol)
        except Exception as e:
            logger.error(f'Fetch {symbol} orderbook FAILED - {e}')
        else:
            return result

    @staticmethod
    def calc_price(side: str, qty: float, ob: List, precision: int) -> float:
        """
        Calculate synthetic price from orderbook layers corresponding to quantity requested.
        :param precision: DPs to quote price to
        :param ob: orderbook (list) as returned by 'get_orderbook'
        :param side: 'buy' or 'sell'
        :param qty: size of the the proposed order
        :return: (float) The price to be served by the API and returned to the user
        Example: qty = 100.  ob = [[30, 1], [40, 2], [100, 3], ...],  components = [30, 1], [40, 2], [30, 3],...]
        """
        ob_side = hp.translate_side(side)
        prices = ob[ob_side]
        needed = qty
        price_components: List[List[float, float]] = []
        for price, volume in prices:
            if needed <= volume:
                price_components.append((price, needed))
                needed -= volume  # To
                break
            price_components.append((price, volume))
            needed -= volume

        # Calculate denominator, in case request size exceeds total orderbook volume,
        # in which case return price as though quoting for maximum available volume only. (Ignore the excess.)
        if needed <= 0:
            denominator = qty
        else:
            denominator = qty - needed

        avg_price = sum(price * (volume/denominator) for price, volume in price_components)
        return round(avg_price, precision)
