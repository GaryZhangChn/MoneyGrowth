# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import config
import asset
import data
import abc
import time
import matplotlib.pyplot as plt
import numpy as np


class Singleton:    # read the config file
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.username = config.username
        self.url_binance = config.api_binance
        self.url_yahoo = config.api_yahoo
        self.key_yahoo = config.yahoo_key
        self.host_yahoo = config.yahoo_host

        # print("URLs initialized!")


class Invoker:  # invoker object to execute commands
    def __init__(self):
        self.__commands = []
    def store_command(self, command):
        self.__commands.append(command)
    def execute_commands(self):
        for command in self.__commands:
            command.execute()

class Command(metaclass=abc.ABCMeta):   # An abstract class that defines how commands are executed
    def __init__(self, receiver):
        self.receiver = receiver

    @abc.abstractmethod
    def execute(self):
        pass

class ConcreteCommand(Command): # Subtype of Command, represents a particular command
    def execute(self):
        self.receiver.action()

class Receiver1: # Perform the updating work
    def action(self):
        print("updating...")
        ctr = 0
        hi_profit_abs = 0   # used to find the asset with highest absolute profit margin
        hi_profit_rel = 0   # used to find the asset with highest relative profit margin
        for i in asset_list:
            time.sleep(0.1)   # my yahoo free account allows only 5 requests per second, 500 per month
            if (ctr+1)==len(asset_list):
                print("100%...Done!")
            elif (ctr+1) >= (len(asset_list)*3/4) :
                print("75%...")
            elif (ctr+1) >= (len(asset_list)/2) :
                print("50%...")
            elif (ctr+1) >= (len(asset_list)/4) :
                print("25%...")
            this_profit_abs = globals()[str(i)].get_profit_abs()
            this_profit_rel = (globals()[str(i)].get_value()-globals()[str(i)].get_cost())/total_profit
            if hi_profit_abs < this_profit_abs:     # compare the value
                hi_profit_abs = this_profit_abs     # store the highest value for next comparison
                hi_profit_abs_asset = globals()[str(i)]     # store the object
            if hi_profit_rel < this_profit_rel:     # compare the value
                hi_profit_rel = this_profit_rel     # store the highest value for next comparison
                hi_profit_rel_asset = globals()[str(i)]     # store the object
            globals()[str(i)].est_value()
            ctr += 1

class Receiver2: # Perform the display work
    def action(self):
        print("Your current asset values are shown below:"
              "\n{0:50s}{1:15s}{2:10s}{3:10s}{4:10s}{5:10s}{6:15s}{7:10s}{8:15s}{9:15s}{10:15s}".format
              ("Name", "Portfolio", "Price", "Unit", " Cost", "Currency", "Market_Value", "Currency",  "  Value_prop", "    Profit_abs", "    Profit_rel"))
        hi_profit_abs = 0
        hi_profit_rel = 0
        for i in asset_list:
            this_profit_abs = globals()[str(i)].get_profit_abs()
            this_profit_rel = (globals()[str(i)].get_value() - globals()[str(i)].get_cost()) / total_profit
            if hi_profit_abs < this_profit_abs:  # compare the value
                hi_profit_abs = this_profit_abs  # store the highest value for next comparison
                hi_profit_abs_asset = globals()[str(i)]  # store the object
            if hi_profit_rel < this_profit_rel:  # compare the value
                hi_profit_rel = this_profit_rel  # store the highest value for next comparison
                hi_profit_rel_asset = globals()[str(i)]  # store the object
            print("\n{0:50s}{1:15s}{2:10s}{3:10s}{4:8.2f}{5:10s}{6:13.2f}{7:10s}{8:13.2f}%{9:13.2f}%{10:13.2f}%"
                  .format(globals()[str(i)].get_name(), globals()[str(i)].get_portfolio(), globals()[str(i)].get_price(),
                          globals()[str(i)].get_unit(), globals()[str(i)].get_cost(), "    " + globals()[str(i)].original_currency(), globals()[str(i)].change_currency(),
                          "      " + globals()[str(i)].display_currency(), globals()[str(i)].get_value()/total_value*100, globals()[str(i)].get_profit_abs()*100,
                          (globals()[str(i)].get_value()-globals()[str(i)].get_cost())/total_profit*100)
                  )
        print("##############################"
              "\nYour total asset is: $%.2f " % total_value,
              "\nYour total cost is: $%.2f " % total_cost,
              "\nYour profit margin is: %.2f%% " % (total_profit_abs * 100),
              "\n############################## \n")
        if total_profit_abs > 0:
            print("Good job, your investment profit is %.2f%%" % (total_profit_abs * 100), "by far. Your %s" % hi_profit_abs_asset.get_name(),
                  "asset has the highest absolute profit margin but %s" % hi_profit_rel_asset.get_name(), "contributes the most to your total profit.")
        elif total_profit_abs < 0:
            print("Attention, your investment profit is %.2f%%" % (total_profit_abs * 100), "by far. Your are loosing money")
            print(hi_profit_rel)
            print(hi_profit_abs)




