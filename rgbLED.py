#!/usr/bin/env python3

import RPi.GPIO

class rgbLED:
    """ LED Object init: 3GPIO pins: red-pin , green-pin , blue-pin"""
   
 
    def __init__(self, redPin, greenPin, bluePin):
        self.greenPin = greenPin
        self.redPin = redPin
        self.bluePin = bluePin
        self.STARTED = False
    
    def start(self):
        """ Starts the LED """
        if self.STARTED == False:
            RPi.GPIO.setmode(RPi.GPIO.BCM)
            RPi.GPIO.setup(self.greenPin, RPi.GPIO.OUT)
            RPi.GPIO.setup(self.redPin, RPi.GPIO.OUT)
            RPi.GPIO.setup(self.bluePin, RPi.GPIO.OUT)
            self.green = RPi.GPIO.PWM(self.greenPin, 100)
            self.red = RPi.GPIO.PWM(self.redPin, 100)
            self.blue = RPi.GPIO.PWM(self.bluePin, 100)
            self.green.start(100)
            self.red.start(100)
            self.blue.start(100)
            self.rawColor="100,100,100"
            self.color="255,255,255"
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

    def stop(self):
        """ Stops the LED """
        if self.STARTED == True:
            self.green.stop()
            self.red.stop()
            self.blue.stop()
            RPi.GPIO.cleanup()
            self.STARTED = False
        else:
            print("LED is not running, start it first")

    def setRawColor(self, r,g,b):
        self.red.ChangeDutyCycle(r)
        self.green.ChangeDutyCycle(g)
        self.blue.ChangeDutyCycle(b)
        self.Rawcolor = str(r) + ',' + str(g) + ',' + str(b)

    def setColor(self, r,g,b):
        self.color = str(r) + ',' + str(g) + ',' + str(b)
        r=round(r*100/255 ,0)
        g=round(g*100/255 ,0)
        b=round(b*100/255 ,0)
        self.red.ChangeDutyCycle(r)
        self.green.ChangeDutyCycle(g)
        self.blue.ChangeDutyCycle(b)