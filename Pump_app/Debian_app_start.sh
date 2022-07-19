#!/bin/sh

modprobe lis331dlh-i2c
echo "changing eth0 IP work with API... "
sudo ip a a 192.168.0.200/24 dev eth0
echo "eth0 IP changed to to 192.168.0.200 to math API IP"
#ip a
echo "loading qt demo..."
export QT_QPA_PLATFORM=eglfs
export QT_QPA_EGLFS_ALWAYS_SET_MODE=1
export QT_QPA_EGLFS_PHYSICAL_WIDTH=1280
export QT_QPA_EGLFS_PHYSICAL_HEIGHT=720
# in order to not show the warning message:
# export XDG_RUNTIME_DIR='/var/volatile/tmp/runtime-root'
cd /home/pi/gui/Pump_gui/Pump_app/control/
echo "qt demo start ok!"
# python3 main.py
python3 main.py>../Guilogs 2>&1
echo "end of qt demo"
rm /home/pi/gui/Pump_gui/Pump_app/*/*.qmlc

