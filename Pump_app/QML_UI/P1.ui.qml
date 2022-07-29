// import libraries
import QtQuick 2.8
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.11
 
/* The Item type is the base type for all visual items in Qt Quick. Here 1280 and 720 are chosen 
for the dimensions because the resolution of reTerminal LCD is 1280x720 */
Item {
    // identify the qml
    id: p1
    // define width and height of the app
    width: 1280
    height: 720


    // blocks for each informations
    P1_volumes {
        x: 20
        y: 150
    }

    P1_debits {
        x: 20
        y: 420
    }

    P1_pumps {
        x: 460
        y: 150
    }

    P1_demarrages {
        x: 860
        y: 150
    }

    P1_tmpfonctionnement {
        x: 860
        y: 420
    }
 

}
