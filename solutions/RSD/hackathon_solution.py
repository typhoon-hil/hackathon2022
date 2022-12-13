import os, sys
#import tensorflow as tf

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from plugin_manager import hookimpl
from communication_manager import CommunicationManager

print("starting hackathon solution plugin")


@hookimpl
def uegos_started_hook(arg1):
    print("inside solution plugin uegos_started_hook()")
    return {"processed": True, "id": "example_solution_uegos_123"}


@hookimpl
def uegos_send_data(system_data):
    print(system_data)

    response = {}
    response["l1"] = 0  # load1 - off(0) and on(1)
    response["l2"] = 0  # load2 - off(0) and on(1)
    response["car_battery"] = "idle"  # "use", "idle"

    # ako postoji trazena vrednost upali load
    if system_data['expected_load1'] == 3:
        response['l1'] = 1
    else:
        response['l1'] = 0
    if system_data['expected_load2'] == 7:
        response['l2'] = 1
    else:
        response['l2'] = 0

    # punjenje auta tokom noci
    if system_data['electricity_price'] == 2:
        if not system_data['car_battery_SOC'] == 100:
            response["car_battery"] = "charge"
        else: 
            response["car_battery"] = "idle"

    # praznjenje auta tokom dana 
    if system_data['grid_intake'] < 20 and system_data['electricity_price'] == 7 and system_data['car_battery_SOC'] >= 20:
        response["car_battery"] = "use"
    

    # 6 ujutru
    if system_data['actual_load2'] == 0 and system_data['expected_load2'] == 7: 
         if system_data['grid_intake'] < 20 and system_data['car_battery_SOC'] >= 57:
            response["car_battery"] = "use"

    # 7 ujutru
    if system_data['actual_load2'] == 7 and system_data['actual_load1'] == 0:
         if system_data['grid_intake'] < 20 and system_data['car_battery_SOC'] >= 60:
            response["car_battery"] = "use"

    # blackout tokom dana
    if system_data['blackout'] == 1:
        if system_data['grid_intake'] < 20 and system_data['electricity_price'] == 7 and system_data['car_battery_SOC'] != 0:
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

    #tf.add(1, 2).numpy()
    #hello = tf.constant('Hello, TensorFlow!')
    #print(hello.numpy())

    # returning True will keep the simulation running, use with care
    return {"keepRunning": False}
