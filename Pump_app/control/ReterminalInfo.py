import sys
import os
from time import sleep

try:
        from PySide2.QtCore import *
except ImportError:
        from PyQt5.QtCore import *
if 'PyQt5' in sys.modules:
        from PyQt5.QtCore import pyqtSignal as Signal
else:
        from PySide2.QtCore import Signal, Slot


from logger import log


import asyncqt
import seeed_python_reterminal.core as rt
import seeed_python_reterminal.button as rt_btn
 
 


#class to handle the eth and wifi infos
class Reterminalinfo(QThread):
        """this class allows to use the Reterminal interface such as leds, buzzer, buttons or accelerometer
        """
        SystemSignal = Signal(bool)
        
        def __init__(self):
                super().__init__()
                print ("Reterminalinfo class instancied")
                self.btn_device = rt.get_button_device()
                self.UsrGreenOff()
                self.Close_popup = False
                
        @asyncqt.asyncSlot()
        async def btn_coroutine(self):
                async for event in self.btn_device.async_read_loop():
                        self.UsrGreenOff()
                        buttonEvent = rt_btn.ButtonEvent(event)
                        if buttonEvent.name != None:
                                # log.info(f"name={str(buttonEvent.name)} value={buttonEvent.value}")
                                # check if we are pushing the right button
                                if buttonEvent.name == rt_btn.ButtonName.O and buttonEvent.value == 1:
                                        self.UsrGreenOn()
                                        self.SystemSignal.emit(True)
                                        # self.sleep(3)
                                else:
                                        self.SystemSignal.emit(False)
                                        self.UsrGreenOff()
                                        

        # close
        @Slot()
        def closeWindow(self):
                os.system("rm /home/pi/gui/gui_test/Debian_Pompe/*/*.qmlc")
                sys.exit()
                
        @Slot()
        def Reboot(self):
                os.system("sudo shutdown -r +1")
                log.info("Thanks, the system will reboot now")
                os.system("cp /home/pi/gui/Pump_gui/Pump_app/Guilogs /home/pi/gui/Pump_gui/Pump_app/Old_guilogsbeforereboot")
                sys.exit()
                
        def UsrGreenOn(self):
                os.system("sudo sh -c 'echo 255 > /sys/class/leds/usr_led0/brightness'")
        
        def UsrGreenOff(self):
                os.system("sudo sh -c 'echo 0 > /sys/class/leds/usr_led0/brightness'")
        
        @Slot()
        def  Close_popup(self):
                self.UsrGreenOff()
                       


                
                
                
                
        
