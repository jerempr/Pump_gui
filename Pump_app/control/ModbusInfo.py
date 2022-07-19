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


def attribute_default_pump_datetime(bin,date):
        if bin and date=="":
                date = Get_clean_datetime()
        if not bin and not date=="":
                date = ""
        return date



### AVEC AUTOMATE:


class Modbusinfo(QThread):
    SystemSignal = Signal(str,bool,float,str,bool,bool)
    def __init__(self):
        super().__init__()
        self.Myclient = OperaMetrix_ModbusTCP_client()
        self.Myclient.connect()
        self.niveau_cuve = 50
        self.pompe2default = False
        self.pompe1default = False
        self.defautelec_message = ""
        self.dateofdefault1 = ""
        self.dateofdefault2 = ""
        self.marchep1_54 = False
        self.marchep2_75 = False
        self.Table = []
        
        self.MUTEX = False

     
    def run(self):
        message1 = ":<b>  - Défaut sur la pompe 1 -  </b>"
        message2 = ":<b>  - Défaut sur la pompe 2 -  </b>"
        while(True):
                #Récupération des valeurs en modbus sur l'automate:
                # self.Table = self.Myclient.Read_all_addr
                self.Wait_for_mutex()

                self.MUTEX = True
                
                self.niveau_cuve = self.Myclient.Read_addr(87)
        
                Ihm_parameters = self.Myclient.Get_Ihm_parameters()
                GraisseOn = self.Myclient.Read_addr(113,'bool')
                
                
                self.marchep1_54 = self.Myclient.Read_addr(54,"bool")
                self.marchep2_75 = self.Myclient.Read_addr(75,"bool")
                self.pompe2default = self.Myclient.Read_addr(75.05,"bool")
                self.pompe1default = self.Myclient.Read_addr(54.05,"bool")
                
                self.MUTEX = False
                #traitement de ces valeurs afin de les envoyer à l'Ihm:
                
                # get the date of defaults if there is some
                self.dateofdefault1 = attribute_default_pump_datetime(self.pompe1default,self.dateofdefault1)
                self.dateofdefault2 = attribute_default_pump_datetime(self.pompe2default,self.dateofdefault2)
                
                self.defautelec_message = (self.dateofdefault1 + message1)*self.pompe1default + (self.dateofdefault2 + message2)*self.pompe2default
                self.sleep(1)
                # Envoi de ces valeurs à l'Ihm:
                self.SystemSignal.emit(Ihm_parameters,GraisseOn,self.niveau_cuve,self.defautelec_message,self.marchep1_54,self.marchep2_75)
                sleep(1)
        
        
    def Wait_for_mutex(self):
        if self.MUTEX:
                sleep(1)
                return self.Wait_for_mutex
        else:
                self.MUTEX = True
                exit
            

    @Slot(int,float)
    def Write_modbus_float(self,addr,obj):
        self.Wait_for_mutex()
        log.info(f"Variable de type float écrite à l'adresse {addr} par modbus: {obj}")
        self.Myclient.Write_addr(addr,float(obj))
        self.MUTEX = False
        

    @Slot(float,bool)
    def Write_modbus_boolean(self,addr, obj):
        self.Wait_for_mutex()
        log.info(f"Variable de type boolean écrite à l'adresse {addr} par modbus: {obj}")
        self.Myclient.Write_addr(addr,float(obj),"bool")
        self.MUTEX = False
        if addr == 54:
                self.pompe1default = obj
                if obj:
                        self.dateofdefault1 = Get_clean_datetime()
        if addr == 75:
                self.pompe2default = obj
                if obj:
                        self.dateofdefault2 = Get_clean_datetime()

### SANS AUTOMATE:

# class Modbusinfo(QThread):
#     SystemSignal = Signal(str,float,str)
#     def __init__(self):
#         super().__init__()
#         self.niveau_cuve = 50
#         self.IhmSeuilNTB = 0
#         self.IhmSeuilNTB = 2.5 
#         self.pompe2default = False
#         self.pompe1default = False
#         self.defautelec_message = ""
#         self.dateofdefault1 = ""
#         self.dateofdefault2 = ""

     
#     def run(self):
#         # create artificial values as if we are connected to an automat
#         monter = 0
#         incr_bandeau = 0
#         bandeau = ""
#         max_bandeau = 80
#         # messages à afficher en cas de défault électrique sur les pompes:
#         message1 = ":<b>  - Défaut sur la pompe 1 -  </b>"
#         message2 = ":<b>  - Défaut sur la pompe 2 -  </b>"

#         # message1 = " - Défaut sur la pompe 1 - "
#         # message2 = " - Défaut sur la pompe 2 - "
        
#         while(True):
#                 ## Gestion arttificielle du niveau de la cuve:
#                 if self.niveau_cuve>300 and monter == 1:
#                         monter = 0
#                 elif self.niveau_cuve<50 and monter == 0:
#                         monter = 1
#                 elif monter == 1:
#                         self.niveau_cuve += 5
#                 elif monter == 0:
#                         self.niveau_cuve -= 5
#                 IhmSeuilNTB_var = str(round(self.IhmSeuilNTB,2))

#                 ## Gestion des messages contextuels dans le menu: 
#                 # if self.pompe1default and not message1 in self.defautelec_message:
#                 #         self.defautelec_message += self.dateofdefault1 + message1
#                 # if self.pompe2default and not message2 in self.defautelec_message:
#                 #         self.defautelec_message += self.dateofdefault2 + message2
                
#                 self.defautelec_message = (self.dateofdefault1 + message1)*self.pompe1default + (self.dateofdefault2 + message2)*self.pompe2default

#                 # ## Gestion du bandeau de texte:
#                 # if len(self.defautelec_message) > max_bandeau :
#                 #         if incr_bandeau == len(self.defautelec_message) : incr_bandeau = 0
#                 #         elif incr_bandeau < (len(self.defautelec_message)-max_bandeau) :
#                 #                 bandeau = self.defautelec_message[incr_bandeau:(incr_bandeau+max_bandeau)]
#                 #                 incr_bandeau += 1
#                 #         else:
#                 #                 bandeau = self.defautelec_message[(incr_bandeau+max_bandeau)%max_bandeau:incr_bandeau]
#                 #                 incr_bandeau += 1
#                 bandeau = self.defautelec_message

#                 self.SystemSignal.emit(IhmSeuilNTB_var,self.niveau_cuve,bandeau)
#                 sleep(1)
                
        
#     @Slot(float,float)
#     def Write_modbus_float(self,addr,obj):
#         log.debug(f"Variable de type float écrite à l'adresse {addr} par modbus: {obj}")
#         if addr == 101:
#                 self.IhmSeuilNTB = obj
                

#     @Slot(float,bool)
#     def Write_modbus_boolean(self,addr, obj):
#         log.debug(f"Variable de type boolean écrite à l'adresse {addr} par modbus: {obj}")
#         if addr == 54:
#                 self.pompe1default = obj
#                 if obj:
#                         self.dateofdefault1 = Get_clean_datetime()
#         if addr == 75:
#                 self.pompe2default = obj
#                 if obj:
#                         self.dateofdefault2 = Get_clean_datetime()
