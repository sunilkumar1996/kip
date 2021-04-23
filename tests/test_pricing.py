# Library imports
import unittest

# Local imports
from pricing.pricer import Pricer

ENV = 'dev'
SYMB = 'ETH/BTC'


class TestCalcPrice(unittest.TestCase):
    def setUp(self):
        self.kip = Pricer(ENV)
        self.obook = {
            'asks': [[0.8, 51], [0.85, 63], [0.9, 75], [1, 80], [1.15, 95], [1.3, 103], [1.5, 121], [1.65, 139]],
            'bids': [[101, 10], [99, 100], [95, 1000], [90, 10000], [80, 100000], [65, 1000000],
                     [50, 10000000], [30, 100000000]]
            }

    def test_calc_price_simple_buy(self):
        self.obook = {
            'asks': [[1, 10], [2, 20]],
            'bids': [[101, 10]]
        }
        self.assertEqual(
            1.50,
            self.kip.calc_price('buy', 20, self.obook, 10)
            )

    def test_calc_price_simple_sell(self):
        self.obook = {
            'asks': [[1, 10]],
            'bids': [[5, 100], [4, 200]]
        }
        self.assertEqual(
            4.50,
            self.kip.calc_price('sell', 200, self.obook, 10)
            )

    def test_calc_price_buy_1_layer(self):
        self.assertEqual(
            0.80,
            self.kip.calc_price('buy', 45, self.obook, 10)
            )

    def test_calc_price_buy_3_layers(self):
        self.assertEqual(
            0.84500,
            self.kip.calc_price('buy', 150, self.obook, 10)
            )

    def test_calc_price_buy_5_layers(self):
        self.assertEqual(
            0.91724137930,
            self.kip.calc_price('buy', 290, self.obook, 10)
            )

    def test_calc_price_buy_more_layers_than_are_in_ob(self):
        self.assertEqual(
            1.23225584590,
            self.kip.calc_price('buy', 8727, self.obook, 10)
        )
        self.assertEqual(
            1.23225584590,
            self.kip.calc_price('buy', 7124, self.obook, 10)
        )

    def test_calc_price_buy_just_below_total_orderbook(self):
        self.assertEqual(
            1.23168044080,
            self.kip.calc_price('buy', 726, self.obook, 10)
        )

    def test_calc_price_sell_1_layer(self):
        self.assertEqual(
            101,
            self.kip.calc_price('sell', 9, self.obook, 10)
            )

    def test_calc_price_sell_3_layers(self):
        self.assertEqual(
            96.58620689660,
            self.kip.calc_price('sell', 290, self.obook, 10)
            )

    def test_calc_price_sell_5_layers(self):
        self.assertEqual(
            87.31937500000,
            self.kip.calc_price('sell', 16000, self.obook, 10)
            )
