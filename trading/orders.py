# Library Imports
import logging
import uuid

# Module logging
logger = logging.getLogger(__name__)

# Constants
ORDER_TYPES = ['market', 'limit']
SIDES = ['buy', 'sell']


class Order:
    """
    Base class for generic order objects. Exchange-agnostic.
    Validation performed in subclasses - base class not [currently] invoked directly.
    NO setter for '_uuid'. This is set at initialisation and must never be changed.
    """
    def __init__(self,
                 symbol: str,
                 side: str,
                 amount: float
                 ):
        # Initialisation
        self._symbol = symbol
        self._side = side
        self._amount = amount
        self._unfilled = amount
        self._uuid = uuid.uuid4()
        self._exchange_id = None

    @property
    def symbol(self):
        return self._symbol

    @property
    def side(self):
        return self._side

    @property
    def amount(self):
        return self._amount

    @property
    def unfilled(self):
        return self._unfilled

    @unfilled.setter
    def unfilled(self, value):
        self._unfilled = value

    @property  # Deliberately no setter!
    def uuid(self):
        return self._uuid

    @property
    def exchange_id(self):
        return self._exchange_id

    @exchange_id.setter
    def exchange_id(self, value):
        self._exchange_id = value

    def get_base_ccy(self):
        """
        Returns the currency code on the left hand side of the symbol,
        e.g. 'EUR/USD' => 'EUR'
        """
        ccy = self.symbol[:3]
        return ccy


class LimitOrder(Order):
    """
    Class for generic limit order objects, derived from 'Order' base class.
    Exchange-agnostic.
    """
    def __init__(self,
                 symbol: str,
                 side: str,
                 amount: float,
                 price: float
                 ):
        # Validation
        if side not in SIDES:
            msg = f'Order side "{side}" is invalid, must be one of {str(SIDES)}'
            logger.critical(msg, exc_info=True)
            raise ValueError(msg)
        if amount == 0:
            msg = 'Can not order zero quantity. Change the amount.'
            logger.error(msg, exc_info=True)
            raise ValueError(msg)
        # Super-class initialisation
        super().__init__(symbol, side, amount)
        # Initialisation
        self._order_type = 'limit'
        self._price = price
        # logger.info(f'Limit order created: {side} {amount} of {symbol} at {price}')

    @property
    def order_type(self):
        return self._order_type

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value
