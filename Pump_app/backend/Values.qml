pragma Singleton
import QtQuick 2.10
import QtQuick 2.8
// import "simulation.js" as JS

QtObject {
    id: networkvalues
    //Datetime
    property string displaydatetime: "00/00/00 00:00:00"

    //Ethernet Connect
    property string displayethernet: "N/A"

    //wifi connection
    property string displaywifi: "N/A"

    // defaut electrique à afficher dans le menu
    property string displaydefautelec: ""

    // Reterminal info objects:
    property bool display_popup: false


    //modbus value recived:
    property variant displayIhmList: ""
    property bool display_graisseOn: true

    property string displayvaleur_niveau_cuve: "5"

    property bool display_working_p1: false
    property bool display_working_p2: false

    Component.onCompleted: {
        console.log(_OPCUAinfo.Write_modbus_float())
        console.log(_Netinfo.SystemSignal)
        _Netinfo.SystemSignal.connect(netinfofunc)
        _Sysinfo.SystemSignal.connect(sysinfofunc)
        _Reterminalinfo.SystemSignal.connect(reterminalinfofunc)
        _OPCUAinfo.SystemSignal.connect(opcuainfofunc)
    }

    function reterminalinfofunc(popup) {
        console.log("\nreceived popup: ",popup);
        display_popup = popup
    }

    function sysinfofunc(str1){
        displaydatetime = String(str1)
    }

    function netinfofunc(str5,str6) {
        // console.log("\nVoila le date objet reçu: ",str7);
        displayethernet = String(str5)
        displaywifi = String(str6)
    }
    function opcuainfofunc(displayIhm,GraisseOn,valeur_niveau_cuve,defautelec,marchep1,marchep2) {
        if (displayIhm != displayIhmList){
            displayIhmList = displayIhm.split(',')
        }
        display_graisseOn = GraisseOn
        displayvaleur_niveau_cuve = valeur_niveau_cuve
        displaydefautelec = String(defautelec)
        display_working_p1 = marchep1
        display_working_p2 = marchep2
    }
}



