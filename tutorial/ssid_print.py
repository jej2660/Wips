from scapy.all import *
from scapy.layers.dot11 import Dot11

ap = []

def findAP(pkt):
    if pkt.haslayer(Dot11):
        print(pkt)
        if pkt.type == 0 and pkt.subtype == 8:
            if pkt.addr2 not in ap:
                ap.append(pkt.addr2)
                print("AP MAC : %s with SSID : %s" % (pkt.addr2, pkt.info))





if __name__ == "__main__":
    sniff(iface="en0", prn=findAP, monitor=True)
