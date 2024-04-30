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



amf_mmi_x = 55
amf_mmi_y = 20
amf_mmi_port_dy = 1.8/2
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

# Definition of TOP cell
top = gf.Component("TOP")

# Initialization of Edge coupler
EC_1 = top.add_ref(amf_edge_coupler)

# Building the Fanout
origin = [100, 0]
fanout = []
scaling_x = 2
scaling_y = 2
dy = amf_mmi_y*scaling_y
dx = amf_mmi_x*scaling_x
channels = 4
for i in range(int(np.log2(channels))):
    l = []
    for j in range(2**i):
        l.append(top.add_ref(amf_mmi).move((origin[0]+i*dx, origin[1] + j*dy - i*amf_mmi_port_dy)))
    fanout.append(l)

route = gf.routing.get_route(EC_1.ports["o1"], fanout[0][0].ports["o1"])
top.add(route.references)

dr = 2
for i in range(len(fanout)-1):
    rmin = 10
    for j in range(len(fanout[i])):
        route = gf.routing.get_route(fanout[i][j].ports["o3"], fanout[i+1][2*j].ports["o1"], radius = rmin)
        top.add(route.references)
        rmin = rmin + dr
        route = gf.routing.get_route(fanout[i][j].ports["o2"], fanout[i+1][2*j+1].ports["o1"], radius = rmin)
        top.add(route.references)
        rmin = rmin + dr

# PBRs array
origin[0] = origin[0] + 250
origin[1] = origin[1]
for i in range(channels):

    pbrs = top.add_ref(amf_pbrs).move((origin[0], i*origin[1]))
    pbrs = top.add_ref(amf_pbrs).move((origin[0], i*amf_pbrs_y * scaling_y + origin[1]))



top.show()

