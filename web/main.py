import random
from flask import Flask, render_template, request
from network import *

app = Flask(__name__)

network = Network("wlan0mon")
p = Process(target = channel_hopper)


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/address")
def address():
    return render_template("address.html")
@app.route("/signal")
def signalpage():
    return render_template("signal.html")
@app.route("/v1/ap")
def requestAp():
    network.updateApList(p)
    ls = network.getApList()
    print(ls)
    return str(ls)
@app.route("/v1/signal", methods=["GET"])
def getSignal():
    adr = request.args.get("mac")
    channel = request.args.get("channel")
    return network.getPowerData(adr,channel)

#Front-End test Code
@app.route("/test/signal")
def testSignal():
    return str(random.randrange(0, 100))
@app.route("/test/ap")
def testRequestAp():
    dummy = """[{'ssid': b'\xec\x9b\x90\xec\x8a\xa4\xed\x86\xb1\xed\x95\x99\xec\x83\x9d\xec\x83\x81\xeb\x8b\xb4\xec\x84\xbc\xed\x84\xb0', 'bssid': '70:5d:cc:94:b5:04', 'channel': 3}, {'ssid': b'HLCERT', 'bssid': '90:9f:33:1b:13:aa', 'channel': 1}, {'ssid': b'T wifi zone', 'bssid': '00:16:1f:03:0e:da', 'channel': 13}, {'ssid': b'T Free WiFi Zone', 'bssid': '12:16:1f:03:0e:da', 'channel': 13}, {'ssid': b'T wifi zone_secure', 'bssid': '02:16:1f:03:0e:da', 'channel': 13}, {'ssid': b'T wifi zone', 'bssid': '00:16:1f:03:16:ea', 'channel': 13}, {'ssid': b'T wifi zone_secure', 'bssid': '02:16:1f:03:16:ea', 'channel': 13}, {'ssid': b'T Free WiFi Zone', 'bssid': '12:16:1f:03:16:ea', 'channel': 13}, {'ssid': b'T wifi zone_secure', 'bssid': '02:16:1f:03:16:3e', 'channel': 13}, {'ssid': b'T Free WiFi Zone', 'bssid': '12:16:1f:03:16:3e', 'channel': 13}, {'ssid': b'CHOSUN_Infra', 'bssid': 'fc:7f:f1:b0:40:a0', 'channel': 1}, {'ssid': b'CHOSUN_Free', 'bssid': 'fc:7f:f1:b0:40:a3', 'channel': 1}, {'ssid': b'', 'bssid': 'fc:7f:f1:b0:40:a4', 'channel': 1}, {'ssid': b'T Free WiFi Zone', 'bssid': '12:16:1f:03:1c:a2', 'channel': 1}, {'ssid': b'T wifi zone_secure', 'bssid': '02:16:1f:03:1c:a2', 'channel': 1}, {'ssid': b'eduroam', 'bssid': 'fc:7f:f1:b0:40:a1', 'channel': 1}, {'ssid': b'CHOSUN_WiFi', 'bssid': 'fc:7f:f1:b0:40:a2', 'channel': 1}, {'ssid': b'T wifi zone', 'bssid': '00:16:1f:03:1c:a2', 'channel': 1}, {'ssid': b'CHOSUN_Infra', 'bssid': 'fc:7f:f1:ae:80:e0', 'channel': 11}, {'ssid': b'eduroam', 'bssid': 'fc:7f:f1:ae:80:e1', 'channel': 11}, {'ssid': b'CHOSUN_WiFi', 'bssid': 'fc:7f:f1:ae:80:e2', 'channel': 11}, {'ssid': b'CHOSUN_Free', 'bssid': 'fc:7f:f1:ae:80:e3', 'channel': 11}, {'ssid': b'', 'bssid': 'fc:7f:f1:ae:80:e4', 'channel': 11}, {'ssid': b'DIRECT-C3-HP M479fdw Color LJ', 'bssid': '02:68:eb:52:16:c3', 'channel': 6}, {'ssid': b'DIRECT-17-HP OfficeJet Pro 8710', 'bssid': '00:04:ea:48:90:20', 'channel': 6}, {'ssid': b'CHOSUN_Infra', 'bssid': 'fc:7f:f1:b0:55:80', 'channel': 6}, {'ssid': b'eduroam', 'bssid': 'fc:7f:f1:b0:55:81', 'channel': 6}, {'ssid': b'CHOSUN_WiFi', 'bssid': 'fc:7f:f1:b0:55:82', 'channel': 6}, {'ssid': b'CHOSUN_Free', 'bssid': 'fc:7f:f1:b0:55:83', 'channel': 6}, {'ssid': b'', 'bssid': 'fc:7f:f1:b0:55:84', 'channel': 6}, {'ssid': b'pc clinic 2.4Ghz', 'bssid': '90:9f:33:6f:90:b6', 'channel': 7}, {'ssid': b'Galaxy Jump8229', 'bssid': '26:95:dc:d3:f5:15', 'channel': 6}]"""
    return dummy


if __name__ == "__main__":
    app.run()