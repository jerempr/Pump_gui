## Importations
import sys


from logger import *
from SysInfo import Get_clean_datetime

from asyncua import Node
from colorama import Fore

try:
        from PySide2.QtCore import *
except ImportError:
        from PyQt5.QtCore import *
if 'PyQt5' in sys.modules:
        from PyQt5.QtCore import pyqtSignal as Signal
        from PyQt5.QtCore import pyqtSlot as Slot
else:
        from PySide2.QtCore import Signal, Slot


def attribute_default_pump_datetime(bin,date):
        if bin and date=="":
                date = Get_clean_datetime()
        if not bin and not date=="":
                date = ""
        return date





class Opcuainfo(QThread):
        SystemSignal = Signal(str,str)
    
        def __init__(self):
                super().__init__()
                log.info("Initialisation classe OPCUAinfo")
                # self.first_call()
                
                # self.SystemSignal.emit("",False,"5.1","",True,False)

        
        def first_call(self):
                """à appeller pour avoir les valeurs au lancement de l'application (sans interrputions"""
                log.info("First call of OPCUAinfo!!")
                self.SystemSignal.emit("connected","True")
                # self.SystemSignal.emit("nan,"*120)
        
        def warn_closed_connexion(self):
                """ call if connexion close in the middle of the process"""
                log.info("Call Server connexion error")
                self.SystemSignal.emit("connected","False")
                
        
        def datachange_notification(self, node: Node, val, data):
                """Callback for asyncua Subscription"""
                # log.info(Fore.BLUE+f"Value for node {node.nodeid.Identifier} : {val} "+Fore.RED +f"data: {data.monitored_item.Value.SourceTimestamp}"+Fore.RESET)
                strid = str(node.nodeid.Identifier).replace("API_local:","")
                # check if we need to send a problem message:
                if "Defaut_Elec_Pompe" in strid:
                        val = "" + bool(val) * f"<i>{str(data.monitored_item.Value.SourceTimestamp)[:-6]}<\i><b>  - Défaut sur la pompe {strid[-1]} -  </b>"
                elif type(val) == float:
                        val = round(val,2)
                self.SystemSignal.emit(f"{strid}",f"{val}")

        @Slot(int,float)
        def Write_modbus_float(self,addr,obj):
                """this function allows to write a float to modbus tcp
                # Args:
                        - addr (int): address where you want to write
                        - obj (float): the float number you want to write
                """
                if float(obj) == float(obj) and obj != "" :
                        log.info(f"Variable de type float écrite à l'adresse {addr} par modbus: {obj}")
                        # TODO
                        
        @Slot(float,bool)
        def Write_modbus_boolean(self,addr, obj):
                """this function allows to write a boolean to modbus tcp
                # Args:
                        - addr (int): address where you want to write
                        - obj (bool): the bool value you want to write
                """
                log.info(f"Variable de type boolean écrite à l'adresse {addr} par modbus: {obj}")
                # TODO

