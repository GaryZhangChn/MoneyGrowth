from abc import abstractmethod, ABCMeta
import config
import requests
import json


class Value(metaclass=ABCMeta):  # The interface of getting market price of asset value
    @abstractmethod
    def get_quote(self, symbol):
        pass


class StockValue(Value):
    def get_quote(self, symbol):
        quote = YahooQuote(symbol)
        return quote.response()


class YahooQuote():  # Yahoo Finance API, used for equities and funds
    def __init__(self, symbol):  # Ref: https://rapidapi.com/apidojo/api/yahoo-finance1
        self.__url = config.api_yahoo
        self.__headers = {'x-rapidapi-key': "c0d5761ea1msh8478d73d97a2201p1a27d3jsn7111dd32cd34",
                          'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"}
        self.__querystring = {"symbols": str(symbol), "region": "US"}

    def response(self):
        response = requests.request("GET", self.__url, headers=self.__headers, params=self.__querystring)
        # print(response.text)
        res_json = json.loads(response.text)
        regularMarketPrice = res_json["quoteResponse"]["result"][0]["regularMarketPrice"]
        return regularMarketPrice


class CoinValue(Value):
    def get_quote(self, symbol):
        quote = BinanceQuote(symbol)
        return quote.response()


class BinanceQuote():  # Binance exchange API, used for Crypto Currencies
    def __init__(self, symbol):  # Ref: https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md
        self.__url = config.api_binance
        self.__path = "/api/v3/avgPrice?symbol=" + symbol

    def response(self):
        response = requests.request("GET", self.__url + self.__path)
        res_json = json.loads(response.text)
        return res_json["price"]


class Currency():
    def __init__(self):  # Ref: https://rapidapi.com/fyhao/api/currency-exchange/
        self.__url = config.api_currency
        self.__headers = {'x-rapidapi-key': config.currency_key,
                          'x-rapidapi-host': config.currency_host}

    def response(self, currency1, currency2):  # displayed currency - original currency rate
        querystring = {"to": str(currency1), "from": str(currency2), "q": "1.0"}
        response = requests.request("GET", self.__url, headers=self.__headers, params=querystring)
        return float(response.text)


# --------- abstract factory ---------
class AssetFactory(metaclass=ABCMeta):  # interface used to create portfolios
    def __init__(self):
        self.__name = None  # optional
        self.__code = None  # object name
        self.__symbol = None  # used to request the market quote
        self.__price = None  # cost price
        self.__unit = None  # unit you have
        self.__cost = None  # total cost
        self.__cost_price = None  # cost of each unit
        self.__value = None
        self.__original_currency = None
        self.__display_currency = "USD"  # default currency is USD
        # self.__getRate = Currency()

    @abstractmethod
    def set_type(self, code, symbol, name=None):
        pass

    @abstractmethod
    def set_cost(self, price):
        pass

    @abstractmethod
    def set_unit(self, unit):
        pass

    @abstractmethod
    def set_price(self, enter_price):
        pass

    @abstractmethod
    def set_value(self, value):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_code(self):
        pass

    @abstractmethod
    def get_portfolio(self):
        pass

    @abstractmethod
    def get_price(self):
        pass

    @abstractmethod
    def get_unit(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def get_profit_abs(self):
        pass

    @abstractmethod
    def change_currency(self):
        pass


# --------- concrete factory ---------
class Stock(AssetFactory):  # factory used to create equities
    def __init__(self):
        super().__init__()

        self.__quote = StockValue()
        self.__portfolio = "stock"

    def set_type(self, code, symbol, name=None):  # Symbol is mandatory, name is optional
        self.__code = code
        self.__symbol = symbol
        if name is not None:
            self.__name = name

    def set_cost(self, cost):
        self.__cost = cost

    def set_unit(self, unit):
        self.__unit = unit

    def set_price(self, enter_price):
        self.__price = enter_price
        self.__value = enter_price * self.__unit

    def set_value(self, value):
        self.__value = value

    def set_currency(self, currency1="USD", currency2="USD"):  # displayed currency, original currency
        self.__original_currency = currency2
        self.__display_currency = currency1

    def display_currency(self):
        return self.__display_currency

    def original_currency(self):
        return self.__original_currency

    def calc_cost_price(self):
        self.__cost_price = self.__cost / self.__unit
        return self.__cost_price

    def est_value(self):
        marketprice = float(self.__quote.get_quote(self.__symbol))
        marketprice = float("{:.4f}".format(marketprice))
        self.__price = marketprice
        self.__value = self.__unit * marketprice
        return self.__value

    def get_name(self):
        return self.__name

    def get_code(self):
        return self.__code

    def get_portfolio(self):
        return self.__portfolio

    def get_price(self):
        return str(self.__price)

    def get_unit(self):
        return str(self.__unit)

    def get_cost(self):
        cost = float("{:.4f}".format(self.__cost))
        return cost

    def get_value(self):
        value = float("{:.4f}".format(self.__value))
        return value

    def get_profit_abs(self):
        profit_abs = (float(self.__value) - float(self.__cost)) / float(self.__cost)
        profit_abs = float("{:.4f}".format(profit_abs))
        return profit_abs

    def change_currency(self):  # new feature, if want to display in a different currency
        if self.__original_currency != self.__display_currency:
            get_rate = Currency()
            rate = get_rate.response(self.__display_currency, self.__original_currency)
        else:
            rate = 1
        display_value = self.__value * rate
        return display_value

    # def __del__(self):
    #     print("object deleted.")


class ETF(AssetFactory):
    def __init__(self):
        super().__init__()

        self.__quote = StockValue()
        self.__portfolio = "ETF"

    def set_type(self, code, symbol, name=None):  # Symbol is mandatory, name is optional
        self.__code = code
        self.__symbol = symbol
        if name is not None:
            self.__name = name

    def set_cost(self, cost):
        self.__cost = cost

    def set_unit(self, unit):
        self.__unit = unit

    def set_price(self, enter_price):
        self.__price = enter_price
        self.__value = enter_price * self.__unit

    def set_value(self, value):
        self.__value = value

    def set_currency(self, currency1="USD", currency2="USD"):  # displayed currency, original currency
        self.__original_currency = currency2
        self.__display_currency = currency1

    def display_currency(self):
        return self.__display_currency

    def original_currency(self):
        return self.__original_currency

    def calc_cost_price(self):
        self.__cost_price = self.__cost / self.__unit
        return self.__cost_price

    def est_value(self):
        marketprice = float(self.__quote.get_quote(self.__symbol))
        marketprice = float("{:.4f}".format(marketprice))
        self.__price = marketprice
        self.__value = self.__unit * marketprice
        return self.__value

    def get_name(self):
        return self.__name

    def get_code(self):
        return self.__code

    def get_portfolio(self):
        return self.__portfolio

    def get_price(self):
        return str(self.__price)

    def get_unit(self):
        return str(self.__unit)

    def get_cost(self):
        cost = float("{:.4f}".format(self.__cost))
        return cost

    def get_value(self):
        value = float("{:.4f}".format(self.__value))
        return value

    def get_profit_abs(self):
        profit_abs = (float(self.__value) - float(self.__cost)) / float(self.__cost)
        profit_abs = float("{:.4f}".format(profit_abs))
        return profit_abs

    def change_currency(self):
        if self.__original_currency != self.__display_currency:
            get_rate = Currency()
            rate = get_rate.response(self.__display_currency, self.__original_currency)
        else:
            rate = 1
        display_value = self.__value * rate
        return display_value

    # def __del__(self):
    #     print("object deleted.")


class Coin(AssetFactory):
    def __init__(self):
        super().__init__()

        self.__quote = CoinValue()
        self.__portfolio = "CryptoCurrency"

    def set_type(self, code, symbol, name=None):  # Symbol is mandatory, name is optional
        self.__code = code
        self.__symbol = symbol
        if name is not None:
            self.__name = name

    def set_cost(self, cost):
        self.__cost = cost

    def set_unit(self, unit):
        self.__unit = unit

    def set_price(self, enter_price):
        self.__price = enter_price
        self.__value = enter_price * self.__unit

    def set_value(self, value):
        self.__value = value

    def set_currency(self, currency1="USD", currency2="USD"):  # displayed currency, original currency
        self.__original_currency = currency2
        self.__display_currency = currency1

    def display_currency(self):
        return self.__display_currency

    def original_currency(self):
        return self.__original_currency

    def calc_cost_price(self):
        self.__cost_price = self.__cost / self.__unit
        return self.__cost_price

    def est_value(self):
        marketprice = float(self.__quote.get_quote(self.__symbol))
        marketprice = float("{:.4f}".format(marketprice))
        self.__price = marketprice
        self.__value = self.__unit * marketprice
        return self.__value

    def get_name(self):
        return self.__name

    def get_code(self):
        return self.__code

    def get_portfolio(self):
        return self.__portfolio

    def get_price(self):
        return str(self.__price)

    def get_unit(self):
        return str(self.__unit)

    def get_cost(self):
        cost = float("{:.4f}".format(self.__cost))
        return float(cost)

    def get_value(self):
        value = float("{:.4f}".format(self.__value))
        return value

    def get_profit_abs(self):
        profit_abs = (float(self.__value) - float(self.__cost)) / float(self.__cost)
        profit_abs = float("{:.4f}".format(profit_abs))
        return profit_abs

    def change_currency(self):
        if self.__original_currency != self.__display_currency:
            get_rate = Currency()
            rate = get_rate.response(self.__display_currency, self.__original_currency)
        else:
            rate = 1
        display_value = self.__value * rate
        return display_value

    # def __del__(self):
    #     print("object deleted.")
