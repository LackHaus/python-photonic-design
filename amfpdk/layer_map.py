from gdsfactory.technology.layer_map import LayerMap, LayerViews
from gdsfactory.typings import Layer

from amfpdk.config import PATH


class AMFLayerMap(LayerMap):  # type: ignore
    """Layer map based on AMF PDK"""

    WAFER: Layer = (99999, 0)

    BB_EP_: Layer = (1020, 0)
    BB_LABEL_: Layer = (1002, 0)
    BB_MT1_: Layer = (1021, 0)
    BB_MT2_: Layer = (1022, 0)
    BB_OP_SIN_: Layer = (1011, 0)
    BB_OP_SI_: Layer = (1010, 0)
    BLACKBOX_: Layer = (1001, 0)

    DRCexclude_: Layer = (1004, 0)
    FP_: Layer = (82, 0)

    OX_OPEN_: Layer = (151, 0)
    DTR_: Layer = (160, 0)

    PinRec: Layer = (997, 0)
    PinRecM: Layer = (999, 10)
    DevRec: Layer = (998, 0)
    Errors: Layer = (999, 0)
    FbrTgt: Layer = (951, 0)
    LABEL_: Layer = (80, 0)
    Lumerical: Layer = (733, 0)

    GeEP_: Layer = (40, 0)
    VIA1_: Layer = (100, 0)
    MT1_: Layer = (105, 0)
    VIA2_: Layer = (120, 0)
    MT2_: Layer = (125, 0)
    HTR_: Layer = (115, 0)
    PAD_: Layer = (150, 0)

    RIB_: Layer = (10, 0)
    GRAT_: Layer = (11, 0)
    SLAB_: Layer = (12, 0)

    PCONT_: Layer = (21, 0)
    NCONT_: Layer = (22, 0)
    PIM_: Layer = (23, 0)
    NIM_: Layer = (24, 0)
    IPD_: Layer = (25, 0)
    IND_: Layer = (26, 0)
    NPPGE_: Layer = (41, 0)
    PPPGE_: Layer = (42, 0)
    PP_PD_: Layer = (20, 0)

    WG_SiN_: Layer = (50, 0)
    SiNwin_: Layer = (53, 0)
    SiNwg1_: Layer = (54, 0)

    MT1_KO_: Layer = (80, 0)
    Si_KO_: Layer = (90, 0)
    Si_Tiles_: Layer = (190, 0)
    MT1_Tiles_: Layer = (191, 0)

    TM1_: Layer = (105, 4)
    TN_: Layer = (50, 4)
    TR_: Layer = (10, 4)
    Text: Layer = (1003, 0)
    Waveguide: Layer = (10, 1)


LAYER = AMFLayerMap()
LAYER_VIEWS = LayerViews(PATH.layer_yaml)
