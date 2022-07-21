import random, json
from multiprocessing import Process
from flask import Flask, render_template, request, Response, jsonify
from network import *
from firewall import *

app = Flask(__name__, template_folder="templates", static_folder="static")

network = Network("wlan1")
dbdao = dbDAO()
block = Blocker(network)
block_thread = Process(target=block.block)
block_status = False



@app.route("/")
def index():
    print(block_status)
    return render_template("index.html", blcok_status=block_status)
@app.route("/address")
def address():
    return render_template("address.html")
@app.route("/signal")
def signalpage():
    return render_template("signal.html")
@app.route("/block")
def blcokpage():
    return render_template("block.html")
@app.route("/switch")
def switch():
    return render_template("switch.html", test="test")


#API CALL


@app.route("/v1/FirewallOff")
def FirewallOff():
    global block_status
    block_status = False
    block_thread.terminate()
    return "Firewall Off"
@app.route("/v1/FirewallOn")
def FirewallOn():
    global block_status, block_thread
    block_status = True
    block_thread = Process(target=block.block)
    block_thread.start()
    return "Firewall On"
@app.route("/v1/BlockList")
def getBlockList():
    dbdao = dbDAO()
    rows = dbdao.select()
    ls = []
    for row in rows:
        tmp = {"ssid": row[0], "mac": row[1], "channel": row[2]}
        ls.append(tmp)
    return jsonify(ls)
@app.route("/v1/updateBlockList", methods= ["POST"])
def updateBlockList():
    data = request.get_json()
    dbdao = dbDAO()
    for row in data:
        dbdao.insert(row['ssid'], row['mac'], row['channel'], 1)
    return "True"


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
    app.run(host="0.0.0.0", port=8080, debug=True)
