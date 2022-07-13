// import libraries
import QtQuick 2.8
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.11
import "../backend/" as Data
 

 
/* The Item type is the base type for all visual items in Qt Quick. Here 1280 and 720 are chosen 
for the dimensions because the resolution of reTerminal LCD is 1280x720 */

Item {
    // identify the qml
    id: p4
    // define width and height of the app
    width: 1280
    height: 720
    
    Text{
        x: 500
        y: 120
        text: "Paramètres systèmes"
        color: "#5f5fe1"
        font.pixelSize: 45
        horizontalAlignment: Text.AlignCenter
    }

    Text{
        x: 494
        y: 200
        text: "TODO"
        color: "green"
        font.pixelSize: 65
        horizontalAlignment: Text.AlignCenter
    }
}
