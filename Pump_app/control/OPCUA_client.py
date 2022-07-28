import asyncio
import sys
sys.path.insert(0, "..")
from asyncua import Client, Node, ua
from colorama import Fore
from logger import *


class SubscriptionHandler:
    def datachange_notification(self, node: Node, val, data):
        """Callback for asyncua Subscription"""
        log.info(Fore.BLUE+f"Value for node {node.nodeid.Identifier} : {val} -- with data: {data}"+Fore.RESET)
        


class OperaMetrix_OPCUA_client():
    
    def __init__(self,url = 'opc.tcp://localhost:4840/freeopcua/server/',uri = "http://edge-proxy.operametrix.fr"):
        self.url = url
        self.uri = uri
        self.nodes = []
        self.handler = SubscriptionHandler()
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
        # self.idx = 2
        log.info(f"INDEX: {self.idx}")
        
    
    
    def _close(self):
        self.client.disconnect()


if __name__ == "__main__":
    
    Myclient = OperaMetrix_OPCUA_client()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Myclient.run())
    print(Fore.GREEN+"on en sors!"+Fore.RESET)
    loop.close()