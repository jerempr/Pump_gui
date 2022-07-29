# import libraries
import sys
import os

from logger import *


# try:
#     import PySide2.QtQml
# except ImportError:
# 	import PyQt5.QtQml
if 'PyQt5' in sys.modules:
	from PyQt5.QtQml import QQmlApplicationEngine
	from PyQt5.QtWidgets import *
	from PyQt5.QtCore import *
	log.info("this app use pyqt5")
else:
	from PySide2.QtQml import QQmlApplicationEngine
	from PySide2.QtWidgets import *
	from PySide2.QtQuick import *
	from PySide2.QtCore import *
	log.info("this app use pyside2")

from NetInfo import Netinfo
from SysInfo import Sysinfo
from ReterminalInfo import Reterminalinfo
from OpcuaInfo import OPCUAinfo
from OPCUA_client import OperaMetrix_OPCUA_client

import asyncio
import asyncqt

      
        

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
    opcuainfo = OPCUAinfo()
    reterminalinfo = Reterminalinfo()
    
    
    #classe de récupération de variable opc-ua
    OPCclient = OperaMetrix_OPCUA_client()
    # Add close async interruption:
    # création de la boucle qui va permettre l'interruption de fermeture d'application
    loop = asyncqt.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Rends les composants utilisables pour les .qml
    context.setContextProperty("_Sysinfo", sysinfo)
    context.setContextProperty("_OPCUAinfo", opcuainfo)
    context.setContextProperty("_Netinfo", netinfo)
    context.setContextProperty("_Reterminalinfo", reterminalinfo)
    
    opcuainfo.first_call()
    sysinfo.start()
    netinfo.start()
    
    engine.load(url)
    
    log.info("Avant lancement des boucles!")
    #On lance la boucle d'interruption puis l'application
    loop = asyncio.get_event_loop()
    # loop.create_task(reterminalinfo.btn_coroutine())
    loop.create_task(OPCclient.run())
    loop.run_forever()
    log.info("Apres lancement des boucles!")
    app.exec_()
    

        