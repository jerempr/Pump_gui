// import libraries
import QtQuick 2.8
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.11
import "../backend/" as Data
 
/* The Item type is the base type for all visual items in Qt Quick. Here 1280 and 720 are chosen 
for the dimensions because the resolution of reTerminal LCD is 1280x720 */
Item {
    // identify the qml
    id: p1pummp
    // define width and height of the app
    width: 350
    height: 550

    property int xpump: 460 
    property int ypump: 150

    // Rectangle block for the heading
    Rectangle {
        id: pumprectangle
        x: 0
        y: 0
        width: 350
        height: 550
        color: "#ebebeb"

            Rectangle{
                x: 492-xpump
                y: 168-ypump
                width: 285
                height: 500
                // color: "#d1d1d1"
                color: "#6bb3d7"

                Rectangle{
                    x: 0
                    y: 0
                    width: parent.width
                    height: 500 - Data.Values.displayvaleur_niveau_cuve*50
                    // color: "#6bb3d7"
                    color: "#d1d1d1"
                }

                Image {
                    source: "../images/pump.png"
                    x: 0
                    y: 555-ypump-parent.y
                    width: 130
                    height: 117
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            console.info("image pump a clicked!")
                            _Opcuainfo.Write_modbus_boolean(54,1)
                        }
                    }
                    Text {
                        x: 50
                        y: 120
                        text: "Pompe 1"
                        font.pixelSize: 15
                    }
                    Image {
                        source: "../images/lightning.png"
                        x: 0
                        y: 0
                        width: 50
                        height: 60
                        visible: (Data.Values.displaydefautelec.includes("pompe 1"))
                    }
                    Image {
                        source: "../images/orange_light_bulb.png"
                        x: 10
                        y: 65
                        width: 34
                        height: 44
                        visible: (Data.Values.display_working_p1)
                    }
                }
                Image {
                    source: "../images/pump.png"
                    x: 645-xpump-parent.x
                    y: 555-ypump-parent.y
                    width: 130
                    height: 117
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            console.info("image pump b  clicked!")
                            _Opcuainfo.Write_modbus_boolean(75,1)
                        }
                    }
                    Text {
                        x: 50
                        y: 120
                        text: "Pompe 2"
                        font.pixelSize: 15
                    }
                    Image {
                        source: "../images/lightning.png"
                        x: 0
                        y: 0
                        width: 50
                        height: 60
                        visible: (Data.Values.displaydefautelec.includes("pompe 2"))
                    }
                    Image {
                        source: "../images/orange_light_bulb.png"
                        x: 10
                        y: 65
                        width: 34
                        height: 44
                        visible: (Data.Values.display_working_p2)
                    }
                    
                }
        }
    }

}
