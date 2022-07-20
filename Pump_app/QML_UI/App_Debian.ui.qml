// import library
import QtQuick 2.8
import QtQuick.Controls 2.1
// import QtQuick.Layouts 1.11
import "../backend/" as Data 
 
// properties of the application window containing UI elements
ApplicationWindow {
    id: application
    width: 1280 
    height: 720 
    visible: true
    visibility: "FullScreen"
 
    // initialize the first window of the application
    property var iniITEM: "P1.ui.qml"
 
    // stack-based navigation model
    StackView {
        id: stackview
        initialItem: iniITEM
        // Need to rotate the application to have it in landscape format:
    }
    

    Menu_block {
        x: 0
        y: 0
    }


    Shortcut {
        sequence: "Ctrl+A"
        onActivated: {
            console.log("Closing App")
            _Reterminalinfo.closeWindow()
        }
    }


    Popup {
        id: close_popup
        modal: true
        visible: Data.Values.display_popup + close_popup.visible
        // font.family: "Courier"
        x: 480
        y: 175
        width: 320
        height: 200
        closePolicy: Popup.CloseOnPressOutside | Popup.CloseOnEscape
        // onRejected:
        // {
        //     _Reterminalinfo.Close_popup()
        // }
        Rectangle {
            anchors.centerIn: parent
            width: 310
            height: 190
            color: "#5d5d5d"
            Button { 
                anchors.horizontalCenter: parent.horizontalCenter
                y: 30
                width: 180
                height: 40
                text: "<b>close application</b>"
                font.pixelSize: 15
                palette.buttonText: "white"
                palette.button: "red"
                onClicked:
                {
                    _Reterminalinfo.closeWindow()
                }
            }
            Button { 
                anchors.horizontalCenter: parent.horizontalCenter
                y: 120
                width: 180
                height: 40
                text: "<b>Reboot</b>"
                font.pixelSize: 15
                palette.buttonText: "black"
                palette.button: "White"
                onClicked:
                {
                    _Reterminalinfo.Reboot()
                }
            }
        }

        

    }


    // // close button
    // Button {
    //     id: close
    //     x: 1200
    //     y: 689
    //     width: 80
    //     height: 31
    //     palette.button: "red"
    //     palette.buttonText: "white"
    //     text: "X"
    //     font.pixelSize: 15
    //     onClicked:
    //     {
    //         close_popup.open()
    //     }
    // }
}
