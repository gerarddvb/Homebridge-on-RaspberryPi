import RPi.GPIO as gpio
import time
#set up pin 3 as an output
gpio.setmode(gpio.BCM)
gpio.setup(3,gpio.OUT)
gpio.setup(2,gpio.OUT)
gpio.setup(4,gpio.OUT)
gpio.setup(17,gpio.OUT)
gpio.setup(7,gpio.OUT)
gpio.setup(8,gpio.OUT)
