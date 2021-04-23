# # Library Imports
#
# # Local Imports
# from utilities import logs
# from pricing.pricer import Pricer
# import utilities.utils as ut
#
#
# # Constants
# DEV = 'dev'
# PROD = 'prod'
#
#
# def initialise(env: str):
#     logs.setup_logging(env)
#
#
# def get_price(env):
#     kip = Pricer(env)
#     ob = kip.get_orderbook('ETH/BTC')
#     return ob
#
#
# def run():
#     mode = DEV
#     initialise(mode)
#     print(mode)
#