def menu():
    print("\n1) Update assets"
          "\n2) View charts"
          "\n3) Change assets"
          "\n4) Init assets")
def select(option):
    if option == "1":
        update_assets()
    elif option == '2':
        view_charts()
    elif option =='3':
        change_assets()
    elif option == '4':
        init_assets()
    else:
        raise Exception("invalid input")

def update_assets():
    selection1 = input("m: input manually"
                      "\na: update from internet"
                      "\nHow would you like to update your assets: ")
    while str(selection1) not in ["m", "a"]:
        selection1 = input("Input invalid, please select from one of the options above: ")
    if selection1 == 'm':
        selection4 = "y"
        while str(selection4) is "y":
            for i in asset_list:
                print(globals()[str(i)].get_name(), ": ", globals()[str(i)].get_code())
            selection2 = input("Choose the asset code you want to update: ")
            selection3 = float(input("Enter the latest market price for %s: " % globals()[str(selection2)].get_name()))
            globals()[str(selection2)].set_price(selection3)
            selection4 = input("Do you want to update another asset market price? (yes: y)")
        display = Receiver2()
        concrete_command = ConcreteCommand(display)
        invoker = Invoker()
        invoker.store_command(concrete_command)
        invoker.execute_commands()

    elif selection1 == 'a':
        update = Receiver1()
        display = Receiver2()
        concrete_command1 = ConcreteCommand(update)
        concrete_command2 = ConcreteCommand(display)
        invoker = Invoker()
        invoker.store_command(concrete_command1)
        invoker.store_command(concrete_command2)
        invoker.execute_commands()



def view_charts():
    char_list = []
    char_label = []
    for i in asset_list:
        char_list.append(globals()[str(i)].get_value()/total_value)
        char_label.append(globals()[str(i)].get_name())
    # print(char_list)
    value_prop = np.array(char_list)
    plt.pie(value_prop, labels= char_label)
    plt.show()

def change_assets():
    selection1 = input("e: edit asset"
                       "\na: add asset"
                       "\nWould you like to add or edit assets: ")
    while str(selection1) not in ["e", "a"]:
        selection1 = input("Input invalid, please select from one of the options above: ")
    if selection1 == 'e':
        selection5 = "y"
        while str(selection5) is "y":
            for i in asset_list:
                print(globals()[str(i)].get_code(), ": ", globals()[str(i)].get_unit())
            selection2 = input("Choose the asset code you want to update: ")
            original_cost = float(globals()[str(selection2)].get_cost())
            original_unit = float(globals()[str(selection2)].get_unit())
            selection3 = float(input("Enter the unit for %s: " % globals()[str(selection2)].get_name()))
            globals()[str(selection2)].set_unit(original_unit + selection3)
            selection4 = float(input("Enter the total cost of the %.2f units you bought/sold: " %float(globals()[str(selection2)].get_unit())))
            globals()[str(selection2)].set_cost(original_cost + selection4)
            print("Edit successful. Your asset %s has changed from %s to %s" %(globals()[str(selection2)].get_name(),original_unit , globals()[str(selection2)].get_unit()))
            selection5 = input("Do you want to update another asset market price? (yes: y)")
    elif selection1 =='a':
        selection3 = input("Enter the asset code (object name): ")
        selection7 = input("Enter the asset symbol (check with API): ")
        selection4 = input("Enter the asset name: ")
        selection2 = input("Choose the portfolio (stock, ETF, CryptoCurrency): ")
        selection5 = input("Enter the asset cost: ")
        selection6 = input("Enter the asset unit: ")
        if selection2 is 'stock':
            globals()[str(selection3)] = asset.Stock()

        elif selection2 is 'ETF':
            globals()[str(selection3)] = asset.ETF()

        elif selection2 is 'CryptoCurrency':
            globals()[str(selection3)] = asset.Coin()
        globals()[str(selection3)].set_type(str(selection3), str(selection7), str(selection4))
        globals()[str(selection3)].set_cost(selection5)
        globals()[str(selection3)].set_unit(selection6)
        globals()[str(selection3)].eta_value()
        # print(total_value)
        # print(total_cost)
        global total_value
        total_value = total_value + globals()[str(selection3)].get_value()
        global total_cost
        total_cost = total_cost + globals()[str(selection3)].get_cost()
        asset_list.append(globals()[str(selection3)].get_code())

    display = Receiver2()
    concrete_command = ConcreteCommand(display)
    invoker = Invoker()
    invoker.store_command(concrete_command)
    invoker.execute_commands()

