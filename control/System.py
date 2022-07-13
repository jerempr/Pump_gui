# import libraries
import sys
import os



if 'PyQt5' in sys.modules:
	from PyQt5.QtCore import QObject, pyqtSlot as Slot
	print("this app use pyqt5")
else:
	from PySide2.QtCore import *
	print("this app use pyside2")
 
# class to handle button controls
class Setting(QObject):
    # close
    @Slot()
    def closeWindow(self):
        os.system("rm /home/pi/gui/gui_test/Debian_Pompe/*/*.qmlc")
        sys.exit()

