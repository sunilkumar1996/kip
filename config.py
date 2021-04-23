# Local Imports
import credentials as cred

# Paths
LOG_PATH = 'output/logs'

KUCOIN = {
    'key': {
        'dev': cred.KC_SANDBOX_API_KEY,
        'prod': cred.KC_API_KEY
    },
    'secret': {
        'dev': cred.KC_SANDBOX_API_SECRET,
        'prod': cred.KC_API_SECRET
    },
    'passphrase': {
        'dev': cred.KC_SANDBOX_API_PASSPHRASE,
        'prod': cred.KC_API_PASSPHRASE
    },
    'is_sandbox': {
        'dev': True,
        'prod': False
    }
}

PAIRS = {
    'ETH/BTC': {
        'precision': 8
    },
    'BAX/BTC':  {
        'precision': 10
    },
    'BAX/ETH':  {
        'precision': 10
    },
}