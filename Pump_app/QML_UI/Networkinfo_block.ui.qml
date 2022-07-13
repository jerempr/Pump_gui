import QtQuick 2.8
import "../backend/" as Data 

Item {
    id: netinfoblock
    width: 200
    height: 120
    property alias n_aText: n_a.text
    property alias gadgetText: gadget.text
    
    property int taille_texte: 13


    // On affiche le wifi et ethernet


    Text {
        id: wi_fi_conection
        x: 0
        y: 0
        width: 160
        height: 15
        color: "#9D7878"
        text: "Wi-Fi :"
        font.pixelSize: taille_texte
        horizontalAlignment: Text.AlignLeft
        Text {
            id: n_a
            x: 0
            y: 20
            width: 160
            height: 15
            color: "#9D7878"
            text: "N/A"
            font.pixelSize: taille_texte
            horizontalAlignment: Text.AlignLeft
    }
    }

    Text {
        id: ethernet_connection
        x: 0
        y: 40
        width: 160
        height: 15
        color: "#9D7878"
        text: "Ethernet :"
        font.pixelSize: taille_texte
        horizontalAlignment: Text.AlignLeft
        Text {
            id: gadget
            x: 0
            y: 20
            width: 160
            height: 15
            color: "#9D7878"
            text: "N/A"
            font.pixelSize: taille_texte
            horizontalAlignment: Text.AlignLeft
    }
    }
}