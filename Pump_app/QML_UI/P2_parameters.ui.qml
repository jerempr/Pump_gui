// import libraries
import QtQuick 2.8
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.11
import "../backend/" as Data


// import "../imports/QtQuick/VirtualKeyboard" 2.1

// Gestion clavier:
// import QtQuick.VirtualKeyboard 2.15
// import "../imports/VirtualKeyboard" 2.15
// import "../imports/VirtualKeyboard/Settings"
// import "../imports/VirtualKeyboard/Styles"
// import QtQuick.VirtualKeyboard.Styles 2.15
// import QtQuick.VirtualKeyboard.Settings 2.15
 

 
/* The Item type is the base type for all visual items in Qt Quick. Here 1280 and 720 are chosen 
for the dimensions because the resolution of reTerminal LCD is 1280x720 */
Item {
    // identify the qml
    id: p2
    // define width and height of the app
    width: 1280
    height: 720

    
    // Rectangle{
    //     id: background
    //     width: 1280
    //     height: 720
    //     color: "grey"
    // }


    // Rectangle block for the heading
    
    // TODO
    Text{
        x: 494
        y: 100
        text: "Paramétrage"
        color: "#5f5fe1"
        font.pixelSize: 45
        horizontalAlignment: Text.AlignCenter
    }

    Rectangle{
        x: 595
        y: 180
        color: "blue"
        width: 10
        height: 500
    }

    Rectangle{
        x: 0
        y: 100
        width: 50
        height: 50
        color: "red"
        visible: txt_ihmsntb.inputMethodComposing
    }

    Text{
        x: 13
        y: 190
        text: "Seuil niveau très bas (m) :"
        color: "black"
        font.pixelSize: 20
        horizontalAlignment: Text.AlignCenter
        TextField{
            id: txt_ihmsntb
            x: 350
            y: -5
            text: Data.Values.displayIhmList[2] * !parent.inputMethodComposing
            font.pixelSize: 15
            onAccepted:{
                console.log("automtruc là",inputMethodComposing)
                _Modbusinfo.Write_modbus_float(101,txt_ihmsntb.text.replace(",","."))
                console.info("Written: ",txt_ihmsntb.text)
            }
        }
    }

    Text{
        x: 13
        y: 280
        text: "Seuil niveau bas (m) :"
        color: "black"
        font.pixelSize: 20
        horizontalAlignment: Text.AlignCenter
        TextField{
            id: txt_ihmsnb
            x: 350
            y: -5
            text: Data.Values.displayIhmList[0]
            font.pixelSize: 15
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _Modbusinfo.Write_modbus_float(97,txt_ihmsnb.text.replace(",","."))
                console.info("Written: ",txt_ihmsnb.text)
            }
        }
    }

    Text{
        x: 13
        y: 370
        text: "Seuil niveau haut (m) :"
        color: "black"
        font.pixelSize: 20
        horizontalAlignment: Text.AlignCenter
        TextField{
            id: txt_ihmsnh
            x: 350
            y: -5
            text: Data.Values.displayIhmList[1]
            font.pixelSize: 15
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _Modbusinfo.Write_modbus_float(99,txt_ihmsnh.text.replace(",","."))
                console.info("Written: ",txt_ihmsnh.text)
            }
        }
    }

    Text{
        x: 13
        y: 460
        text: "Seuil niveau très haut (m) :"
        color: "black"
        font.pixelSize: 20
        horizontalAlignment: Text.AlignCenter
        TextField{
            id: txt_ihmsnth
            x: 350
            y: -5
            text: Data.Values.displayIhmList[3]
            font.pixelSize: 15
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _Modbusinfo.Write_modbus_float(103,txt_ihmsnth.text.replace(",","."))
                console.info("Written: ",txt_ihmsnth.text)
            }
        }
    }

    Text{
        x: 13
        y: 550
        text: "Volume rempli/vidangé si niveau haut (m) :"
        color: "black"
        font.pixelSize: 15
        horizontalAlignment: Text.AlignCenter
        TextField{
            id: txt_ihmvrvnh
            x: 350
            y: -5
            text: Data.Values.displayIhmList[4]
            font.pixelSize: 15
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _Modbusinfo.Write_modbus_float(105,txt_ihmvrvnh.text.replace(",","."))
                console.info("Written: ",txt_ihmvrvnh.text)
            }
        }
    }

    Text{
        x: 13
        y: 640
        text: "Volume rempli/vidangé si niveau très haut (m) :"
        color: "black"
        font.pixelSize: 15
        horizontalAlignment: Text.AlignCenter
        TextField{
            id: txt_ihmvrvnth
            x: 350
            y: -5
            text: Data.Values.displayIhmList[5]
            font.pixelSize: 15
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _Modbusinfo.Write_modbus_float(107,txt_ihmvrvnth.text.replace(",","."))
                console.info("Written: ",txt_ihmvrvnth.text)
            }
        }
    }

    Text{
        x: 625
        y: 190
        text: "Temps de décalage entre les 2 pompes (h) :"
        color: "black"
        font.pixelSize: 20
        horizontalAlignment: Text.AlignCenter
        TextField{
            id: txt_ihmecart
            x: 400
            y: -5
            text: Data.Values.displayIhmList[6]
            font.pixelSize: 15
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _Modbusinfo.Write_modbus_float(109,txt_ihmecart.text.replace(",","."))
                console.info("Written: ",txt_ihmecart.text)
            }
        }
    }

    Text{
        x: 625
        y: 280
        text: "Offset de l'anneau de graisse (+/-) :"
        color: "black"
        font.pixelSize: 20
        horizontalAlignment: Text.AlignCenter
        TextField{
            x: 400
            y: -5
            text: Data.Values.displayIhmList[7]
            font.pixelSize: 15
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _Modbusinfo.Write_modbus_float(111,parent.text.replace(",","."))
                console.info("Written: ",parent.text)
            }
        }
    }


    Text{
        x: 625
        y: 360
        text: "Valeur Maxi Niveau :"
        color: "black"
        font.pixelSize: 20
        horizontalAlignment: Text.AlignCenter
        TextField{
            x: 400
            y: -5
            text: Data.Values.displayIhmList[9]
            font.pixelSize: 20
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _Modbusinfo.Write_modbus_float(91,parent.text.replace(",","."))
                console.info("Written: ",parent.text)
            }
        }
    }

    Text{
        x: 625
        y: 450
        text: "Valeur mini niveau :"
        color: "black"
        font.pixelSize: 20
        horizontalAlignment: Text.AlignCenter
        TextField{
            x: 400
            y: -5
            text: Data.Values.displayIhmList[8]
            font.pixelSize: 20
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            onEditingFinished:{
                _Modbusinfo.Write_modbus_float(89,parent.text.replace(",","."))
                console.info("Written: ",parent.text)
            }
        }
    }

    Text{
        x: 625
        y: 560
        text: "<b><u>Activation niveau de graisse :</b></u>"
        color: "black"
        font.pixelSize: 20
        horizontalAlignment: Text.AlignCenter
        Image {
            source: "../images/stop.png"
            visible: Data.Values.display_graisseOn
            x: 350
            y: -5
            width: 150
            height: 150
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    console.info("image graisse on clicked!")
                    _Modbusinfo.Write_modbus_boolean(113,0)
                }
            }
        }
        Image {
            source: "../images/start.png"
            visible: !Data.Values.display_graisseOn
            x: 350
            y: -5
            width: 100
            height: 100
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    console.info("image graisse on clicked!")
                    _Modbusinfo.Write_modbus_boolean(113,1)
                }
            }
        }
    }




    
    // InputPanel {
    //     id:inputPanel
    //     y: Qt.inputMethod.visible ? parent.height - inputPanel.height : parent.height
    //     anchors.left: parent.left
    //     anchors.right: parent.right
    // }




}
