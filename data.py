stock = {"Rendong", "Fuling", "Chimin"}
ETF = {"BMO0722", "BMO764"}
coin = {"BTC", "ETH", "DOGE"}

# Tesla = dict(
#     code="Tesla",   # code is the object name
#     name="Tesla",   # used to display
#     symbol="TSLA",  # used to retrieve data from API
#     portfolio="stock",
#     currency="USD",
#     price=657.62,
#     unit=100,
#     cost=50000,
#     market_value=65762,
#     value_prop=0.6838,
#     profit_abs=0.3154,
#     profit_rel=0.7464
# )

Rendong = dict(
    code="Rendong",
    name="Rendong Holding",
    symbol="002647.SZ",
    portfolio="stock",
    display_currency="CNY",
    original_currency="CNY",
    # price=43.19,
    unit=3300,
    cost=31376.4,
    market_value=27687,
    # value_prop=0.6838,
    # profit_abs=0.3154,
    # profit_rel=0.7464
)
Fuling = dict(
    code="Fuling",
    name="Fuling Zhacai",
    symbol="002507.SZ",
    portfolio="stock",
    display_currency="CNY",
    original_currency="CNY",
    # price=43.19,
    unit=600,
    cost=18820.2,
    market_value=17142,
    # value_prop=0.6838,
    # profit_abs=0.3154,
    # profit_rel=0.7464
)
Chimin = dict(
    code="Chimin",
    name="Chimin Health Management",
    symbol="603222.SS",
    portfolio="stock",
    display_currency="CNY",
    original_currency="CNY",
    unit=900,
    cost=13884.3,
    market_value=14058,
)
BMO0722 = dict(
    code="BMO0722",
    name="BMO U.S. Equity ETF Fund (S&P500)",
    symbol="0P000070RM.TO",
    portfolio="ETF",
    display_currency="CAD",
    original_currency="CAD",
    price=None,
    unit=122.8852,
    cost=3500,
    market_value=3827.76,
    value_prop=0.6838,
    profit_abs=0.3154,
    profit_rel=0.7464
)
BMO764 = dict(
    code="BMO764",
    name="BMO Sustainable Opportunities Global Equity Fund",
    symbol="0P00017TVS.TO",
    portfolio="ETF",
    display_currency="CAD",
    original_currency="CAD",
    price=None,
    unit=1841.003,
    cost=24100.28,
    market_value=35962.89,
    value_prop=0.6838,
    profit_abs=0.3154,
    profit_rel=0.7464
)
# for CryptoCurrency, convert to USD as original currency
BTC = dict(
    code="BTC",
    symbol="BTCUSDT",
    name="Bitcoin",
    portfolio="CryptoCurrency",
    display_currency="CAD",
    # original_currency="CAD",
    original_currency="USD",
    unit=0.10073003,
    # cost=7500,
    cost=5993.29,
    market_value=5877.86,
)
ETH = dict(
    code="ETH",
    symbol="ETHUSDT",
    name="Ethereum",
    portfolio="CryptoCurrency",
    display_currency="CAD",
    original_currency="USD",
    unit=0.9033,
    cost=0.1,
    # cost=4855.36,
    market_value=9340.49,
)
DOGE = dict(
    code="DOGE",
    symbol="DOGEUSDT",
    name="Doge Coin",
    portfolio="CryptoCurrency",
    display_currency="CNY",
    original_currency="USD",
    unit=7926,
    # cost=10115,
    cost=1561.73,
    market_value=9340.49,
)

date = "2021.7.26"