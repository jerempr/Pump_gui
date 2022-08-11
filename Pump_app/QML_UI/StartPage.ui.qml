import QtQuick 2.8
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.11


Item {
    id: startpage
    width: 1280
    height: 100

    property int page: 1 


    Image {
        source: "../images/logo.png"
        anchors.centerIn: parent
        y: 
        width: 500
        height: 500
    }

    Text {
        anchors.centerIn: parent
        y: 600
        font.family: "Helvetica"
        font.pixelSize: 40
        color: "black"
        horizontalAlignment: Text.AlignHCenter
        text:  qsTr("Loading app...")
    }
        
    Timer {
        interval: 10000
        running: true
        onTriggered: {
            stackview.pop()
            stackview.push("P1.ui.qml",StackView.Immediate)
            }
    }
}
