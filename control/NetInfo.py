import sys
import os

try:
        from PySide2.QtCore import *
except ImportError:
        from PyQt5.QtCore import *
if 'PyQt5' in sys.modules:
        from PyQt5.QtCore import pyqtSignal as Signal
else:
        from PySide2.QtCore import Signal, Slot


def Get_networksituation():
        eth = os.popen('ip addr show eth0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
        wifi = os.popen('ip addr show wlan0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()

        if wifi == '':
                wifi = 'Not WiFi connexion'

        if eth == '' or str(eth) == '192.168.0.200':
                eth = 'No Eth connexion'
        return str(eth),str(wifi)





class Netinfo(QThread):
    SystemSignal = Signal(str,str)
    def __init__(self):
        super().__init__()

     
    def run(self):
        Ethernet , Wifi = Get_networksituation()
        self.sleep(3)
        self.SystemSignal.emit(Ethernet,Wifi)
        while(1):
                Ethernet , Wifi = Get_networksituation()
                self.sleep(3)
                self.SystemSignal.emit(Ethernet,Wifi)
                self.sleep(5*60)