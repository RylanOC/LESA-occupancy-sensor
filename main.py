#!/usr/bin/python3

import map
import operator
import numpy as np

# libraries to read light sensor data
import smbus
import time
import Adafruit_TCS34725 as sensor


'''
@requires None
@modifies None
@returns Sensor object for Adafruit TCS34725 color sensor
'''
def setup_sensor():
    tcs_sensor = sensor.TCS34725()
    tcs_sensor.set_interrupt(False)
    tcs_sensor.set_integration_time(0xD5) # set integration time to 100ms
    return tcs_sensor

'''
@requires The new and old values being compared, and the maximum value allowed
@modifies None
@returns Percent change between the values
'''
def calc_percent_change(new_reading, old_reading, max):
    change = new_reading - old_reading
    percent_change = abs(change) / max * 100
    return percent_change

'''
@requires Adafruit TCS34725 color sensor object
@modifies None
@returns None
main loop to read color sensor and detect occupancy
'''
def detect_occupancy(tcs_sensor):
        b_r, b_g, b_b a_b= tcs_sensor.get_raw_data() # background color to compare readings to
        threshold = 5 # threshold percent for occupancy

        while True:
                r, g, b, a= tcs_sensor.get_raw_data()

                # get_raw_data() returns a tuple of unsigned, 16 bit values
                # 2^16 = 65536, so the maximum expected reading is 65536
                r_change = calc_percent_change(r, b_r, 65536)
                g_change = calc_percent_change(g, g_g, 65536)
                b_change = calc_percent_change(b, b_b, 65536)
                a_change = calc_percent_change(a, a_b, 65536)

                state = "Unoccupied"
                if (max(r_change, g_change, b_change, a_change) > threshold):
                    state = "Occupied"

                print("""Percent Change (r, g, b, a): ({:.2f}, {:.2f}, {:.2f}, {:.2f})%    
                    State: {}""".format(r_change, g_change, b_change, a_change, state))
                
'''
@requires Adafruit TCS34725 color sensor object
@modifies None
@returns None
frees sensor object
'''
def free(tcs_sensor):
        tcs_sensor.set_interrupt(True)
        tcs_sensor.disable()

if __name__ == '__main__':
        tcs_sensor = setup_sensor()
        detect_occupancy(tcs_sensor)
        free(tcs_sensor)
