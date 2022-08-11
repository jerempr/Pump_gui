import QtQuick 2.8
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.11
import "../backend/" as Data 

Item {
    id: menublock
    width: 1280
    height: 100

    property int page: 1 


    Rectangle {
        x: 333
        y: 0
        width: 600
        height: 44
        color: "#ebebeb"
        Text{
            anchors.fill: parent
            text: Data.Values.display_Defaut_Elec_Pompe_1 + Data.Values.display_Defaut_Elec_Pompe_2
            color: "red"
            font.pixelSize: 11
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Image {
        source: "../images/logo.png"
        x: 20
        y: 10
        width: 85
        height: 85
        MouseArea {
            anchors.fill: parent
            onClicked: {
                if (menublock.page != 4 ){
                    // stackview.pop()
                    stackview.push("P4_sysparams.ui.qml",StackView.Immediate)
                    menublock.page = 4
                    console.info("image OperaMetrix clicked!")
                    console.info("push to page 4")
                }
                else{
                    // stackview.pop()
                    stackview.push("P1.ui.qml",StackView.Immediate)
                    menublock.page = 1
                    console.info("image OperaMetrix clicked!")
                    console.info("push to page 1")
                }
            }
        }
    }

    Image {
        id: parameters_button
        source: "../images/parameters.png"
        x: 175
        y: 10
        width: 70
        height: 70
        MouseArea {
            anchors.fill: parent
            onClicked: {
                if (menublock.page != 2 ){
                    // stackview.pop()
                    stackview.push("P2_parameters.ui.qml",StackView.Immediate)
                    menublock.page = 2
                    console.info("image parameters clicked!")
                    console.info("push to page 2")
                }
                else{
                    // stackview.pop()
                    stackview.push("P1.ui.qml",StackView.Immediate)
                    menublock.page = 1
                    console.info("image parameters clicked!")
                    console.info("push to page 1")
                }
            }
        }
    }

    
    Image {
        source: "../images/warning.png"
        x: 270
        y: 40
        width: 45
        height: 45
        MouseArea {
            anchors.fill: parent
            onClicked: {
                if (menublock.page != 3 ){
                    // stackview.pop()
                    stackview.push("P3_warnings.ui.qml",StackView.Immediate)
                    menublock.page = 3
                    console.info("image warnings clicked!")
                    console.info("push to page 3")
                }
                else{
                    console.info("avant changement de page")
                    // stackview.pop()
                    stackview.push("P1.ui.qml",StackView.Immediate)
                    menublock.page = 1
                    console.info("image warnings clicked!")
                    console.info("push to page 1")
                }
            }
        }
    }

    // Text {
    //     x: 960
    //     y: 8
    //     width: 40
    //     height: 333
    //     text: "Print Datetime"
    // }

    Datetimeinfo_block {
        id: datetimeinfoblock
        x: 940
        y: 15
        datetimeText: Data.Values.displaydatetime
    }

    Networkinfo_block {
        id: netinfoblock
        x: 1120
        y: 15
        n_aText: Data.Values.displaywifi
        gadgetText: Data.Values.displayethernet
    }


}