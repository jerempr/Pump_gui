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

    property string display_Ihm_Seuil_Niveau_Bas : "N/A"

    property string display_Ihm_Seuil_Niveau_Haut : "N/A"

    property string display_Ihm_Seuil_Niveau_Tres_Bas : "N/A"

    property string display_Ihm_Seuil_Niveau_Tres_Haut : "N/A"

    property string display_Ihm_Volume_Niveau_Haut : "N/A"

    property string display_Ihm_Volume_Niveau_Tres_Haut : "N/A"

    property string display_Temps_De_Décalage : "N/A"

    property string display_Offset_Anneau_Graisse : "N/A"

    property bool display_Anneau_Graisse_ON : true

    property string display_Valeur_Mini_Niveau : "N/A"

    property string display_Valeur_Maxi_Niveau : "N/A"


    Component.onCompleted: {
        _Netinfo.SystemSignal.connect(netinfofunc)
        _Opcuainfo.SystemSignal.connect(opcuainfofunc)
        // _Modbusinfo.Ihm_parametersSignal(modbusinfoparamsfunc)
        _Sysinfo.SystemSignal.connect(sysinfofunc)
        _Reterminalinfo.SystemSignal.connect(reterminalinfofunc)
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
    // function opcuainfofunc(displayIhm,GraisseOn,valeur_niveau_cuve,defautelec,marchep1,marchep2) {
    //     // console.log("ça marche 3");
    //     // Receive list Ihm and split it to get all the values and then attribute it to the variables:
    //     if (displayIhm != displayIhmList){
    //         displayIhmList = displayIhm.split(',')
    //     }
        
            
    //     display_graisseOn = GraisseOn
    //     displayvaleur_niveau_cuve = valeur_niveau_cuve
    //     displaydefautelec = String(defautelec)
    //     display_working_p1 = marchep1
    //     display_working_p2 = marchep2
    // }

    function opcuainfofunc(id,val) {
        // Receive list Ihm and split it to get all the values and then attribute it to the variables:
        switch (id){
            case "Ihm_Seuil_Niveau_Bas":
                display_Ihm_Seuil_Niveau_Bas = val
                break;
            case "Ihm_Seuil_Niveau_Haut":
                display_Ihm_Seuil_Niveau_Haut = val
                break;
            case "Ihm_Seuil_Niveau_Tres_Bas":
                display_Ihm_Seuil_Niveau_Tres_Bas = val
                break;
            case "Ihm_Seuil_Niveau_Tres_Haut":
                display_Ihm_Seuil_Niveau_Tres_Haut = val
                break;
            case "Ihm_Volume_Niveau_Haut":
                display_Ihm_Volume_Niveau_Haut = val
                break;
            case "Ihm_Volume_Niveau_Tres_Haut":
                display_Ihm_Volume_Niveau_Tres_Haut = val
                break;
            case "Temps_De_Décalage":
                display_Temps_De_Décalage = val
                break;
            case "Offset_Anneau_Graisse":
                display_Offset_Anneau_Graisse = val
                break;
            case "Anneau_Graisse_ON":
                display_Anneau_Graisse_ON = val
                break;
            case "Valeur_Mini_Niveau":
                display_Valeur_Mini_Niveau = val
                break;
            case "Valeur_Maxi_Niveau":
                display_Valeur_Maxi_Niveau = val
                break;
            // default:
            //     console.log("id not found in your switchcase: ", id);
            //     break;
            
        }
    }

}



