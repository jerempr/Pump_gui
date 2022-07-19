pragma Singleton
import QtQuick 2.10
import QtQuick 2.8
// import "simulation.js" as JS

QtObject {
    id: networkvalues
    //Datetime
    property string displaydatetime: "00/00/00 00:00:00"

    //Ethernet Connect
    property string displayethernet: "0"

    //wifi connection
    property string displaywifi: "0"

    // defaut electrique à afficher dans le menu
    property string displaydefautelec: ""

    //modbus value recived:
    property string displayIhmSeuilNTB: "0"

    property int displayvaleur_niveau_cuve: 5

    property bool display_working_p1: false
    property bool display_working_p2: false

    Component.onCompleted: {
        _Netinfo.SystemSignal.connect(netinfofunc)
        _Modbusinfo.SystemSignal.connect(modbusinfofunc)
        _Sysinfo.SystemSignal.connect(sysinfofunc)
    }

    function sysinfofunc(str1){
        displaydatetime = String(str1)
    }

    function netinfofunc(str5,str6) {
        // console.log("\nVoila le date objet reçu: ",str7);
        displayethernet = String(str5)
        displaywifi = String(str6)
    }
    function modbusinfofunc(IhmSeuilNTB,valeur_niveau_cuve,defautelec,marchep1,marchep2) {
        // console.log("ça marche 3");
        // console.log("Voila le modbus objet reçu: ",String(strobj));
        displayIhmSeuilNTB = String(IhmSeuilNTB)
        displayvaleur_niveau_cuve = valeur_niveau_cuve
        displaydefautelec = String(defautelec)
        display_working_p1 = marchep1
        display_working_p2 = marchep2
    }
}



