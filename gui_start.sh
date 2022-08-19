#!/bin/sh

modprobe lis331dlh-i2c

loglevel="${1:-'info'}"

export QT_QPA_PLATFORM=eglfs
export QT_QPA_EGLFS_ALWAYS_SET_MODE=1
export QT_QPA_EGLFS_HIDECURSOR=1

if [[ $(cat /etc/hostname | grep reterminal) ]]
then
    echo "loading qt demo..."
    # use gifs:
    # export PACKAGECONFIG_append=gif
    # in order to not show the warning message:
    export XDG_RUNTIME_DIR='/var/volatile/tmp/runtime-root'
    cd /home/root/GUI_Demo_Custom/

else
    echo "changing eth0 IP work with API... "
    sudo ip a a 192.168.0.200/24 dev eth0
    echo "eth0 IP changed to to 192.168.0.200 to match API IP"
    export QT_QPA_EGLFS_PHYSICAL_WIDTH=1280
    export QT_QPA_EGLFS_PHYSICAL_HEIGHT=720

    cd /home/pi/gui/Pump_gui/
fi

echo "qt demo starting..."
# python3 -m Pump_app.control  -l $loglevel
python3 -m Pump_app.control  -l info>Guilogs.log 2>&1
echo "end of qt demo"

if [[ $(cat /etc/hostname | grep raspberry) ]]
then
    rm /home/pi/gui/Pump_gui/Pump_app/*/*.qmlc
fi