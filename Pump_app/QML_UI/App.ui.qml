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

    Page{
        transform: Rotation {
            origin.x:360; origin.y: 360; angle: 90
        }
        anchors.fill: parent

        Shortcut {
            sequence: "Ctrl+A"
            onActivated: {
                console.log("Closing App")
                _Reterminalinfo.closeWindow()
            }
        }
 
        // stack-based navigation model
        StackView {
            id: stackview
            initialItem: iniITEM
            // Need to rotate the application to have it in landscape format:
            // transform: Rotation {origin.x:360; origin.y: 360; angle: 90}
        }
        

        Menu_block {
            x: 0
            y: 0
            // transform: Rotation {origin.x:360; origin.y: 360; angle: 90}
        }

        Popup {
            id: close_popup
            modal: true
            visible: Data.Values.display_popup + close_popup.visible
            x: 480
            y: 480
            width: 320
            height: 320
            closePolicy: Popup.CloseOnPressOutside | Popup.CloseOnEscape
            Item {
                id: container
                anchors.fill: parent
                rotation: 90
                transformOrigin: Item.Center
                Rectangle {
                    anchors.centerIn: parent
                    anchors.fill: parent
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
                        text: "<b>Restart Application</b>"
                        font.pixelSize: 15
                        palette.buttonText: "black"
                        palette.button: "White"
                        onClicked:
                        {
                            _Reterminalinfo.Restart_app()
                        }
                    }
                    Button { 
                        anchors.horizontalCenter: parent.horizontalCenter
                        y: 210
                        width: 180
                        height: 40
                        text: "<b>Reboot Device</b>"
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
        }
    }
}
