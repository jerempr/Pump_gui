// import libraries
import QtQuick 2.8
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.11
import "../backend/" as Data
 

 
/* The Item type is the base type for all visual items in Qt Quick. Here 1280 and 720 are chosen 
for the dimensions because the resolution of reTerminal LCD is 1280x720 */

Item {
    // identify the qml
    id: p3
    // define width and height of the app
    width: 1280
    height: 720
    
    Text{
        x: 500
        y: 120
        text: "Warnings"
        color: "#5f5fe1"
        font.pixelSize: 45
        horizontalAlignment: Text.AlignCenter
    }

    Text{
        x: 494
        y: 200
        text: "<b>Pas de défaut électrique sur les pompes</b>"
        color: "green"
        font.pixelSize: 20
        horizontalAlignment: Text.AlignCenter
        visible : !(Data.Values.displaydefautelec.includes("pompe 2")) * !(Data.Values.displaydefautelec.includes("pompe 1"))
    }


    Text{
        x: 175
        y: 250
        text: "<b>Défaut électrique sur la pompe 1 !</b>"
        color: "red"
        font.pixelSize: 20
        horizontalAlignment: Text.AlignCenter
        visible : (Data.Values.displaydefautelec.includes("pompe 1"))
        Button {
            x: 5
            y: 100
            visible : (Data.Values.displaydefautelec.includes("pompe 1"))
            width: 300
            height: 100
            text: "Remettre Pompe 1 en marche"
            font.pointSize: 15
            palette.button: "green"
            palette.buttonText: "white"
            font.pixelSize: 15
            onClicked:
            {
                _Modbusinfo.Write_modbus_boolean(54,0)
            }
        }
    }

    Text{
        x: 800
        y: 250
        text: "<b>Défaut électrique sur la pompe 2 !</b>"
        color: "red"
        font.pixelSize: 20
        horizontalAlignment: Text.AlignCenter
        visible : (Data.Values.displaydefautelec.includes("pompe 2"))
        Button {
            x: 5
            y: 100
            visible : (Data.Values.displaydefautelec.includes("pompe 2"))
            width: 300
            height: 100
            text: "Remettre Pompe 2 en marche"
            font.pointSize: 15
            palette.button: "green"
            palette.buttonText: "white"
            font.pixelSize: 15
            onClicked:
            {
                _Modbusinfo.Write_modbus_boolean(75,0)
            }
        }
    }

    
}
