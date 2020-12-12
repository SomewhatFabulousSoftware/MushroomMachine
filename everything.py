#import all the modules we need
import time
import busio
import board
import adafruit_shtc3
import mcp9600
import display_module as dm
import qwiic_relay


# define the constants we are monitoring for
MAX_TEMP = 23
MAX_HUM = 80
MIN_TEMP = 18
MIN_HUM = 50
UPDATE_FREQ = 30 #time in seconds to re-run everything
WATER_FREQ = (3600 * 24) / UPDATE_FREQ # gives the number of intervals to wait before watering again (once per day)
HEAT_RELAY = 1
BUBBLER_RELAY = 2
WATER_RELAY = 3
WATERING_TIME = 15 # in seconds
MAX_WATER_ATTEMPT = 5
MEASUREMENT_OFFSET = 2 #time in seconds that it takes the rest of the program to run approx
NUM_RELAYS = 4

# define some variables we will use
interval_count = WATER_FREQ
measurements = []


#collect all the data from the sensors
i2c = busio.I2C(board.SCL, board.SDA)
sht = adafruit_shtc3.SHTC3(i2c)
lcd = dm.lcd()

dirt_temp_sensor = mcp9600.MCP9600(0x66)
myRelay = qwiic_relay.QwiicRelay(0x6D)
myRelay.begin()
heat = False
bubbler = False


if((UPDATE_FREQ - MEASUREMENT_OFFSET) - WATERING_TIME < 0):
    print("Cannot run - check configured times")
    exit(1)

#loop to run every 30 seconds
time.sleep(20) # sleep to let i2c init before running

#initialize relay
for i in range(1, NUM_RELAYS):
    try:
        myRelay.set_relay_off(i)
    except IOError:
        print("Failed to initialize relays, check connections and restart the Pi")
        exit(3)

print("Relay initialization complete")
while(True):
    try:
        #update temperatures
        temp_dirt = dirt_temp_sensor.get_hot_junction_temperature()
        temp_ambient, relative_humidity = sht.measurements

        #increment count for watering - run each time watering hits 0
        if(interval_count < WATER_FREQ):
            interval_count += 1
        else:
            #make sure the watering function works so we don't starve the mushrooms of water
            watering_success = False
            attempts = 0
            while(not watering_success):
                try:
                    interval_count = 0
                    myRelay.set_relay_on(WATER_RELAY)
                    lcd.lcd_display_string("Watering...",1)
                    lcd.lcd_display_string("", 2)
                    time.sleep(WATERING_TIME)
                    myRelay.set_relay_off(WATER_RELAY)
                    watering_success = True
                except IOError:
                    attempts += 1
                    if (attempts >= MAX_WATER_ATTEMPT):
                        print ("watering failed, please check connections")
                        lcd.lcd_display_string("Water Fail    ", 1)
                        lcd.lcd_display_string("Check Conn    ", 2)
                        # Disable all relays before shutting down the program
                        for i in range(1, NUM_RELAYS):
                            try:
                                myRelay.set_relay_off(i)
                            except IOError:
                                print("Failed to disable relays, check connections and restart the Pi")
                        exit(2)
                    else:
                        print("Watering function failed, retrying (probably)")
                        lcd.lcd_display_string("Watering         ", 1)
                        lcd.lcd_display_string("Attempt" + str(attempts) + "     ", 2)

        if (temp_dirt < MIN_TEMP):
            myRelay.set_relay_on(HEAT_RELAY)
            heat = True
        elif (temp_dirt > MAX_TEMP):
            myRelay.set_relay_off(HEAT_RELAY)
            heat = False

        if (relative_humidity < MIN_HUM):
            myRelay.set_relay_on(BUBBLER_RELAY)
            bubbler = True
        elif (relative_humidity > MAX_TEMP):
            myRelay.set_relay_off(BUBBLER_RELAY)
            bubbler = False




        # write to display
        if(heat):
            lcd.lcd_display_string("Temp:" + str(temp_dirt) + " C*    ", 1)
        else: 
            lcd.lcd_display_string("Temp:" + str(temp_dirt) + " C     ", 1)

        if(bubbler):
            lcd.lcd_display_string("Humidity:" + str(relative_humidity) + "%*    ", 2)
        else:
            lcd.lcd_display_string("Humidity:" + str(relative_humidity) + "%     ", 2)

        #wait for next run
        if(interval_count == 0): #if we watered this time, subtract that time from the time we are waiting
            time_to_run = (UPDATE_FREQ - MEASUREMENT_OFFSET) - WATERING_TIME
        else: 
            time_to_run = UPDATE_FREQ - MEASUREMENT_OFFSET
        print("running: " + str(interval_count))
        time.sleep(time_to_run)
    except IOError:
        print("something broke - (probably the display) - but we're gonna try again!!!")
