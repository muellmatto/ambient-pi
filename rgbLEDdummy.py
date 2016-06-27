#!/usr/bin/env python3


class rgbLED:
    """ LED-DUMMY-Object init: 3GPIO pins: red-pin , green-pin , blue-pin
    it doesnt do anything :)"""
   
 
    def __init__(self, redPin, greenPin, bluePin):
        self.greenPin = greenPin
        self.redPin = redPin
        self.bluePin = bluePin
        self.STARTED = False
        self.color="128,128,128"
    
    def start(self):
        """ Starts the LED """
        if self.STARTED == False:
            self.STARTED = True
            print("LED started")
        else:
            print("LED already started, stop it first")

    def kill(self):
        """ stop ALL LEDs und Cleans GPIO """
        self.STARTED = False
        self.color="0,0,0"
        print("LED killed")

    def stop(self):
        """ Stops the LED """
        if self.STARTED == True:
            self.STARTED = False
            self.color="0,0,0"
            print("LED stopped")
        else:
            print("LED is not running, start it first")

    def setRawColor(self, r,g,b):
        if self.STARTED == True:
            self.color = str(int(r*2.55)) + ',' + str(int(g*2.55)) + ',' + str(int(b*2.55))
            print("LED color set to: " + self.color)
        else:
            print("Start LED first")

    def setColor(self, r,g,b):
        if self.STARTED == True:
            self.color = str(r) + ',' + str(g) + ',' + str(b)
            r=round(r*100/255 ,0)
            g=round(g*100/255 ,0)
            b=round(b*100/255 ,0)
            print("LED color set to: " + self.color)
        else:
            print("Start LED first")
