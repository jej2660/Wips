from operator import ne
import sys, os, signal
from multiprocessing import Process
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11ProbeResp,Dot11Elt
from scapy.all import *

def channel_hopper():
        while True:
            try:
                channel = random.randrange(1,14)
                exe = "iw dev %s set channel %d" % ("wlan0mon", channel)
                os.system(exe)
                print(exe)
                time.sleep(1)
            except KeyboardInterrupt:
                break


class Ap:
    def __init__ (self, ssid, bssid, channel, enc):
        self.ssid = ssid
        self.bssid = bssid
        self.channel = channel
        self.enc = enc
    def getApInfo(self):
        return {"ssid":self.ssid,"bssid":self.bssid,"channel":self.channel}

class Network:
    def __init__(self, interface):
        self.interface = interface
        self.aps = {}
        self.target = ""
        self.rssList = []
    def updateApList(self):
        self.hopStart()
        sniff(iface=self.interface, prn=self.sniffAP, timeout=20)
        self.hopStop()

    def getApList(self):
        ls = []
        for data in self.aps.keys():
            ls.append(self.aps[data].getApInfo())
        return ls

    def getPowerData(self, adr, channel):
        self.target = adr
        self.rssList = []
        self.setChannel(channel)
        sniff(iface=self.interface, prn=self.getRssi, count=100)
        return  sum(self.rssList) / len(self.rssList)

    def getRssi(self, pkt):
        if pkt.haslayer(Dot11):
            if pkt.type == 0 and pkt.subtype == 8 :
                if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
                    if pkt.addr3 == self.target:
                        try:
                            extra = pkt.notdecoded
                            rssi = -(256-ord(extra[-4:-3]))
                        except:
                            rssi = -100
                        print(rssi)
                        self.rssList.append(rssi)

    def setChannel(self, channel):
        exe = "iw dev %s set channel %d" % (self.interface, channel)
        os.system(exe)
    def hopStop(self):
        p.terminate()
        p.join()
    def hopStart(self):
        p.start()
    def sniffAP(self, pkt):
        if( (pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp)) and not pkt[Dot11].addr3 in self.aps.keys()):
            ssid       = pkt[Dot11Elt].info
            bssid      = pkt[Dot11].addr3    
            channel    = int( ord(pkt[Dot11Elt:3].info))
            capability = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                    {Dot11ProbeResp:%Dot11ProbeResp.cap%}")
            
            # Check for encrypted networks
            if re.search("privacy", capability): enc = 'Y'
            else: enc  = 'N'

            # Save discovered AP
            self.aps[pkt[Dot11].addr3] = Ap(ssid, bssid, channel, enc)

            # Display discovered AP    
            print ("%02d  %s  %s %s" % (int(channel), enc, bssid, ssid))
    def deAuth(stationAdr, apAdr):
        #write down u are code
        return ""

if __name__ == "__main__":


    # Start the channel hopper
    p = Process(target = channel_hopper)

    network = Network("wlan0mon")
    network.hopStart()
    #network.target = "90:9f:33:6f:52:86"
    network.getPowerData("fc:7f:f1:ae:80:e0")
    network.hopStop()
    print("set channel")
    network.setChannel(11)
    network.getPowerData("fc:7f:f1:ae:80:e0")
    network.hopStop()
    
    #network.updateApList()
    #print(network.getApList())
    #p2 = Process(target=network.getPowerData)
    #p2.start()
    # Start the sniffer

    #sniff(iface=network.interface, prn=network.sniffAP)