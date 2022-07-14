import random, json
from multiprocessing import Process
from flask import Flask, render_template, request, Response, jsonify
from network import *

app = Flask(__name__)

network = Network("wlan1")




@app.route("/")
def index():
    return render_template("index.html")
@app.route("/address")
def address():
    return render_template("address.html")
@app.route("/signal")
def signalpage():
    return render_template("signal.html")


#API CALL
@app.route("/v1/ap")
def requestAp():
    network.updateApList()
    ls = network.getApList()
    print(ls)
    return jsonify(ls)
@app.route("/v1/getap")
def getAp():
    ls = network.getApList()
    if len(ls) == 0:
        return requestAp()
    print(ls)
    return jsonify(ls)
@app.route("/v1/signal", methods=["GET"])
def getSignal():
    adr = request.args.get("mac")
    channel = int(request.args.get("channel"))
    value = network.getPowerData(adr,channel)
    return str(value)
@app.route("/v1/deauth", methods=["GET"])
def requestDeauth():
    mode = int(request.args.get("mode"))
    if mode == 1:
        apmac = request.args.get("apmac")
        channel = int(request.args.get("channel"))
        network.deAuth(apmac, channel)
    elif mode == 0:
        apmac = request.args.get("apmac")
        channel = int(request.args.get("channel"))
        network.attackAP.append(Ap("0", apmac, channel, "Y"))
        p = Process(target=network.autoDeAuth)
        p.start()
    elif mode == 3:
        network.deauthAll()
    return ""




if __name__ == "__main__":
    #p = Process(target=network.autoDeAuth)
    #p.start()
    app.run()
