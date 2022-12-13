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

# load1 = l1; load2 = l2; car_battery;

PPprosliKrozJutro = False

@hookimpl
def uegos_send_data(system_data):
    #print(system_data)
    global PPprosliKrozJutro
    response = {}
    
    response["l1"] = 1
    response["l2"] = 1
    response["car_battery"] = "use"
    
    if system_data["expected_load2"] == 0:
        response["l2"] = 0
    if system_data["expected_load1"] == 0:
        response["l1"] = 0
        
    if system_data["electricity_price"] == 7 and system_data["car_plugged"] == 0:
        PPprosliKrozJutro = False
        
    if system_data["electricity_price"] == 2: #Noc
        PPprosliKrozJutro = False
        if system_data["expected_load2"] == 7: #workday
            PPprosliKrozJutro = True
            if system_data["car_battery_SOC"] <70: #Parametar za stelovanje
                response["car_battery"] = "charge"
            else:
                response["car_battery"] = "use"
                
        
        else: #I dalje noc ali moze nastati homeday ili workday period od 23 do 6 ili 7
            response["car_battery"] = "charge"
        
    if system_data["electricity_price"] == 7: #Dan
        if system_data["car_plugged"] == 1 and system_data["car_battery_SOC"] >= 80: #Pravametar za stelovanje - dnevna cena jutro
            response["car_battery"] = "use"
        elif system_data["car_plugged"] == 1 and system_data["car_battery_SOC"] <=50 and system_data["car_battery_SOC"] >=30 and PPprosliKrozJutro:
            response["car_battery"] = "charge"
        else:
            response["car_battery"] = "use"
            #PPprosliKrozJutro = False
           
    if system_data["car_plugged"] ==1 and system_data["car_battery_SOC"] <= 10 and system_data["expected_load2"] == 7 and system_data["expected_load1"] == 3 and system_data["blackout"] == 1:
        response["l1"] = 0
    elif system_data["expected_load2"] == 0 and system_data["expected_load1"] == 3 and system_data["car_battery_SOC"] >= 3:
        response["l1"] = 1
        response["car_battery"] = "use"
        
    #if response["car_battery"] == "charge" and system_data["car_battery_SOC"]>=85 and system_data["electricity_price"] == 2:
     #   response["car_battery"] = "idle"
        
            
            

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
