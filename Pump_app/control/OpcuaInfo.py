import sys
import os
from time import sleep

try:
        from PySide2.QtCore import *
except ImportError:
        from PyQt5.QtCore import *
if 'PyQt5' in sys.modules:
        from PyQt5.QtCore import pyqtSignal as Signal
        from PyQt5.QtCore import pyqtSlot as Slot
else:
        from PySide2.QtCore import Signal, Slot


from logger import log

import asyncio

import asyncqt
import seeed_python_reterminal.core as rt
import seeed_python_reterminal.button as rt_btn
 
 


class OPCUAinfo(QThread):
    SystemSignal = Signal(str,bool,str,str,bool,bool)
    
    def __init__(self):
        super().__init__()
        log.info("Initialisation classe OPCUAinfo")
        # self.SystemSignal.emit("",False,"5.1","",True,False)

    
    def first_call(self):
        """à appe
        ller pour avoir les valeurs au lancement de l'application (sans interrputions"""
        log.info("First call of OPCUAinfo!!")
        # self.SystemSignal.emit("",False,"5.1","",True,False)
        
    
    # def datachange_notification(self, node: Node, val, data):
    #     """Callback for asyncua Subscription"""
    #     log.info(Fore.BLUE+f"Value for node {node.nodeid.Identifier} : {val} -- with data: {data}"+Fore.RESET)
    #     self.SystemSignal.emit("",False,"5.1","",True,False)

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
        
                       


                
                
                
                
        
