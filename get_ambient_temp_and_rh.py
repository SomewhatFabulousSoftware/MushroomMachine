import time
import busio
import board
import adafruit_shtc3
import mcp9600



i2c = busio.I2C(board.SCL, board.SDA)
sht = adafruit_shtc3.SHTC3(i2c)
dirt_temp_sensor = mcp9600.MCP9600(0x66)
temp_dirt = dirt_temp_sensor.get_hot_junction_temperature()


temp_ambient, relative_humidity = sht.measurements
with open("Measurements.txt", "w") as f:
    f.write("temp: " + str(temp_dirt) + "\nHumidity: " + str(relative_humidity))
#print("Temp: %0.1f C" % temperature)
#print("Humidity: %0.1f %%" % relative_humidity)
