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

    //modbus value recived:
    property string displayIhmSeuilNTB: "N/A"
    property string displayIhmSeuilNB: "N/A"
    property string displayIhmSeuilNH: "N/A"
    property string displayIhmSeuilNTH: "N/A"
    property string displayIhmVolumeRVNH: "N/A"
    property string displayIhmVolumeRVNTH: "N/A"
    property string displayIhmDecalage: "N/A"
    property string displayIhmOffsetgraisse: "N/A"

    property string displayIhm: ""
    property variant displayIhmList: ""

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
    function modbusinfofunc(displayIhm,valeur_niveau_cuve,defautelec,marchep1,marchep2) {
        // console.log("ça marche 3");

        // Receive list Ihm and split it to get all the values and then attribute it to the variables:
        displayIhmList = displayIhm.split(',')
        console.log("Voila le modbus objet reçu: ",displayIhmList);
        
        displayIhmSeuilNB = displayIhmList[0]
        displayIhmSeuilNH = displayIhmList[1]
        displayIhmSeuilNTB = displayIhmList[2]
        displayIhmSeuilNTH = displayIhmList[3]
        displayIhmVolumeRVNH = displayIhmList[4]
        displayIhmVolumeRVNTH = displayIhmList[5]
        displayIhmDecalage = displayIhmList[6]
        displayIhmOffsetgraisse = displayIhmList[7]



        displayvaleur_niveau_cuve = valeur_niveau_cuve
        displaydefautelec = String(defautelec)
        display_working_p1 = marchep1
        display_working_p2 = marchep2
    }
}



