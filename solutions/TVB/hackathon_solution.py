import os, sys
import helpers

# import tensorflow as tf

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
    print("---------------------------------------------")
    helpers.load_recnik(system_data)
    # print(helpers.recnik)
    # print("KRAJ")

    response = {"l1": (helpers.set_load_state())[0], "l2": (helpers.set_load_state())[1], "car_battery": helpers.car_charging_time()}

    if system_data["blackout"] == 1:
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

    # tf.add(1, 2).numpy()
    # hello = tf.constant('Hello, TensorFlow!')
    # print(hello.numpy())

    # returning True will keep the simulation running, use with care
    return {"keepRunning": False}
