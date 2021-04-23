import config


def translate_side(side: str) -> str:
    """
    Translate order 'side' into corresponding side of the orderbook. For 'buy' look at 'asks', for 'sell' look at 'bids'
    :param side: [str] 'buy' or 'sell'
    :return: [str] 'bids' or 'asks or None
    """
    if side == 'buy':
        return 'asks'
    elif side == 'sell':
        return 'bids'
    else:
        return None


def get_precision(pair: str) -> int:
    """
    Fetch precision for supplied pair from internal dictionary.
    (Check periodically against exchange in market metadata.)
    :param pair: [str] - format is: 'base_ccy/quote_ccy' eg BAX/BTC
    :return: [int] - Decimal precision to serve price data to.  Default is 10dp.
    """
    try:
        return config.PAIRS[pair]['precision']
    except KeyError:
        return 10
