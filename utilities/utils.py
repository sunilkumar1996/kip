import json
from pprint import PrettyPrinter


def json_pretty(my_json):
    parsed = json.loads(my_json)
    return json.dumps(parsed, indent=4, sort_keys=True)


def get_market_ids(markets_dict):
    full_list = []
    for mkt in markets_dict:
        full_list.append(mkt['id'])
    return full_list


def pp(d):
    pretty = PrettyPrinter(indent=4)
    pretty.pprint(d)



##############
# Dev Utils
##############
def get_market_ids(markets_dict):
    """Usage:
    m = kip.ccxt.fetch_markets()
    m = ut.get_market_ids(m)
    ut.pp(m)
    """
    full_list = []
    for mkt in markets_dict:
        full_list.append(mkt['id'])
    return full_list
