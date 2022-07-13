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
        transform: Rotation {origin.x:360; origin.y: 360; angle: 90}
    }
    

    Menu_block {
        x: 0
        y: 0
        transform: Rotation {origin.x:360; origin.y: 360; angle: 90}
    }

    // close button
    // Button {
    //     id: close
    //     x: 1200
    //     y: 0
    //     width: 80
    //     height: 31
    //     palette.button: "red"
    //     palette.buttonText: "white"
    //     text: "X"
    //     font.pixelSize: 15
    //     transform: Rotation {origin.x:360-1200; origin.y: 360; angle: 90}
    //     onClicked:
    //     {
    //         _Setting.closeWindow()
    //     }
    // }
}
