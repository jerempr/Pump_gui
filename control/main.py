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
from System import Setting
from ModbusInfo import Modbusinfo
from SysInfo import Sysinfo
 



# launch the app
if __name__ == '__main__':
    app = QApplication([])
    engine = QQmlApplicationEngine()
    engine.addImportPath("../imports")
    os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

    # Hide the mouse:
    
    # location of the fullscreen app that we created before
    url = QUrl("../QML_UI/App.ui.qml")
    
    context = engine.rootContext()
    
    # Récup-re les classes créées dans les dépendances:
    seting = Setting()
    netinfo = Netinfo()
    modinfo = Modbusinfo()
    sysinfo = Sysinfo()


    # Rends les composants utilisables pour les .qml
    context.setContextProperty("_Setting", seting)
    context.setContextProperty("_Netinfo", netinfo)
    context.setContextProperty("_Modbusinfo", modinfo)
    context.setContextProperty("_Sysinfo", sysinfo)
    
    netinfo.start()
    modinfo.start()
    sysinfo.start()
    
    engine.load(url)
    app.exec_()
