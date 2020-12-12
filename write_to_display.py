import sys, getopt
import display_module as dm


mylcd = dm.lcd()
mylcd.lcd_display_string("Hello World!", 1)
mylcd.lcd_display_string("Hola Mundo!", 2)
mylcd.backlight(1)

 # python write_to_display.py "Temp: 70C" "Hum: 65%" true
