import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
gpio.setup(4,gpio.OUT)
gpio.setup(17,gpio.OUT)
