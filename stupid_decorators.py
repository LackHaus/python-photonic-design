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

@gf.cell
def SecondOrderRing(r=10, g0=0.2, g1=0.1, l=(10,0), w=0.5):
    c = gf.Component()
    ring1 = c.add_ref(gf.components.ring(r, layer=l, width=w))
    ring2 = c.add_ref(gf.components.ring(r, layer=l, width=w)).movey(2*r+w+g1)
    straight1 = c.add_ref(gf.components.straight(2*r+w)).move((-r,-r-w-g0))
    straight2 = c.add_ref(gf.components.straight(2*r+w)).move((-r,3*r+g1+2*w+g0))
    c.add_port("bl", port=straight1.ports["o1"])
    c.add_port("br", port=straight1.ports["o2"])
    c.add_port("tl", port=straight2.ports["o1"])
    c.add_port("tr", port=straight2.ports["o2"])
    return c

@gf.cell
def FanOut(ch=32, dx=200, dy=100, port_misalignment=0.9, rmin=10, dr=1, w=0.5):
    mem = 0
    c = gf.Component()
    fanout_cells = []
    for i in range(int(np.log2(ch))):
        l  = []
        for j in range(2**i):
            l.append(c.add_ref(PDK.get_component("AMF_Si_1X2MMI_Cband_v3p0_SiEPIC")).move((i*dx, j*dy-port_misalignment*i)))
        fanout_cells.append(l)
    port_names = ["o3", "o2"]
    for i in range(len(fanout_cells)):
        for j in range(int(len(fanout_cells[i])/2)): 
                route = gf.routing.get_route(fanout_cells[i-1][j].ports["o3"], fanout_cells[i][2*j].ports["o1"], with_sbend=True, radius=rmin+2*j*2*dr)
                c.add(route.references)
                route = gf.routing.get_route(fanout_cells[i-1][j].ports["o2"], fanout_cells[i][2*j+1].ports["o1"], with_sbend=True, radius=rmin+2*j*2*dr + dr + w)
                c.add(route.references)
    c.add_port("in", port=fanout_cells[0][0].ports["o1"])
    for j in range(int(len(fanout_cells[-1])/2)):
        c.add_port("ch"+str(2*j), port=fanout_cells[-1][j].ports["o3"])
        c.add_port("ch"+str(2*j+1), port=fanout_cells[-1][j].ports["o2"])
    return c

@gf.cell
def PBRS_Pairs(ch=32, dy=300, sep=150):
    c = gf.Component()
    pbrs_cells = []
    for i in range(ch):
        pbrs_cells.append(c.add_ref(PDK.get_component("AMF_Si_PBRS_Cband_v3p0")).movey(i*dy))
    for cc,v in enumerate(pbrs_cells):
        c.add_port("in"+str(cc), port=v.ports["o1"])
        c.add_port("bot"+str(cc), port=v.ports["o3"])
        c.add_port("top"+str(cc), port=v.ports["o2"])
    return c

"""
c = gf.Component()
a = gf.Component()
rect_top = a.add_ref(gf.components.rectangle(size=(r,r), layer=(-1,0)))
rect_bot = a.add_ref(gf.components.rectangle(size=(r,r), layer=(-1,0))).move((-2, -5))
rect_cut = gf.geometry.boolean(A=rect_top, B=rect_bot, operation="A-B", layer=l)
c.add_ref(rect_cut)
return c
"""

@gf.cell
def RingHeater(r=10, l=(115,0), w=1, ring_opening=5, pad_size=(2, 5), multi_stage = True):
    c = gf.Component()
    a = gf.Component()
    big_ring = a.add_ref(gf.components.ring(r, layer=(1,0), width=w))
    rect = a.add_ref(gf.components.rectangle(size=(ring_opening, r), layer=(2,0))).move((-ring_opening/2, -r-ring_opening))
    rect_cut = gf.geometry.boolean(A=big_ring, B=rect, operation="A-B", layer=l)
    pad_left = c.add_ref(gf.components.rectangle(size=pad_size, layer=l)).move((-ring_opening/2, -pad_size[1] - np.sqrt((r-w/2)**2 - (ring_opening/2)**2)))
    pad_right = c.add_ref(gf.components.rectangle(size=pad_size, layer=l)).move((ring_opening/2 - pad_size[0], -pad_size[1] - np.sqrt((r-w/2)**2 - (ring_opening/2)**2)))
    c.add_ref(rect_cut)

    if multi_stage:
        
    return c

RingHeater().show()

#-pad_size[1]-np.sqrt((r-w)**2  - (ring_opening/2)**2
