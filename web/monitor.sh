$adap = "wlan1"
ifconfig $adap down
iwconfig $adap mode monitor
ifconfig $adap up
