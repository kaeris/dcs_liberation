from dcs.vehicles import *
from dcs.ships import *
from dcs.planes import *
from dcs.helicopters import *

USA_2005 = {
    "country": "USA",
    "side": "blue",
    "units": [
        F_15C,
        F_14B,
        FA_18C_hornet,
        F_16C_50,

        A_10C,
        AV8BNA,

        B_1B,

        KC_135,
        S_3B_Tanker,
        C_130,
        E_3A,

        UH_1H,
        AH_64D,

        Armor.MBT_M1A2_Abrams,
        Armor.ATGM_M1134_Stryker,
        Armor.IFV_M2A2_Bradley,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,

        AirDefence.SAM_Hawk_PCP,
        AirDefence.SAM_Patriot_EPP_III,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ], "shorad":[
        AirDefence.SAM_Avenger_M1097,
    ]
}