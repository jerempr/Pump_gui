from optparse import Values
from pymodbus3.client.sync import ModbusTcpClient
from pymodbus3.constants import Endian
from pymodbus3.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from logger import *
from colorama import Fore


from asyncua import Client, Node, ua
import asyncio

# import logging
# # --------------------------------------------------------------------------- #
# # log config
# # --------------------------------------------------------------------------- #
# FORMAT = (
#     "%(asctime)-15s %(threadName)-15s "
#     "%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
# )
# logging.basicConfig(format=FORMAT)
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)


# UNIT = 0x01

class SubscriptionHandler:
    def datachange_notification(self, node: Node, val, data):
        """Callback for asyncua Subscription"""
        log.info(Fore.BLUE+f"Value for node {node.nodeid.Identifier} : {val} -- with data: {data}"+Fore.RESET)

class OperaMetrix_OPCUA_client():
    def __init__(self,url = 'opc.tcp://localhost:4840/freeopcua/server/',uri = "http://edge-proxy.operametrix.fr"):
        log.info("trying to use OPCUA communication...")
        self.url = url
        self.uri = uri
        self.nodes = []
        self.handler = SubscriptionHandler()
        self.object = "API_local"
        self.client = Client(url=self.url)
        log.info("we are using OPCUA communication")

        
    async def run(self):
        log.info("Running task opcua!")
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
        # self.idx = 2
        log.info(f"INDEX: {self.idx}")
        
    
    
    def _close(self):
        self.client.disconnect()
