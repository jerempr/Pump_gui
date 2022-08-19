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

    property bool inputting: true

    
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
            text: Data.Values.display_Ihm_Seuil_Niveau_Tres_Bas
            font.pixelSize: 15
            onAccepted:{
                _OPCclient.Write_node("Ihm_Seuil_Niveau_Tres_Bas",txt_ihmsntb.text.replace(",","."))
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
            text: Data.Values.display_Ihm_Seuil_Niveau_Bas
            font.pixelSize: 15
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _OPCclient.Write_node("Ihm_Seuil_Niveau_Bas",txt_ihmsnb.text.replace(",","."))
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
            text: Data.Values.display_Ihm_Seuil_Niveau_Haut
            font.pixelSize: 15
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _OPCclient.Write_node("Ihm_Seuil_Niveau_Haut",txt_ihmsnh.text.replace(",","."))
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
            text: Data.Values.display_Ihm_Seuil_Niveau_Tres_Haut
            font.pixelSize: 15
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _OPCclient.Write_node("Ihm_Seuil_Niveau_Tres_Haut",txt_ihmsnth.text.replace(",","."))
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
            text: Data.Values.display_Ihm_Volume_Niveau_Haut
            font.pixelSize: 15
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _OPCclient.Write_node("Ihm_Volume_Niveau_Haut",txt_ihmvrvnh.text.replace(",","."))
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
            text: Data.Values.display_Ihm_Volume_Niveau_Tres_Haut
            font.pixelSize: 15
            focus: true 
            onEditingFinished:{
                _OPCclient.Write_node("Ihm_Volume_Niveau_Tres_Haut",txt_ihmvrvnth.text.replace(",","."))
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
            text: Data.Values.display_Temps_De_Décalage
            font.pixelSize: 15
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _OPCclient.Write_node("Temps_De_Décalage",txt_ihmecart.text.replace(",","."))
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
            text: Data.Values.display_Offset_Anneau_Graisse
            font.pixelSize: 15
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _OPCclient.Write_node("Offset_Anneau_Graisse",parent.text.replace(",","."))
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
            text: Data.Values.display_Valeur_Maxi_Niveau
            font.pixelSize: 20
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            // color: "black"
            onEditingFinished:{
                _OPCclient.Write_node("Valeur_Maxi_Niveau",parent.text.replace(",","."))
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
            text: Data.Values.display_Valeur_Mini_Niveau
            font.pixelSize: 20
            // activeFocusOnTab: true 
            // color: activeFocus ? "black" : "gray " 
            focus: true 
            onEditingFinished:{
                _OPCclient.Write_node("Valeur_Mini_Niveau",parent.text.replace(",","."))
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
            visible: Data.Values.display_Anneau_Graisse_ON
            x: 350
            y: -5
            width: 150
            height: 150
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    console.info("image graisse on clicked!")
                    _OPCclient.Write_node("Anneau_Graisse_ON",0)
                }
            }
        }
        Image {
            source: "../images/start.png"
            visible: !Data.Values.display_Anneau_Graisse_ON
            x: 350
            y: -5
            width: 100
            height: 100
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    console.info("image graisse on clicked!")
                    _OPCclient.Write_node("Anneau_Graisse_ON",1)
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
