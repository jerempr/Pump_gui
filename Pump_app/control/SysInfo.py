import sys
import datetime

try:
        from PySide2.QtCore import *
except ImportError:
        from PyQt5.QtCore import *
if 'PyQt5' in sys.modules:
        from PyQt5.QtCore import pyqtSignal as Signal
else:
        from PySide2.QtCore import Signal, Slot




def Get_clean_datetime():
    date = datetime.datetime.now()
    D1 = [date.day,date.month,date.hour,date.minute,date.second]
    D2 = ["","","","",""]
    for k in range (len(D1)):
        if D1[k]<10:
            D2[k] = f"0{D1[k]}"
        else :
            D2[k] = str(D1[k])
    return f"<u>{D2[0]}/{D2[1]}/{date.year}</u>   {D2[2]}:{D2[3]}:{D2[4]}"


class Sysinfo(QThread):
    SystemSignal = Signal(str)
    def __init__(self):
        super().__init__()

     
    def run(self):
        while(1):
                Date = Get_clean_datetime()
                # self.sleep()
                self.SystemSignal.emit(Date)
                self.sleep(1)