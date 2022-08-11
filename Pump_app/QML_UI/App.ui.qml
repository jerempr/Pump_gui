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
    property int loadedpage: 0

    Page{
        id: mymainpage
        transform: Rotation {
            origin.x:360; origin.y: 360; angle: 90
        }
        anchors.fill: parent

        Shortcut {
            sequence: "Ctrl+T"
            onActivated: {
                console.log("truc")
                console.log(stackview.get(1))
            }
        }

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
            id: connextion_popup
            modal: true
            visible: !Data.Values.display_connected && !loading_popup.visible
            x: 480
            y: 480
            width: 320
            height: 320
            closePolicy: Popup.CloseOnEscape
             Item {
                id: connexion_popup_container
                anchors.fill: parent
                rotation: 90
                transformOrigin: Item.Center
                Rectangle {
                    anchors.centerIn: parent
                    anchors.fill: parent
                    color: "red"
                    Text {
                        anchors.fill:parent
                        id: myText
                        font.family: "Helvetica"
                        font.pixelSize: 20
                        color: "white"
                        text:  qsTr(" \n No connexion to the server... \n Retrying in 10s...")
                        horizontalAlignment: Text.AlignHCenter
                    }
                    AnimatedImage { 
                        id: loadinganimation
                        source: "../images/loading.gif" 
                        y: 100
                        x: 100
                    }
                }
            }
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
    Popup {
        id: loading_popup
        // modal: true
        closePolicy: Popup.CloseOnEscape
        Item {
            x: 0
            y: 0
            width: 1280 
            height: 720 
            // anchors.fill: parent
            id: loading_popup_container
            transform: Rotation {
                origin.x:360; origin.y: 360; angle: 90
            }
            // transformOrigin: Item.Center
            Rectangle {
                anchors.centerIn: parent
                anchors.fill: parent
                color: "white"
                Image {
                    source: "../images/logo.png"
                    anchors.centerIn: parent
                    width: 500
                    height: 500
                }
                Text {
                    // anchors.centerIn: parent
                    x: 0
                    y: 600
                    width: parent.width
                    height: 50 
                    font.family: "Helvetica"
                    font.pixelSize: 40
                    color: "black"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    text:  qsTr("Loading app")+Data.Values.displayloading
                }
                Timer {
                    interval: 10000
                    running: true
                    triggeredOnStart: true
                    onTriggered: {
                        console.log("triggered timer")
                        pagesloadingtimer.running = !pagesloadingtimer.running
                        loading_popup.visible = !loading_popup.visible
                        }
                }
                // We will use another timer to load all the pages that we will need after
                Timer {
                    id: pagesloadingtimer
                    interval: 1500
                    running: false
                    repeat: true
                    onTriggered: {
                        // console.log("triggered second timer!")
                        switch (loadedpage){
                            case 0:
                                stackview.push("P2_parameters.ui.qml",StackView.Immediate)
                                break;
                            case 1:
                                stackview.push("P3_warnings.ui.qml",StackView.Immediate)
                                break;
                            case 3:
                                stackview.push("P4_sysparams.ui.qml",StackView.Immediate)
                                break;
                            case 4:
                                stackview.push(iniITEM,StackView.Immediate)
                                break;
                        }
                        loadedpage = loadedpage + 1
                    }
                }
            }
        }
    }
}
