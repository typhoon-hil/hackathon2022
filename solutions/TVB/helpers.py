counter = 0
week_load1_penalty_sum = 0
week_load2_penalty_sum = 0
week_car_penalty_sum = 0
week_grid_intake_sum = 0  # price

recnik = {}


def load_recnik(system_data):
    global recnik, counter
    counter += 1
    recnik = system_data


def check_home_day():
    global counter, recnik
    day, hour = calc_day_hour(counter)

    if day % 7 == 6 or day % 7 == 0:
        return True

    if hour == 7 and recnik["expected_load2"] == 7:
        return False
    else:
        return True


def car_charging_time():
    """Should I charge it now"""
    global counter, recnik
    day, hour = calc_day_hour(counter)
    print(day)
    if hour == 22 and recnik["expected_load1"] == 3 and recnik["expected_load2"] == 0:
        return "use"
    if (hour == 23 or hour == 24 or hour < 7) and recnik["car_battery_SOC"] < 95:
        return "charge"
    elif hour < 7 and recnik["car_battery_SOC"] > 95:
        return "idle"
    if hour == 7 and (recnik["expected_load1"] > 0 or recnik["expected_load2"] > 0):
        return "use"
    elif hour == 7 and recnik["expected_load1"] == 0 and recnik["expected_load2"] == 0:
        return "idle"
    return "use"


def set_load_state():
    global recnik
    t1 = 1
    t2 = 1
    if recnik["expected_load1"] == 0:
        t1 = 0
    if recnik["expected_load2"] == 0:
        t2 = 0
    return t1, t2


def calc_day_hour(counter):
    day = int(counter / 24) + 1
    if counter % 24 == 0:
        day -= 1
    hour = counter - 24 * (day - 1)
    return day, hour


if __name__ == "__main__":
    load1_expected = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        3,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        3,
        3,
        3,
        3,
        3,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        3,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        3,
        3,
        3,
        3,
        3,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        0,
        0,
    ]
    for i in range(1, 24 * 7 + 1):
        day, hour = calc_day_hour(i)
        print("[day: " + str(day) + " hour: " + str(hour) + "] = " + str(load1_expected[i - 1]))

# 2022-12-03 18:08:56 {'car_plugged': 1, 'car_battery_SOC': 100.0, 'blackout': 0, 'expected_load1': 0,
#                       'expected_load2': 0, 'actual_load1': 0, 'actual_load2': 0, 'electricity_price': 2,
#                       'feed_in_price': 2, 'car_load': 0, 'grid_intake': 0.0, 'load1_penalty': 45,
#                       'load2_penalty': 105, 'car_penalty': 0, 'pv_power': 0.0}
