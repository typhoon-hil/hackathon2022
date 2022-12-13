
import os,sys
#import tensorflow as tf
#import torch



sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from communication_manager import CommunicationManager
from plugin_manager import hookimpl

FEED_IN_PRICE_HIGH = 5
ELECTRICITY_PRICE_LOW = 2



print("starting hackathon solution plugin")


@hookimpl
def uegos_started_hook(arg1):
    print("inside solution plugin uegos_started_hook()")
    return {"processed": True, "id": "example_solution_uegos_123"}


@hookimpl
def uegos_send_data(system_data):

    print(system_data)
    response = {}

    #Set loads
    response["l1"] = system_data["expected_load1"]//(system_data["expected_load1"]-0.01)

    response["l2"] = system_data["expected_load2"]//(system_data["expected_load2"]-0.01)
    #check if blackout
    if (system_data["blackout"]):
        if (system_data["feed_in_price"] == FEED_IN_PRICE_HIGH):
            response["car_battery"] = "use"
            return response
       # if (system_data["car_battery_SOC"] >= 55):
       #     response["car_battery"] = "use"
       #     return response
       #So that the car has enough battery left if the owner goes to work
        if(system_data["car_battery_SOC"]>=52 and system_data["car_battery_SOC"]< 55):
            response["l1"] = 0
      
        response["car_battery"] = "use"
        return response
    #Charge car when the electricity_price is low
    if (system_data["electricity_price"] == ELECTRICITY_PRICE_LOW):
        if (system_data["car_battery_SOC"] >= 82):
            response["car_battery"] = "idle"
        else:
            response["car_battery"] = "charge"
        return response

    response["car_battery"] = "use"
    return response


@hookimpl
def uegos_end_data(summary_data):

    print("Car spent: " + str(summary_data["car_battery_power"]))
    print("Load1 spent: " + str(summary_data["load1_power"]))
    print("Load2 spent: " + str(summary_data["load2_power"]))
    print("Load1 penalty: " + str(summary_data["penalty_load1"]))
    print("Load2 penalty: " + str(summary_data["penalty_load2"]))
    print("Car penalty: " + str(summary_data["car_penalty"]))
    print("Feed In Discount: " + str(summary_data["feed_in_discount"]))
    print("Total spent: " + str(summary_data["total_cost"]))

   
 
    
    # returning True will keep the simulation running, use with care
    return {"keepRunning": False}
