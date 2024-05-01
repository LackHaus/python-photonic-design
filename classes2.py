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
amf_pbrs_port_dy = 1.8
amf_pbrc_x = 413
amf_pbrc_y = 98.55
amf_pbrc_port_dy = 1.8
amf_edge_coupler_x = 370
amf_edge_coupler_y = 127
amf_pd_x = 190.9
amf_pd_y = 170

amf_mmi = PDK.get_component("AMF_Si_1X2MMI_Cband_v3p0")
amf_edge_coupler = PDK.get_component("AMF_Si_EdgeCoupler_Cband_v3p0").rotate(180)
amf_pbrs = PDK.get_component("AMF_Si_PBRS_Cband_v3p0")
amf_pbrc = PDK.get_component("AMF_Si_PBRC_Cband_v3p0")
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

# PBRS array
origin[0] = origin[0] + 250
origin[1] = origin[1]
pbrs = []
scaling_y = 1.1
bend = 10
for i in range(channels):
    pbrs.append(top.add_ref(amf_pbrs).move((origin[0], i*amf_pbrs_y * scaling_y + origin[1] - amf_pbrs_port_dy)))
for c,v in enumerate(fanout[-1]):
    bend = bend + 2*2*c
    route = gf.routing.get_route(v.ports["o3"], pbrs[2*c].ports["o1"], radius=bend)
    top.add(route.references)
    bend = bend + 2*(2*c+1)
    route = gf.routing.get_route(v.ports["o2"], pbrs[2*c+1].ports["o1"], radius=bend)
    top.add(route.references)


#Ring stage 1
origin[0] = origin[0] + 600
origin[1] = origin[1]
rings_1 = []
rings_2 = []
radii1 = [[10, 10], [9, 9], [8, 8], [7, 7]]
radii2 = [[9.5, 9.5], [8.5, 8.5], [7.5, 7.5], [6.5, 6.5]]
gaps1 = [[0.2, 0.2, 0.2], [0.3, 0.3, 0.3], [0.4, 0.4, 0.4], [0.5, 0.5, 0.5]] 
gaps2 = [[0.25, 0.25, 0.25], [0.35, 0.35, 0.35], [0.45, 0.45, 0.45], [0.5, 0.5, 0.5]] 
dy = 150
dx = 200
ring_y_port = 1.8
for i in range(channels):
    rings1 = gf.components.ring_crow(gaps=gaps1[i], radius=radii1[i])
    rings2 = gf.components.ring_crow(gaps=gaps2[i], radius=radii2[i]) 
    r1 = []
    r2 = []
    for j in range(2):
        r1.append(top.add_ref(rings1).move((origin[0], origin[1] + i*dy + (j)*dy/2 - ring_y_port)))
        r2.append(top.add_ref(rings2).move((origin[0]+dx, origin[1] + i*dy + (j)*dy/2)))

    rings_1.append(r1)
    rings_2.append(r2)

bend = 10
for i in range(len(pbrs)):
    route = gf.routing.get_route(pbrs[i].ports["o3"], rings_1[i][0].ports["o1"], radius=bend)
    top.add(route.references)
    bend = bend + 5
    route = gf.routing.get_route(pbrs[i].ports["o2"], rings_1[i][1].ports["o1"], radius=bend)
    top.add(route.references)
    bend = bend + 5

for i in range(len(rings_1)):
    route = gf.routing.get_route(rings_1[i][0].ports["o4"], rings_2[i][0].ports["o3"], radius=10)
    top.add(route.references)
    route = gf.routing.get_route(rings_1[i][1].ports["o4"], rings_2[i][1].ports["o3"], radius=10)
    top.add(route.references)


# PBRC array
origin[0] = origin[0] + 350
origin[1] = origin[1]
pbrc = []
scaling_y = 1.1
bend = 10
for i in range(channels):
    pbrc.append(top.add_ref(amf_pbrc).move((origin[0], i*amf_pbrc_y * scaling_y + origin[1] - amf_pbrc_port_dy)))
bend = 10 + 2*2*channels
for i in range(len(pbrc)):
    route = gf.routing.get_route(rings_2[i][0].ports["o2"], pbrc[i].ports["o1"], radius = bend)
    top.add(route.references)
    bend = bend-2
    route = gf.routing.get_route(rings_2[i][1].ports["o2"], pbrc[i].ports["o2"], radius = bend)
    top.add(route.references)
    bend = bend-2
top.show()

# PD array 
origin[0] = origin[0] + 350
origin[1] = origin[1]
pds = []
scaling_y = 1.1
bend = 10


