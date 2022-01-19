import sys, os, signal
from multiprocessing import Process
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11ProbeResp,Dot11Elt
from scapy.all import *

def channel_hopper():
        while True:
            try:
                channel = random.randrange(1,14)
                exe = "iw dev %s set channel %d" % ("wlan0mon", channel)
                #print(exe)
                os.system(exe)
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
        return [self.ssid, self.bssid, self.channel]

class Network:
    def __init__(self, interface):
        self.interface = interface
        self.aps = {}
        self.target = ""
        self.rssList = []
    def updateApList(self):
        sniff(iface=self.interface, prn=self.sniffAP, timeout=10)

    def getApList(self):
        return self.aps

    def getPowerData(self, adr):
        self.target = adr
        self.rssList = []
        sniff(iface=self.interface, prn=self.getRssi, count=100)

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
    p.start()

    network = Network("wlan0mon")
    #network.target = "90:9f:33:6f:52:86"
    print(network.getPowerData("90:9f:33:6f:52:86"))
    p.terminate()
    p.join()
    #p2 = Process(target=network.getPowerData)
    #p2.start()
    # Start the sniffer
    #sniff(iface=network.interface, prn=network.sniffAP)