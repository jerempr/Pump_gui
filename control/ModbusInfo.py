## Importations
import sys
from ModBus_Communication import OperaMetrix_ModbusTCP_client
from time import sleep
from logger import *
from SysInfo import Get_clean_datetime

try:
        from PySide2.QtCore import *
except ImportError:
        from PyQt5.QtCore import *
if 'PyQt5' in sys.modules:
        from PyQt5.QtCore import pyqtSignal as Signal
        from PyQt5.QtCore import pyqtSlot as Slot
else:
        from PySide2.QtCore import Signal, Slot


### AVEC AUTOMATE:

# class Modbusinfo(QThread):
#     SystemSignal = Signal(str,float)
#     def __init__(self):
#         super().__init__()
#         self.Myclient = OperaMetrix_ModbusTCP_client()
#         self.Myclient.connect()
#         self.niveau_cuve = 50
#         self.IhmSeuilNTB = 0
#         sleep(1)

     
#     def run(self):
#         while(True):
#                 self.IhmSeuilNTB = self.Myclient.Read_addr(101)
#                 IhmSeuilNTB_var = str(round(self.IhmSeuilNTB,2))
#                 niveau_cuve = self.Myclient.Read_addr(87)
#                 self.sleep(1)
#                 # log.debug(f"Variable modbus envoyée : {IhmSeuilNTB_var}")
#                 self.SystemSignal.emit(IhmSeuilNTB_var,niveau_cuve)
#                 sleep(1)
        
#     @Slot(float,float)
#     def Write_modbus_float(self,addr,obj):
#         log.debug(f"Variable de type float écrite à l'adresse {addr} par modbus: {obj}")
#         self.Myclient.Write_addr(addr,float(obj),type)

#     @Slot(float,bool)
#     def Write_modbus_boolean(self,addr, obj):
#         log.debug(f"Variable de type boolean écrite à l'adresse {addr} par modbus: {obj}")
#         self.Myclient.Write_addr(addr,float(obj),type)

### SANS AUTOMATE:

class Modbusinfo(QThread):
    SystemSignal = Signal(str,float,str)
    def __init__(self):
        super().__init__()
        self.niveau_cuve = 50
        self.IhmSeuilNTB = 0
        self.IhmSeuilNTB = 2.5 
        self.pompe2default = False
        self.pompe1default = False
        self.defautelec_message = ""
        self.dateofdefault1 = ""
        self.dateofdefault2 = ""

     
    def run(self):
        # create artificial values as if we are connected to an automat
        monter = 0
        incr_bandeau = 0
        bandeau = ""
        max_bandeau = 80
        # messages à afficher en cas de défault électrique sur les pompes:
        message1 = ":<b>  - Défaut sur la pompe 1 -  </b>"
        message2 = ":<b>  - Défaut sur la pompe 2 -  </b>"

        # message1 = " - Défaut sur la pompe 1 - "
        # message2 = " - Défaut sur la pompe 2 - "
        
        while(True):
                ## Gestion arttificielle du niveau de la cuve:
                if self.niveau_cuve>300 and monter == 1:
                        monter = 0
                elif self.niveau_cuve<50 and monter == 0:
                        monter = 1
                elif monter == 1:
                        self.niveau_cuve += 5
                elif monter == 0:
                        self.niveau_cuve -= 5
                IhmSeuilNTB_var = str(round(self.IhmSeuilNTB,2))

                ## Gestion des messages contextuels dans le menu: 
                # if self.pompe1default and not message1 in self.defautelec_message:
                #         self.defautelec_message += self.dateofdefault1 + message1
                # if self.pompe2default and not message2 in self.defautelec_message:
                #         self.defautelec_message += self.dateofdefault2 + message2
                
                self.defautelec_message = (self.dateofdefault1 + message1)*self.pompe1default + (self.dateofdefault2 + message2)*self.pompe2default

                # ## Gestion du bandeau de texte:
                # if len(self.defautelec_message) > max_bandeau :
                #         if incr_bandeau == len(self.defautelec_message) : incr_bandeau = 0
                #         elif incr_bandeau < (len(self.defautelec_message)-max_bandeau) :
                #                 bandeau = self.defautelec_message[incr_bandeau:(incr_bandeau+max_bandeau)]
                #                 incr_bandeau += 1
                #         else:
                #                 bandeau = self.defautelec_message[(incr_bandeau+max_bandeau)%max_bandeau:incr_bandeau]
                #                 incr_bandeau += 1
                bandeau = self.defautelec_message

                self.SystemSignal.emit(IhmSeuilNTB_var,self.niveau_cuve,bandeau)
                sleep(1)
                
        
    @Slot(float,float)
    def Write_modbus_float(self,addr,obj):
        log.debug(f"Variable de type float écrite à l'adresse {addr} par modbus: {obj}")
        if addr == 101:
                self.IhmSeuilNTB = obj
                

    @Slot(float,bool)
    def Write_modbus_boolean(self,addr, obj):
        log.debug(f"Variable de type boolean écrite à l'adresse {addr} par modbus: {obj}")
        if addr == 54:
                self.pompe1default = obj
                if obj:
                        self.dateofdefault1 = Get_clean_datetime()
        if addr == 75:
                self.pompe2default = obj
                if obj:
                        self.dateofdefault2 = Get_clean_datetime()
