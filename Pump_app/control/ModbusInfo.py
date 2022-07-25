## Importations
from math import nan
import sys

import threading

from numpy import NaN
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
        """This class allows the modbus reading and writing 
        Args:
            QThread (_type_): _description_
        """
        
        SystemSignal = Signal(str,bool,str,str,bool,bool)
        
        def __init__(self):
                super().__init__()
                self.Myclient = OperaMetrix_ModbusTCP_client()
                self.Myclient.connect()
                
                ## Variables to fill with modbus infos
                self.niveau_cuve = 5
                # Booleans about pump functionnality
                self.pompe2default = False
                self.pompe1default = False
                self.marchep1 = False
                self.marchep2 = False
                # Messages to print depending of the pump defaults
                self.defautelec_message = ""
                self.dateofdefault1 = ""
                self.dateofdefault2 = ""
                # booleans:
                self.GraisseOn = False
                # list:
                self.Ihm_parameters =""
                
                # Tables de valeurs (format string)
                self.Table = []
                # Create a mutex to handle the modbus connection
                self.MUTEX = False
                
                
                # Création d'un thread de lecture modbus:
                self.T_modbus = threading.Thread(target=self.ReadModbus)
                self.T_modbus.setDaemon(True)
                self.T_modbus.start()
                log.info("Beginning of thread reading modbus addresses")

                

        
        def ReadModbus(self):
                """Allows to get all needed modbus addresses values"""
                self.Wait_for_mutex()
                self.Get_Ihm_parameters()
                self.niveau_cuve = self.Myclient.Read_addr(87)
                self.Ihm_parameters = self.Get_Ihm_parameters()
                self.Get_Pumps_defaults()
                self.GraisseOn = self.Myclient.Read_addr(113,'bool')
                self.MUTEX = False
                sleep (.5)
                self.ReadModbus()
        
        
        def run(self):
                """Here we emit the read modbus values
                """
                message1 = ":<b>  - Défaut sur la pompe 1 -  </b>"
                message2 = ":<b>  - Défaut sur la pompe 2 -  </b>"
                Ihmparams = ""
                while(True):
                        ## traitement de ces valeurs afin de les envoyer à l'Ihm:
                        # get the date of defaults if there is some
                        self.dateofdefault1 = attribute_default_pump_datetime(self.pompe1default,self.dateofdefault1)
                        self.dateofdefault2 = attribute_default_pump_datetime(self.pompe2default,self.dateofdefault2)
                        self.defautelec_message = (self.dateofdefault1 + message1)*self.pompe1default + (self.dateofdefault2 + message2)*self.pompe2default
                        
                        # Envoi de ces valeurs à l'Ihm:
                        self.Wait_for_mutex()
                        self.SystemSignal.emit(self.Ihm_parameters,self.GraisseOn,str(self.niveau_cuve),self.defautelec_message,self.marchep1,self.marchep2)
                        self.MUTEX = False
                        sleep(1)
        
 
        def Get_Ihm_parameters(self):
                """allows to get all the parameters of the ihm:
                ## Return a table with (as string separated by ',') :
                - Ihm seuil niveau bas
                - Ihm seuil niveau haut
                - Ihm seuil niveau très bas
                - Ihm seuil niveau très haut
                - Temps de Décalage
                - Offset anneau Graisse
                - Valeur mini niveau
                - Valeur maxi niveau
                """
                Table = ""
                for k in range(97,113,2):
                        Table+=","+(str(round(self.Myclient.Read_addr(k),2)))
                Table+=","+(str(round(self.Myclient.Read_addr(89),2)))
                Table+=","+(str(round(self.Myclient.Read_addr(91),2)))
                return Table.replace(",","",1)
        
        
        def Get_Pumps_defaults(self):
                """allows to get all the parameters of the ihm:
                ## Return a table with (as string separated by ',') :
                - retour marche pompe 1
                - retour marche pompe 2
                - Ihm seuil niveau très bas
                - Ihm seuil niveau très haut
                - Temps de Décalage
                - Offset anneau Graisse
                - Valeur mini niveau
                - Valeur maxi niveau
                """
                self.marchep1 = self.Myclient.Read_addr(54,"bool")
                self.marchep2 = self.Myclient.Read_addr(75,"bool")
                self.pompe2default = self.Myclient.Read_addr(75.05,"bool")
                self.pompe1default = self.Myclient.Read_addr(54.05,"bool")
                
        
        def Wait_for_mutex(self):
                """this function allows to wait until the mutex is free. 
                When he is, he is then put to True and the code can continue
                """
                if self.MUTEX:
                        sleep(1)
                        return self.Wait_for_mutex
                else:
                        self.MUTEX = True
                        exit


        @Slot(int,float)
        def Write_modbus_float(self,addr,obj):
                """this function allows to write a float to modbus tcp
                # Args:
                    - addr (int): address where you want to write
                    - obj (float): the float number you want to write
                """
                if float(obj) == float(obj) and obj != "" :
                        self.Wait_for_mutex()
                        log.info(f"Variable de type float écrite à l'adresse {addr} par modbus: {obj}")
                        self.Myclient.Write_addr(addr,float(obj))
                        self.MUTEX = False
                

        @Slot(float,bool)
        def Write_modbus_boolean(self,addr, obj):
                """this function allows to write a boolean to modbus tcp
                # Args:
                    - addr (int): address where you want to write
                    - obj (bool): the bool value you want to write
                """
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
#     SystemSignal = Signal(str,bool,str,str,bool,bool)
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

#                 Ihm_table = "5,3,2.5,6,8,5,10,0.5,10,0"
                
                
#                 self.SystemSignal.emit(Ihm_table,True,str(self.niveau_cuve/40),self.defautelec_message,False,False)
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
