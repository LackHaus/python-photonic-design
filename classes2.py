from collections.abc import Callable
from functools import partial
from amfpdk import *
from pydantic import BaseModel

import numpy as np
import gdsfactory as gf
from gdsfactory.add_pins import add_pin_rectangle_inside
from gdsfactory.component import Component
from gdsfactory.config import CONF
from gdsfactory.cross_section import cross_section
from gdsfactory.technology import (
    LayerLevel,
    LayerStack,
    LayerView,
    LayerViews,
    LayerMap,
)
from gdsfactory.typings import Layer
from gdsfactory.config import print_version_pdks, print_version_plugins
import random


top = gf.Component()
amf_mmi_x = 55
amf_mmi_y = 20
amf_pbrs_x = 413
amf_pbrs_y = 98.55
amf_edge_coupler_x = 370
amf_edge_coupler_y = 127
amf_pd_x = 190.9
amf_pd_y = 170

amf_mmi = PDK.get_component("AMF_Si_1X2MMI_Cband_v3p0")
amf_edge_coupler = PDK.get_component("AMF_Si_EdgeCoupler_Cband_v3p0").rotate(180)
amf_pbrs = PDK.get_component("AMF_Si_PBRS_Cband_v3p0")
rings = gf.components.ring_crow(gaps=[0.2, 0.2, 0.2], radius=[10, 10])
amf_pd = PDK.get_component("AMF_Ge_PD56G_Cband_v3p0")

top.add_ref(amf_pd)


top.show()

