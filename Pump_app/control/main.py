# import libraries
import sys
import os



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
from ModbusInfo import Modbusinfo
from SysInfo import Sysinfo
from ReterminalInfo import Reterminalinfo
 

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
    modinfo = Modbusinfo()
    reterminalinfo = Reterminalinfo()
    
    
    # Add close async interruption:
    # création de la boucle qui va permettre l'interruption de fermeture d'application
    loop = asyncqt.QEventLoop(app)
    asyncio.set_event_loop(loop)
    

    # Rends les composants utilisables pour les .qml
    context.setContextProperty("_Sysinfo", sysinfo)
    context.setContextProperty("_Netinfo", netinfo)
    context.setContextProperty("_Modbusinfo", modinfo)
    context.setContextProperty("_Reterminalinfo", reterminalinfo)
    
    sysinfo.start()
    netinfo.start()
    modinfo.start()
    
    engine.load(url)
    #On lance la boucle d'interruption puis l'application
    with loop:
            loop.run_until_complete(reterminalinfo.btn_coroutine())
    app.exec_()
    
