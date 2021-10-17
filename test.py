import requests
import json
import sys
import time

#   ---------- test of binance api ----------
# url = "https://api.binance.com"
# path = "/api/v3/avgPrice?symbol=BTCUSDT"
#
# response = requests.request("GET", url+path)
# market_price = json.loads(response.text)
#
# print(market_price["price"])

#   ---------- test of yahoo api ----------
# url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"
#
# querystring = {"symbols":"0P00017TVS.TO","region":"US"}
#
# headers = {
#     'x-rapidapi-key': "c0d5761ea1msh8478d73d97a2201p1a27d3jsn7111dd32cd34",
#     'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
#     }
#
# response = requests.request("GET", url, headers=headers, params=querystring)
# market_price = json.loads(response.text)
# print(response.text)
# print(market_price["quoteResponse"]["result"][0]["regularMarketPrice"])

#   ---------- test of progress bar ----------
# toolbar_width = 40
#
# sys.stdout.write("[%s]" % (" " * toolbar_width))
# sys.stdout.flush()
# sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
#
# for i in xrange(toolbar_width):
#     time.sleep(0.1) # do real work here
#     # update the bar
#     sys.stdout.write("-")
#     sys.stdout.flush()
#
# sys.stdout.write("]\n") # this ends the progress bar
#   ---------- test of currency converter api ----------
url = "https://currency-exchange.p.rapidapi.com/exchange"

querystring = {"to":"RMB","from":"CAD","q":"1.0"}

headers = {
    'x-rapidapi-key': "c0d5761ea1msh8478d73d97a2201p1a27d3jsn7111dd32cd34",
    'x-rapidapi-host': "currency-exchange.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)