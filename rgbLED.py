#!/usr/bin/env python3

import RPi.GPIO

class rgbLED:
    """ LED Object init: 3GPIO pins: red-pin , green-pin , blue-pin"""
   
 
    def __init__(self, redPin, greenPin, bluePin):
        self.greenPin = greenPin
        self.redPin = redPin
        self.bluePin = bluePin
        self.STARTED = False
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(self.greenPin, RPi.GPIO.OUT)
        RPi.GPIO.setup(self.redPin, RPi.GPIO.OUT)
        RPi.GPIO.setup(self.bluePin, RPi.GPIO.OUT)
        self.color="0,0,0"
    
    def start(self):
        """ Starts the LED """
        if self.STARTED == False:
            self.green = RPi.GPIO.PWM(self.greenPin, 100)
            self.red = RPi.GPIO.PWM(self.redPin, 100)
            self.blue = RPi.GPIO.PWM(self.bluePin, 100)
            self.green.start(50)
            self.red.start(50)
            self.blue.start(50)
            self.color="128,128,128"
            self.STARTED = True
        else:
            print("LED already started, stop it first")

    def kill(self):
        """ stop ALL LEDs und Cleans GPIO """
        self.green.stop()
        self.red.stop()
        self.blue.stop()
        RPi.GPIO.cleanup()
        self.STARTED = False
        self.color="0,0,0"

    def stop(self):
        """ Stops the LED """
        if self.STARTED == True:
            self.green.stop()
            self.red.stop()
            self.blue.stop()
            self.STARTED = False
            self.color="0,0,0"
        else:
            print("LED is not running, start it first")

    def setRawColor(self, r,g,b):
        if self.STARTED == True:
            self.red.ChangeDutyCycle(r)
            self.green.ChangeDutyCycle(g)
            self.blue.ChangeDutyCycle(b)
            self.color = str(int(r*2.55)) + ',' + str(int(g*2.55)) + ',' + str(int(b*2.55))
        else:
            print("Start LED first")

    def setColor(self, r,g,b):
        if self.STARTED == True:
            self.color = str(r) + ',' + str(g) + ',' + str(b)
            r=round(r*100/255 ,0)
            g=round(g*100/255 ,0)
            b=round(b*100/255 ,0)
            self.red.ChangeDutyCycle(r)
            self.green.ChangeDutyCycle(g)
            self.blue.ChangeDutyCycle(b)
        else:
            print("Start LED first")
