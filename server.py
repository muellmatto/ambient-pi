import flask
import signal
import sys
import time
import threading
import rgbLED


## Sigterm abfangen und LEDs wieder aus machen!!
def signal_term_handler(signal, frame):
    led1.kill() 
    led2.kill()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)


## Main App

app = flask.Flask(__name__)

## Create RGB-LEDS
led1 = rgbLED.rgbLED(27,17,22)
led2 = rgbLED.rgbLED(19,13,26)

## Timerkram
snoozeTimer = 0

### Routes

@app.route("/")
def hello():
    return flask.render_template("ledSetter.html", led1Color="rgb(" + led1.color + ")", led2Color="rgb(" + led2.color + ")" , snoozeTimer=str(snoozeTimer))


@app.route("/off")
def off():
    global snoozeTimer
    snoozeTimer = 0
    led1.stop()
    led2.stop()
    return flask.render_template("ledSetter.html", led1Color="rgb(0,0,0)", led2Color="rgb(0,0,0)", snoozeTimer=str(snoozeTimer))




@app.route("/set/<handleThis>")
def handler(handleThis):
    global snoozeTimer
    snoozeTimer = 0
    if led1.STARTED == False:
        led1.start()
    if led2.STARTED == False:
        led2.start()
    led1Color, led2Color = handleThis.split("&")
    r, g, b = led1Color.split(",")
    led1.setColor(int(r) , int(g) , int(b) )
    r, g, b = led2Color.split(",")
    led2.setColor(int(r) , int(g) , int(b) )
    return flask.render_template("ledSetter.html", led1Color="rgb("+led1.color+")", led2Color="rgb("+led2.color+")" , snoozeTimer=str(snoozeTimer))


@app.route("/timer/<int:snooze>")
def timer(snooze):
    a = threading.Thread(target=snoozing, args=[snooze])
    a.start()
    return flask.render_template("ledSetter.html", led1Color="rgb("+led1.color+")", led2Color="rgb("+led2.color+")" , snoozeTimer=str(snoozeTimer))


def snoozing(snooze):
    global snoozeTimer
    snoozeTimer = snooze
    r1,g1,b1 = led1.color.split(',')
    r2,g2,b2 = led2.color.split(',')
    while snoozeTimer > 0:
        time.sleep(1)
        q = snoozeTimer/snooze
        led1.setColor(round(int(r1)*q) ,round(int(g1)*q) , round(int(b1)*q)  )
        led2.setColor(round(int(r2)*q) ,round(int(g2)*q) , round(int(b2)*q)  )
        snoozeTimer -= 1
    led1.stop()
    led2.stop()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
