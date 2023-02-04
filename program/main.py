from func_connections import connect_dydx
from constants import ABORT_ALL_POSITIONS
from func_private import abort_all_positions
from constants import FIND_COINTEGRATED 
from func_public import construct_market_prices

if __name__ == "__main__":
    print("Hello Bot")
    try:
        print("Connecting to client....")
        client = connect_dydx()
    except Exception as ex:
        print(ex)
        print("Error occured when trying to connect dydx")
        exit(1)
    
    # Abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all positions...")
            close_orders = abort_all_positions(client)
        except Exception as ex:
            print("Error closing all positions...", ex)
            exit(1)

    #Find Cointegrated Pairs
    if FIND_COINTEGRATED:

        #Construct Market Price
        try:
            print("Fetching market prices, please allow 3 mins....")
            df_market_prices = construct_market_prices(client)

        except Exception as ex:
            print("Error constructing market prices...", ex)
            exit(1)