def init_assets():
    for i in asset_list:
        del globals()[str(i)]
    asset_list.clear()

if __name__ == '__main__':
    print("Welcome to Money Growth V1.0 - Your personal Investment Manager \n")
    config = Singleton()
    # print(config.key_yahoo)
    # global total_value
    # global total_cost
    total_value = 0
    total_cost = 0
    asset_list = []
    for i in data.stock:    # instantiate stock assets
        # print(data["price"])
        symbol = i
        asset_list.append(symbol)
        data_read = getattr(data, i)
        globals()[str(symbol)] = asset.Stock()
        # asset_id = "stock_" + symbol
        # exec("%s = asset.Stock()" % symbol)
        # i = asset.Stock()
        # i.set_type(symbol, data_read["name"])
        globals()[str(symbol)].set_type(data_read["code"], data_read["symbol"], data_read["name"])
        globals()[str(symbol)].set_currency(data_read["display_currency"], data_read["original_currency"])  # only set the first option (displayed currency)
        globals()[str(symbol)].set_cost(data_read["cost"])
        globals()[str(symbol)].set_unit(data_read["unit"])
        globals()[str(symbol)].set_value(data_read["market_value"])
        total_value = total_value + data_read["market_value"]
        total_cost = total_cost + data_read["cost"]


    for i in data.ETF:      # instantiate ETF assets
        symbol = i
        asset_list.append(symbol)
        data_read = getattr(data, i)
        globals()[str(symbol)] = asset.ETF()
        globals()[str(symbol)].set_type(data_read["code"], data_read["symbol"], data_read["name"])
        globals()[str(symbol)].set_currency(data_read["display_currency"], data_read["original_currency"])
        globals()[str(symbol)].set_cost(data_read["cost"])
        globals()[str(symbol)].set_unit(data_read["unit"])
        globals()[str(symbol)].set_value(data_read["market_value"])
        total_value = total_value + data_read["market_value"]
        total_cost = total_cost + data_read["cost"]


    for i in data.coin:     # instantiate CryptoCoin assets
        symbol = i
        asset_list.append(symbol)
        data_read = getattr(data, i)
        globals()[str(symbol)] = asset.Coin()
        globals()[str(symbol)].set_type(data_read["code"], data_read["symbol"], data_read["name"])
        globals()[str(symbol)].set_currency(data_read["display_currency"], data_read["original_currency"])
        globals()[str(symbol)].set_cost(data_read["cost"])
        globals()[str(symbol)].set_unit(data_read["unit"])
        globals()[str(symbol)].set_value(data_read["market_value"])
        total_value = total_value + data_read["market_value"]
        total_cost = total_cost + data_read["cost"]
        # print(globals()[str(symbol)].est_value())
    total_profit = total_value - total_cost
    total_profit_abs = total_profit / total_cost
    print("##############################"
          "\nYour total asset is: $%.2f " % total_value,
          "\nLast updating time: %s" %data.date,
          "\n##############################")
    menu()
    selection = input("Please select from one of the options above: ")
    while int(selection) < 1 or int(selection) > 4:
        selection = input("Input invalid, please select from one of the options above: ")
    select(selection)
