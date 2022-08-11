# import libraries
import sys
import os

from logger import *

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

from NetInfo import Netinfo
from OpcuaInfo import Opcuainfo
from SysInfo import Sysinfo
from ReterminalInfo import Reterminalinfo
 
from OPCUA_Client import OperaMetrix_OPCUA_client
 

import asyncio
import asyncqt

import threading


def Launch_OPCUA(handler):
    Myclient = OperaMetrix_OPCUA_client(handler)
    opcloop = asyncio.new_event_loop()
    asyncio.set_event_loop(opcloop)
    opcloop.run_until_complete(Myclient.run())
    # print(Fore.GREEN+"on en sors!"+Fore.RESET)
    opcloop.close()

def Launch_reterminalinfo(loop,reterminalinfo):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(reterminalinfo.btn_coroutine())


# launch the app
if __name__ == '__main__':
    app = QApplication([])
    engine = QQmlApplicationEngine()
    engine.addImportPath("../imports")
    os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
    
    
    
    # Hide the mouse:
    
    # location of the fullscreen app that we created before
    if "Debian" in os.popen('hostnamectl').read().strip():
        url = QUrl("../QML_UI/App_Debian.ui.qml")
    else:
        url = QUrl("../QML_UI/App.ui.qml")
        
    
    context = engine.rootContext()
    
    # Récup-re les classes créées dans les dépendances:
    sysinfo = Sysinfo()
    netinfo = Netinfo()
    opcuainfo = Opcuainfo()
    reterminalinfo = Reterminalinfo()
    
    # Rends les composants utilisables pour les .qml
    context.setContextProperty("_Sysinfo", sysinfo)
    context.setContextProperty("_Netinfo", netinfo)
    context.setContextProperty("_Opcuainfo", opcuainfo)
    context.setContextProperty("_Reterminalinfo", reterminalinfo)
    
    sysinfo.start()
    netinfo.start()

    
    log.info("begin to create the loops...")
    
    #loop to handle opcua client
    T_opcua = threading.Thread(target=Launch_OPCUA, args = (opcuainfo,))
    T_opcua.setDaemon(True)
    T_opcua.start()
    
    engine.load(url)
    # app.exec()

    # loop for handling reTerminal buttons
    loop = asyncqt.QEventLoop(app)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(reterminalinfo.btn_coroutine())
    # T_reterminalinfo = threading.Thread(target=Launch_reterminalinfo,args = (loop,reterminalinfo,))
    # T_reterminalinfo.setDaemon(True)
    # T_reterminalinfo.start()
    




    log.info("opcua loop created!")
    log.info("reTerminal buttons loop created!")


    log.info("launching the app !")
    engine.load(url)
    app.exec()
    
