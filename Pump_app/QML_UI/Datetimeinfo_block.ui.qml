import QtQuick 2.8

Item {
    id: datetimeinfoblock
    width: 200
    height: 20
    property alias datetimeText: datetime.text
    
    
    Text {
        id: datetime
        x: 0
        y: 0
        width: 160
        height: 20
        color: "black"
        text: "N/A"
        font.pixelSize: 15
        horizontalAlignment: Text.AlignLeft
    }
}
