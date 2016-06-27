import flask
import signal
import sys
import time
import threading
# import rgbLEDdummy as rgbLED
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
    r1, g1, b1 = led1.color.split(",")
    r2, g2, b2 = led2.color.split(",")
    ledData = { 'led': [ {'color':{'r': r1, 'g': g1, 'b': b1 }} , {'color':{'r': r2, 'g': g2, 'b': b2 }} ] , 'snoozeTimer':str(snoozeTimer) }
    return flask.render_template("ledSetter.html", ledData=ledData)


@app.route("/off")
def off():
    global snoozeTimer
    snoozeTimer = 0
    led1.stop()
    led2.stop()
    r1, g1, b1 = "0,0,0".split(",")
    r2, g2, b2 = "0,0,0".split(",")
    ledData = { 'led': [ {'color':{'r': r1, 'g': g1, 'b': b1 }} , {'color':{'r': r2, 'g': g2, 'b': b2 }} ] , 'snoozeTimer':str(snoozeTimer) }
    return flask.render_template("ledSetter.html", ledData=ledData)




@app.route("/set/<handleThis>")
def handler(handleThis):
    global snoozeTimer
    snoozeTimer = 0
    if led1.STARTED == False:
        led1.start()
    if led2.STARTED == False:
        led2.start()
    led1Color, led2Color = handleThis.split("&")
    r1, g1, b1 = led1Color.split(",")
    led1.setColor(int(r1) , int(g1) , int(b1) )
    r2, g2, b2 = led2Color.split(",")
    led2.setColor(int(r2) , int(g2) , int(b2) )
    ledData = { 'led': [ {'color':{'r': r1, 'g': g1, 'b': b1 }} , {'color':{'r': r2, 'g': g2, 'b': b2 }} ] , 'snoozeTimer':str(snoozeTimer) }
    return flask.render_template("ledSetter.html", ledData=ledData)


@app.route("/timer/<int:snooze>")
def timer(snooze):
    a = threading.Thread(target=snoozing, args=[snooze])
    a.start()
    r1, g1, b1 = led1.color.split(",")
    r2, g2, b2 = led2.color.split(",")
    ledData = { 'led': [ {'color':{'r': r1, 'g': g1, 'b': b1 }} , {'color':{'r': r2, 'g': g2, 'b': b2 }} ] , 'snoozeTimer':str(snoozeTimer) }
    return flask.render_template("ledSetter.html", ledData=ledData)


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
    app.run(host="0.0.0.0", port=8000)
    # app.run(host="0.0.0.0", port=80)
