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
    return tcs_sensor


'''
@requires Adafruit TCS34725 color sensor object
@modifies None
@returns None
main loop to read color sensor and detect occupancy
'''
def detect_occupancy(tcs_sensor):
        background = (0,0,0) # base value to compare new readings to
        threshold = 5 # threshold percent for occupancy

        while True:
                r, g, b = tcs_sensor.get_raw_data()
                current_color = (r, g, b)

                change = np.subtract(background, current_color)
                percent_change = abs(sum(change)/255*100)

                state = "Unoccupied"
                if (percent_change > threshold):
                    state = "Occupied"
                print("Percent Change: {:.2f}%    State: {}".format(percent_change, state))
                
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
