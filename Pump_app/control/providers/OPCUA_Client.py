# from logger import *
from colorama import Fore
from dataclasses import dataclass
from asyncua import Client, Node, ua
import asyncio
import logging
log = logging.getLogger(__name__)

from time import sleep
import yaml
import sys

try:
        from PySide2.QtCore import *
except ImportError:
        from PyQt5.QtCore import *
if 'PyQt5' in sys.modules:
        from PyQt5.QtCore import pyqtSignal as Signal
        from PyQt5.QtCore import pyqtSlot as Slot
else:
        from PySide2.QtCore import Signal, Slot




@dataclass
class Register:
    name: str
    type: str
    address: int = 0
    writable: bool = False
    position: int = 0




class OperaMetrix_OPCUA_client(QThread):
    """Client for opcua. Needs a handler to handle the suscriptions nodes changes notifications.
    """ 
    def __init__(self,handler,url = 'opc.tcp://localhost:4840/freeopcua/server/',uri = "http://edge-proxy.operametrix.fr"):
        # for QT
        super().__init__()
        log.debug("Initialisation classe OPCUAinfo")
        
        # for client:
        log.info("trying to use OPCUA communication...")
        self.url = url
        self.uri = uri
        self.nodes = []
        self.handler = handler
        self.OBJECT_NAME = "API_local"
        self.My_addresses = []
        # self._get_addr_list()
        self._towrite = []
        self._parse_registers('/home/root/GUI_Demo_Custom/Pump_app/control/providers/addr_toread.yml')
        log.info("we are using OPCUA communication")

        
    async def run(self):
        """
        task to launch the client with.
        """
        log.info("Running task opcua!")
        await self._connect()
        
    def _parse_registers(self,config: str):
        """parse the registers that we want to read and/or write
        Args:
            config (str): config yaml file
        """
        self._myadresses=[]
        self._myadresses_dict = {}
        with open(config) as file:
            data = yaml.load(file,Loader=yaml.FullLoader)
            for address in data:
                if address['writable']:
                    if address['type'] == 'Boolean':
                        new_addr = Register(
                            name=str(address['name']), type=str(address['type']), address=int(address['address']), writable=bool(address['writable']), position=int(address['position'])
                        )
                    else:
                        new_addr = Register(
                            name=str(address['name']), type=str(address['type']), address=int(address['address']), writable=bool(address['writable'])
                        )
                    self._myadresses_dict[new_addr.name] = new_addr
                else:
                    new_addr = Register(
                            name=str(address['name']), type=str(address['type']), writable=bool(address['writable'])
                        )
                self._myadresses.append(new_addr)



    async def _connect(self):
        """This function allows to wait for connexion to the opcua server.
        """
        while True:
            try:
                self.client = Client(url=self.url)
                async with self.client:
                    await self.client.send_hello()
                    log.info("We connected successfully to the server !")
                    await self._run_everythingisfine()
                break
            except (OSError,asyncio.exceptions.TimeoutError):
                log.warning(f"{sys.exc_info()[0]}: No connexion found to the opcua server... Retrying ...")
                sleep(2)
            except:
                log.error(f"Unexpected error:{sys.exc_info()[0]}")
                raise


    async def _run_everythingisfine(self):
        """
        running function after connexion, it will call the subscribe function and then wait for an error to occur.
        """
        loopcounter = 0
        await self._subscribe()
        self.handler.first_call()
        self.objects = self.client.nodes.objects
        # log.info (Fore.GREEN + f"objects: {objects}" + Fore.RESET)
        while True:
            await asyncio.sleep(0.5)
            if self._towrite :
                log.info("we have something to write")
                command = self._towrite.pop(0)
                await self._write_to_node(command[0],command[1],command[2])
            loopcounter += 1
            if loopcounter == 40:
                try:
                    await self.client.send_hello()
                    loopcounter = 0
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
        log.info(f"INDEX: {self.idx}")
        self.subscription = await self.client.create_subscription(500, self.handler)
        for node in self._myadresses:
            self.nodes.append(self.client.get_node(ua.NodeId(f"{self.OBJECT_NAME}:{node.name}",self.idx)))
        print (f"Nodes: {self.nodes}")
        await self.subscription.subscribe_data_change(self.nodes)
        
        
        
    # def _get_addr_list(self):
    #     """
    #     parse the file addr_toread to get the nodes names that we need to subscribe to
    #     """
    #     file = open('/home/root/GUI_Demo_Custom/Pump_app/control/providers/addr_toread.yaml', 'r')
    #     for line in file:
    #         if line[0] != "#":
    #             self.My_addresses.append(line.strip('\n'))


    @Slot(str,float)
    def Write_node(self, node_name: str, obj: float):
        """allows a call from qml to write to a modbus value

        Args:
            node_name (str): the name of the node where we want to write
            obj (float): what we want to write
        """
        node_towrite = self._myadresses_dict[node_name]
        self._towrite.append([node_name,obj,node_towrite.type])

        # self.
        # for node in self._myadresses:
        #     if node.name == node_name:
        #         if node.writable:
        #             if node.type == 'Float':
        #                 self.towrite.append([node_name,obj,node.type])
        #             elif node.type == 'Boolean':
        #                 self.towrite.append([node_name,obj,node.type])
        #             else:
        #                 log.error(f"bad type '{node.type}' name for write command to node {node_name}")
        #         else:
        #             log.error(f"the node {node_name} was called as writable but is not")
        # writingloop = asyncio.new_event_loop()
        # asyncio.set_event_loop(writingloop)
        # writingloop.run_until_complete(self._write_to_node(node_name,obj))
        # writingloop.close()


    async def _write_to_node(self,node_name: str, obj, type: str):
        child = await self.objects.get_child(['2:API_local',f'2:{node_name}']) # get the node where we want to write 
        print (Fore.GREEN + f"writing {obj} to this node: {child}" + Fore.RESET) 
        value =  ua.DataValue(ua.Variant(obj, getattr(ua.VariantType,type))) # change the value to write to a good format
        print(f"value: {value}")
        await child.set_value(value)

    async def _close(self):
        """delete subscriptions and disconnect to the server
        """
        await self.subscription.unsubscribe(self.handle)
        await self.subscription.delete()
        self.client.disconnect()
