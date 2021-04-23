# # Library Imports
# from pricing.pricer import Pricer
# import logging
#
# # Local Imports
# import utilities as ut
#
# # Module logging
# logger = logging.getLogger(__name__)
#
#
# class Trader(Pricer):
#     def __init__(self, env):
#         super().__init__(env)
#
#     def get_kucoin_account_balance(self, ccy, *args) -> float:
#         """
#         Gets AVAILABLE funds not tied up in orders. Available <= total balance.
#         :param ccy: Currency
#         :param args: Accounts to include, ('main', 'trade' etc)
#         :return: Available cleared balance in ccy in accounts
#         """
#         accounts = self.kucoin.get_account_list(ccy)
#         cumulative = 0
#         for account in accounts:
#             try:
#                 if account['currency'] == ccy and (account['type'] in args or len(args) == 0):
#                     cumulative += float(account['available'])
#             except TypeError:
#                 # No accounts returned for specified ccy, return zero balance
#                 msg = f'No {ccy} accounts found at KuCoin ({self.env}). Returning zero balance.'
#                 logger.warning(msg)
#                 ut.send_telegram(self.env, msg, 'dev')
#                 return 0
#         return cumulative
#
#     def move_kucoin_funds(self, ccy, quantity, source, destination) -> bool:
#         """
#         KuCoin internal wallet transfer.
#         :param ccy: currency code (e.g. 'ETH')
#         :param quantity: amount of ccy
#         :param source: The 'from' wallet
#         :param destination: The 'to' wallet
#         :return: True if full transfer succeeded, otherwise False
#         """
#         success = False
#         destination_balance = self.get_kucoin_account_balance(ccy, destination)
#         # Check whether the transfer is even needed - do we already have enough funds in 'destination' wallet?
#         if destination_balance >= quantity:
#             success = True
#         else:
#             internal_transfer = round(quantity - destination_balance, 8)
#             # Check 'source' wallet has enough balance to effect the transfer before attempting
#             source_balance = self.get_kucoin_account_balance(ccy, source)
#             if source_balance >= internal_transfer:
#                 try:
#                     result = self.kucoin.inner_transfer(currency=ccy,
#                                                         from_payer=source,
#                                                         to_payee=destination,
#                                                         amount=internal_transfer)
#                     if result['orderId']:
#                         success = True
#                 except Exception as e:
#                     # Exception: 200-{"code":"100000","msg":"Transfer amount precision: 0.00000001"}
#                     msg = f'Kucoin Inner Transfer (inter-wallet move) FAILED: {e}'
#                     logger.error(msg)
#                     ut.send_telegram(self.env, msg, 'dev')
#         return success
