#!/bin/sh

modprobe lis331dlh-i2c

echo "loading qt demo..."
export QT_QPA_PLATFORM=eglfs
export QT_QPA_EGLFS_ALWAYS_SET_MODE=1

# use gifs:
# export PACKAGECONFIG_append=gif
# in order to not show the warning message:
export XDG_RUNTIME_DIR='/var/volatile/tmp/runtime-root'
cd /home/root/GUI_Demo_Custom/control
echo "qt demo start ok!"
python3 main.py>../Guilogs 2>&1
echo "end of qt demo"
# echo "changing eth0 IP work with API... "
#ip a a 192.168.0.200/24 dev eth0
#echo "eth0 IP changed to to 192.168.0.200 to math API IP"
#ip a

