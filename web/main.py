from calendar import c
from flask import Flask, render_template
from network import *

app = Flask(__name__)

network = Network("wlan0mon")
p = Process(target = channel_hopper)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ap")
def getAp():
    return "getAP"

if __name__ == "__main__":
    app.run()