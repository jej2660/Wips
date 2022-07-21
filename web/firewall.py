import sqlite3,time
from network import *


class dbDAO():
    def __init__(self):
        self.con = sqlite3.connect("list.db")
        self.cur = self.con.cursor()

    def createTable(self):
        self.cur.execute("CREATE TABLE BLOCK_LIST (SSID text, MAC_ADDR TEXT, channel INT, flag INT)")
        self.con.commit()
    def insert(self, ssid, mac, channel, flag):
        self.cur.execute("INSERT INTO BLOCK_LIST VALUES (?,?,?,?)", (ssid, mac, channel, flag))
        self.con.commit()
    def select(self):
        self.cur.execute("SELECT * FROM BLOCK_LIST")
        return self.cur.fetchall() 
    def getAllowTarget(self):
        self.cur.execute("SELECT MAC_ADDR FROM BLOCK_LIST WHERE flag=1")
        return self.cur.fetchall()
    def getDisallowTarget(self):
        self.cur.execute("SELECT MAC_ADDR FROM BLOCK_LIST WHERE flag=0")
        return self.cur.fetchall()
    def delete(self, mac):
        self.cur.execute("DELETE FROM BLOCK_LIST WHERE mac_addr=?", (mac,))
        self.con.commit()
    def update(self, mac, channel, flag):
        self.cur.execute("UPDATE BLOCK_LIST SET ssid=?, channel=?, flag=? WHERE mac_addr=?", (ssid, channel, flag, mac))
        self.con.commit()
    def close(self):
        self.con.close()
    def getList(self):
        return self.select()

class Blocker():
    def __init__(self, net):
        self.net = net
    def block(self):
        self.dbdao = dbDAO()
        while True:
            self.net.updateApList()
            whitelistAP = self.dbdao.getAllowTarget()
            white = set()
            for row in whitelistAP:
                white.add(row[0])
            print(white)
            for ap in self.net.getApList():
                if ap["bssid"] not in white:
                    print(f"Now Block {ap['ssid']} {ap['bssid']}")
                    self.net.deAuth(ap['bssid'], ap['channel'])
            
            time.sleep(5)




if __name__ == "__main__":
    dbdao = dbDAO()
    data = dbdao.select()
    print(data)
