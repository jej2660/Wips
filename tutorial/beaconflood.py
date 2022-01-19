from scapy.all import Dot11, Dot11Beacon, Dot11Elt, RadioTap, sendp, hexdump
 
netSSID = 'Cbosun'
iface = 'en0'
 
dot11 = Dot11(type=0, subtype=8, addr1 = 'ff:ff:ff:ff:ff:ff', addr2 = '11:11:11:11:11:11', addr3 = '22:22:22:22:22:22')
beacon = Dot11Beacon(cap='ESS+privacy')
essid = Dot11Elt(ID='SSID', info=netSSID, len=len(netSSID))
 
rsn = Dot11Elt(ID='RSNinfo', info=(
'\x01\x00'
'\x00\x0f\xac\x02'
'\x02\x00'
'\x00\x0f\xac\x04'
'\x00\x0f\xac\x02'
'\x01\x00'
'\x00\x0f\xac\x02'
'\x00\x00'))
 
frame = RadioTap()/dot11/beacon/essid/rsn
 
sendp(frame, iface=iface, inter=0.100, loop=1)