// import libraries
import QtQuick 2.8
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.11
import "../backend/" as Data

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
        y: 120
        text: "Paramétrage"
        color: "#5f5fe1"
        font.pixelSize: 45
        horizontalAlignment: Text.AlignCenter
    }

    Text{
        x: 13
        y: 190
        text: "Seuil niveau très bas (m) :"
        color: "black"
        font.pixelSize: 20
        horizontalAlignment: Text.AlignCenter
    }
    
    // InputPanel {
    //     id:inputPanel
    //     y: Qt.inputMethod.visible ? parent.height - inputPanel.height : parent.height
    //     anchors.left: parent.left
    //     anchors.right: parent.right
    // }


    TextField{
        id: txt_ihmsntb
        x: 366
        y: 176.2
        text: Data.Values.displayIhmSeuilNTB
        font.pixelSize: 15
        // activeFocusOnTab: true 
        // color: activeFocus ? "black" : "gray " 
        focus: true 
        // color: "black"
        onEditingFinished:{
            _Modbusinfo.Write_modbus_float(101,txt_ihmsntb.text)
            console.info("Written: ",txt_ihmsntb.text)
        }
    }

}
