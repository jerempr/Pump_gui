import sys
sys.path.insert(0, "..")

from time import sleep

import asyncio
import logging
from colorama import Fore

from asyncua import Client, Node, ua

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


class SubscriptionHandler:
    def datachange_notification(self, node: Node, val, data):
        """Callback for asyncua Subscription"""
        # _logger.info('datachange_notification %r %s', node.nodeid, val)
        _logger.info(Fore.BLUE+f"Value for node {node.nodeid.Identifier} : {val} -- with data: {data}"+Fore.RESET)


async def main():
    url = 'opc.tcp://localhost:4840/freeopcua/server/'
    client = Client(url=url)
    nodes = []
    # client.set_security_string()
    async with client:
        uri = "http://edge-proxy.operametrix.fr"
        idx = await client.get_namespace_index(uri)
        print (f"INDEX: {idx}")
        object = "API_local"
        # var = await client.nodes.objects.get_child([f"{idx}:API_local", f"{idx}:Valeur_Niveau_cuve"])
        # var = await client.nodes.objects.get_child([f"{idx}:API_local", f"{idx}:Ihm_Volume_Niveau_Tres_Haut"])
        node = client.get_node(ua.NodeId(f"{object}:Valeur_Niveau_cuve",2))
        nodes.append(node)
        print (f"Nodes: {nodes}")

        handler = SubscriptionHandler()
        subscription = await client.create_subscription(500, handler)
        # nodes = [
        #     var,
        #     client.get_node(ua.ObjectIds.Server_ServerStatus_CurrentTime),
        # ]
        await subscription.subscribe_data_change(nodes)
        while True:
        # print (Fore.RED+f"subscription value change: {subscription}"+Fore.RESET)
            await asyncio.sleep(10)


async def forever():
    while(1):
        await main()

if __name__ == "__main__":
    
    
    loop = asyncio.get_event_loop()
    # loop.create_task(main())
    # loop.run_forever()
    loop.run_until_complete(main())
    print(Fore.GREEN+"on en sors!"+Fore.RESET)
    # loop.
    loop.close()