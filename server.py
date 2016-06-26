import flask
import signal
import sys
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



### Routes

@app.route("/")
def hello():
    return flask.render_template("ledSetter.html", led1Color="rgb(" + led1.color + ")", led2Color="rgb(" + led2.color + ")")

@app.route("/jscolor.js")
def jsshit():
    return flask.render_template("jscolor.js")

@app.route("/off")
def off():
    led1.stop()
    led2.stop()
    return flask.render_template("ledSetter.html", led1Color="rgb(0,0,0)", led2Color="rgb(0,0,0)")




@app.route("/<handleThis>")
def handler(handleThis):
    if led1.STARTED == False:
        led1.start()
    if led2.STARTED == False:
        led2.start()
    led1Color, led2Color = handleThis.split("&")
    r, g, b = led1Color.split(",")
    led1.setColor(int(r) , int(g) , int(b) )
    r, g, b = led2Color.split(",")
    led2.setColor(int(r) , int(g) , int(b) )
    return flask.render_template("ledSetter.html", led1Color="rgb("+led1Color+")", led2Color="rgb("+led2Color+")")




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
