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


day = 1
hour = 0
home_day = None


@hookimpl
def uegos_send_data(system_data):

    # Developed by Fit Art IT Team

    # Track day, hour, and home day

    global day, hour, home_day

    hour += 1

    if hour > 24:
        hour = hour % 24
        day += 1
        home_day = None

    if day is 6 or day is 7:
        home_day = True

    elif hour is 9:
        home_day = system_data["car_plugged"] is 1

    print("day: " + str(day) + ", hour: " + str(hour) + ", home_day: " + str(home_day))
    print(system_data)

    response = {}

    # Handle load 1

    # if hour < 7 or hour >= 23:
    #     # turn off at night
    #     response["l1"] = 0
    # elif 7 <= hour < 9 or 17 <= hour < 23:
    #     # turn on before and after work
    #     response["l1"] = 1
    # else:
    #     # toggle depending on work day
    #     response["l1"] = 1 if home_day is True else 0

    response["l1"] = 0 if system_data["expected_load1"] is 0 else 1

    # Handle load 2

    # if hour < 6 or hour >= 23:
    #     # turn off at night
    #     response["l2"] = 0
    # elif home_day is True:
    #     # handle home day hours
    #     response["l2"] = 1 if 9 <= hour < 22 else 0
    # else:
    #     # handle work day hours
    #     response["l2"] = 1 if 6 <= hour < 9 or 19 <= hour < 23 else 0

    response["l2"] = 0 if system_data["expected_load2"] is 0 else 1

    # Handle car battery

    if system_data["car_plugged"] is 0:
        # idle if car not plugged
        response["car_battery"] = "idle"

    elif hour >= 22 and day == 7:
        # sell late Sunday evening (optimization)
        response["car_battery"] = "use"

    elif system_data["feed_in_price"] is 5:  # 13 <= hour < 15:
        # sell when price is high
        response["car_battery"] = "use"

    elif system_data["car_battery_SOC"] < 100 and \
            system_data["electricity_price"] is 2 and \
            system_data["blackout"] is 0:
        # charge when price is low if no blackout
        response["car_battery"] = "charge"

    elif system_data["blackout"] is 1 and \
            response["l1"] is 0 and response["l2"] is 0:
        # charge battery form panel
        # if no loads and blackout (optimization)
        response["car_battery"] = "charge"

    elif system_data["car_battery_SOC"] >= 10 and \
            (response["l1"] is 1 or response["l2"] is 1) and \
            (system_data["electricity_price"] is not 2 or
             system_data["blackout"] is 1):
        # use battery for loads if possible
        # (since it charged on cheap electricity)
        response["car_battery"] = "use"

    else:  # otherwise idle
        response["car_battery"] = "idle"

    print(response)

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
    print("Cost minimized by: Fit Art IT Team")

    # Reset globals
    global day, hour, home_day
    day = 1
    hour = 0
    home_day = None

    # tf.add(1, 2).numpy()
    # hello = tf.constant("Hello, TensorFlow!")
    # print(hello.numpy())

    # returning True will keep the simulation running, use with care
    return {"keepRunning": False}
