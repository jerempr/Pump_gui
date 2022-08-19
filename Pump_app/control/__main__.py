# import libraries
import sys
import os

# from logger import *

try:
	import PySide2.QtQml
except ImportError:
	import PyQt5.QtQml
if 'PyQt5' in sys.modules:
	from PyQt5.QtQml import QQmlApplicationEngine
	from PyQt5.QtWidgets import *
	from PyQt5.QtCore import *
	print("this app use pyqt5")
else:
	from PySide2.QtQml import QQmlApplicationEngine
	from PySide2.QtWidgets import *
	from PySide2.QtQuick import *
	from PySide2.QtCore import *
	print("this app use pyside2")



from Pump_app.control.providers.NetInfo import Netinfo
from Pump_app.control.providers.OpcuaInfo import Opcuainfo
from Pump_app.control.providers.SysInfo import Sysinfo
from Pump_app.control.providers.ReterminalInfo import Reterminalinfo

from Pump_app.control.providers.OPCUA_Client import OperaMetrix_OPCUA_client
 

import asyncio
import asyncqt

import threading


import argparse
import logging



def config_argument():
    """configurate our arguments parsing
    """
    parser = argparse.ArgumentParser(description="Edge-Proxy proxifies anything to OPC:UA.")
    parser.add_argument(
        "-l",
        "--log-level",
        type=str,
        default="error",
        choices=["debug", "info", "warning", "error", "critical"],
        help="debug output (caution, sensitive informations may appears in clear text)",
    )
    parser.add_argument("-f", "--foreground", action="store_true", help="foreground execution")
    return parser.parse_args()

def config_logging(args):
    """configure our logging

    Args:
        args : arguments of the main call
    """
    # --------------------------------------------------------------------------- #
    # log config
    # --------------------------------------------------------------------------- #
    FORMAT = (
        "%(asctime)-15s %(threadName)-15s "
        "%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
    )
    logging.basicConfig(format=FORMAT)
    log = logging.getLogger()
    log.setLevel(getattr(logging, args.log_level.upper()))


def Launch_OPCUA(opcuaclient):
    """Tread launching opcua client

    Args:
        handler : handler for the opcua client subscriptions
    """
    opcloop = asyncio.new_event_loop()
    asyncio.set_event_loop(opcloop)
    opcloop.run_until_complete(opcuaclient.run())
    opcloop.close()



# launch the app
if __name__ == '__main__':
    """
    Main entry point
    """
    args = config_argument()
    config_logging(args)
    
    log = logging.getLogger(__name__)

    app = QApplication([])
    engine = QQmlApplicationEngine()
    
    
    # location of the fullscreen app that we created before
    if "Debian" in os.popen('hostnamectl').read().strip():
        url = QUrl("Pump_app/QML_UI/App_Debian.ui.qml")
    else:
        url = QUrl("Pump_app/QML_UI/App.ui.qml")
        
    
    context = engine.rootContext()
    
    # Récupère les classes créées dans les dépendances:
    sysinfo = Sysinfo()
    netinfo = Netinfo()
    opcuainfo = Opcuainfo()
    reterminalinfo = Reterminalinfo()
    
    #initialise the client
    Myclient = OperaMetrix_OPCUA_client(handler = opcuainfo )


    # Rends les composants utilisables pour les .qml and start classes
    context.setContextProperty("_Sysinfo", sysinfo)
    context.setContextProperty("_Netinfo", netinfo)
    context.setContextProperty("_Opcuainfo", opcuainfo)
    context.setContextProperty("_Reterminalinfo", reterminalinfo)
    context.setContextProperty("_OPCclient", Myclient)

    sysinfo.start()
    netinfo.start()

    
    log.info("begin to create the loops...")
    
    #loop to handle opcua client
    T_opcua = threading.Thread(target=Launch_OPCUA, args = (Myclient,))
    T_opcua.setDaemon(True)
    T_opcua.start()
    
    engine.load(url)
    # app.exec()

    # loop for handling reTerminal buttons
    loop = asyncqt.QEventLoop(app)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(reterminalinfo.btn_coroutine())

    log.info("opcua loop created!")
    log.info("reTerminal buttons loop created!")


    log.info("launching the app !")
    engine.load(url)
    app.exec()
    
