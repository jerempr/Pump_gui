import asyncio
import sys
sys.path.insert(0, "..")
from asyncua import Client, Node, ua
from colorama import Fore
from logger import *


try:
        from PySide2.QtCore import *
except ImportError:
        from PyQt5.QtCore import *
if 'PyQt5' in sys.modules:
        from PyQt5.QtCore import pyqtSignal as Signal
        from PyQt5.QtCore import pyqtSlot as Slot
else:
        from PySide2.QtCore import Signal, Slot



class OPCUAinfo:
    SystemSignal = Signal(str,bool,str,str,bool,bool)
    
    
    def first_call(self):
        """à appeller pour avoir les valeurs au lancement de l'application (sans interrputions"""
        self.SystemSignal.emit("",False,"5.1","",True,False)
        
    
    def datachange_notification(self, node: Node, val, data):
        """Callback for asyncua Subscription"""
        log.info(Fore.BLUE+f"Value for node {node.nodeid.Identifier} : {val} -- with data: {data}"+Fore.RESET)
        self.SystemSignal.emit("",False,"5.1","",True,False)

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


class OperaMetrix_OPCUA_client():
    
    SystemSignal = Signal(str)
        
    def __init__(self,url = 'opc.tcp://localhost:4840/freeopcua/server/',uri = "http://edge-proxy.operametrix.fr"):
        self.url = url
        self.uri = uri
        self.nodes = []
        self.handler = OPCUAinfo()
        self.object = "API_local"
        self.client = Client(url=self.url)

        
    async def run(self):
        async with self.client:
            await self._connect()
            await self._subscribe("Valeur_Niveau_cuve")
            await self._keepalive()
            while True:
                await asyncio.sleep(20)
        
    
    
    async def _subscribe(self, name:str):
        self.subscription = await self.client.create_subscription(500, self.handler)
        self.nodes.append(self.client.get_node(ua.NodeId(f"{self.object}:{name}",self.idx)))
        print (f"Nodes: {self.nodes}")
    
    async def _keepalive(self):
        await self.subscription.subscribe_data_change(self.nodes)
    
    async def _connect(self):
        self.root = self.client.get_root_node()
        self.idx = await self.client.get_namespace_index(self.uri)
        self.handler.first_call()
        log.info(f"INDEX: {self.idx}")
                
    def _close(self):
        self.client.disconnect()


