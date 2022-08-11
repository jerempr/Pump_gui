from logger import *
from colorama import Fore

from asyncua import Client, Node, ua
import asyncio


from time import sleep

import sys

class OperaMetrix_OPCUA_client():
    """Client for opcua. Needs a handler to handle the suscriptions nodes changes notifications.
    """ 
    def __init__(self,handler,url = 'opc.tcp://localhost:4840/freeopcua/server/',uri = "http://edge-proxy.operametrix.fr"):
        log.info("trying to use OPCUA communication...")
        self.url = url
        self.uri = uri
        self.nodes = []
        self.handler = handler
        self.object = "API_local"
        self.My_addresses = []
        self._get_addr_list()
        
        log.info("we are using OPCUA communication")

        
    async def run(self):
        """
        task to launch the client with.
        """
        log.info("Running task opcua!")
        await self._connect()
        
        
    async def _run_afterconnect(self):
        """
        running function after connexion, it will call the subscribe function and then wait for an error to occur.
        """
        await self._subscribe("Valeur_Niveau_cuve")
        self.handler.first_call()
        while True:
            await asyncio.sleep(20)
            try:
                await self.client.send_hello()
            except AttributeError:
                log.warning("Connexion to the OPCUA server closed! We will try to reconnect...")
                break
        # self._close()
        self.handler.warn_closed_connexion()
        return await self.run()
    
    async def _subscribe(self):
        """allows to subscribe to all the nodes written in a file add_toread.yaml that must be in the same directory
        """
        self.idx = await self.client.get_namespace_index(self.uri)
        # log.info(f"INDEX: {self.idx}")
        self.subscription = await self.client.create_subscription(500, self.handler)
        for addr_name in self.My_addresses:
            self.nodes.append(self.client.get_node(ua.NodeId(f"{self.object}:{addr_name}",self.idx)))
        print (f"Nodes: {self.nodes}")
        await self.subscription.subscribe_data_change(self.nodes)
        
    
    async def _connect(self):
        """This function allows to wait for connexion to the opcua server.
        """
        while True:
            try:
                self.client = Client(url=self.url)
                async with self.client:
                    await self.client.send_hello()
                    log.info("We connected successfully to the server !")
                    await self._run_afterconnect()
                break
            except (OSError,asyncio.exceptions.TimeoutError):
                log.warning(f"{sys.exc_info()[0]}: No connexion found to the opcua server... Retrying ...")
                sleep(2)
            except:
                log.error(f"Unexpected error:{sys.exc_info()[0]}")
                raise
        
        
        
    def _get_addr_list(self):
        """
        parse the file addr_toread to get the nodes names that we need to subscribe to
        """
        file = open('addr_toread.yaml', 'r')
        for line in file:
            if line[0] != "#":
                self.My_addresses.append(line.strip('\n'))
            
    
    async def _close(self):
        """delete subscriptions and disconnect to the server
        """
        await self.subscription.unsubscribe(self.handle)
        await self.subscription.delete()
        self.client.disconnect()
