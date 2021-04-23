# Library Imports
from flask import Flask
from flask_restful import Resource, Api, reqparse

# Local Imports
import pricing.helpers
from pricing.pricer import Pricer
import utilities.utils as ut

# Constants
DEV = 'dev'
PROD = 'prod'
SYMB = 'ETH/BTC'

# Setup
app = Flask(__name__)
api = Api(app)
kip = Pricer(PROD)


@app.route('/price')
def get_price():
    # Parse request arguments
    parser = reqparse.RequestParser()
    parser.add_argument('pair', required=True)
    parser.add_argument('side', required=True)
    parser.add_argument('qty', required=True)
    args = parser.parse_args()
    pair = args['pair']
    side = args['side']
    qty = float(args['qty'])

    # Calculate price quote and create response data object
    orderbook = kip.get_orderbook(pair)
    precis = pricing.helpers.get_precision(pair)
    price = kip.calc_price(
        side=side,
        qty=qty,
        ob=orderbook,
        precision=precis
    )
    return {'price_quote':
                {'side': side,
                 'pair': pair,
                 'qty': qty,
                 'price': price}
            }, 200

# @app.route('/trade', methods=['POST'])
# def trade():
#     parser = reqparse.RequestParser()  # initialize
#     parser.add_argument('pair', required=True)  # add args
#     parser.add_argument('side', required=True)
#     parser.add_argument('qty', required=True)
#     args = parser.parse_args()  # parse arguments to dictionary
#     status = ''
#     return {'trade status': status}, 200


###########
# Test Area
###########
# ordbk = kip.get_orderbook(SYMB)
# print(ordbk['asks'])
# print(kip.calc_price('buy', 3, ordbk))


if __name__ == '__main__':
    app.run()  # run our Flask app
