from calendar import c
from flask import Flask
from network import *

app = Flask(__name__)

network = Network("wlan0mon")
p = Process(target = channel_hopper)
p.start()

@app.route("/")
def index():
    return "Hello World!"

@app.route("/ap", method="GET")
def getAp():
    return "getAP"

if __name__ == "__main__":
    app.run()