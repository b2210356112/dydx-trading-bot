from datetime import datetime, timedelta
import time
from pprint import pprint
from func_utils import format_number

#Place market order
def place_market_order(client, market, side, size, price, reduce_only):
    #Get PositionId
    account_response = client.private.get_account()
    position_id = account_response.data["account"]["positionId"]

    #Get Expiration Time
    server_time = client.public.get_time()
    expiration = datetime.fromisoformat(server_time.data["iso"].replace("Z", "")) + timedelta(seconds=2000)

    #Place an order
    placed_order = client.private.create_order(
        position_id=position_id,
        market=market,
        side=side,
        order_type="MARKET",
        post_only=False,
        size=size,
        price=price,
        limit_fee='0.015',
        expiration_epoch_seconds=time.time() + 65,
        time_in_force="FOK",
        reduce_only=reduce_only
)
    return placed_order.data

#Abort all open positions
def abort_all_positions(client):
    
    # Cancel all orders
    client.private.cancel_all_orders()

    #Protect API
    time.sleep(0.5)

    #Get market for reference of tick size
    markets = client.public.get_markets().data

    pprint(markets)

    #Protect API
    time.sleep(0.5)

    # Get all open positions 
    positions = client.private.get_positions(status ="OPEN")
    all_positions = positions.data["positions"]

    # Handle open positions
    close_orders = []
    if len(all_positions) > 0:

        #Loop through each positions
        for position in all_positions:

            # Determine Market
            market = position["market"]

            # Determine Side
            side="BUY"
            if position["side"] == "LONG":
                side = "SELL"
            
            # Get price
            price = float(position["entryPrice"]) 
            accept_price = price * 1.7 if side == "BUY" else price * 0.3
            tick_size = markets["markets"][market]["tickSize"]
            accept_price = format_number(accept_price, tick_size)

            # Place order to close
            order = place_market_order(
                client,
                market,
                side,
                position["sumOpen"],
                accept_price,
                True
            )

            # Append the results
            close_orders.append(order)
            time.sleep(0.2)
    
        # Return close_orders
        return close_orders