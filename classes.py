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

"""Defining a generic cell class for show() or other methods shared by all the cells
Hopefully it won't mess anything up later..."""
class Cell():
    def __init__(self):
        self.inst = 0

    def show(self):
        self.inst.show()

"""---------------------------------------------
LEVEL 0 : Represent all the fundamental cells, 
each subsequent level refers to the previous
---------------------------------------------"""

"""AMF blackboxes don't work well when transformed in classes,
 too many references and dependencies"""

amf_edgecoupler_cband = PDK.get_component("amf_Edge_Coupler_1550").rotate(180)
amf_1x2mmi_cband = PDK.get_component("AMF_Si_1X2MMI_Cband_v3p0_SiEPIC")
amf_pbrs_cband = PDK.get_component("AMF_Si_PBRS_Cband_v3p0_SiEPIC")


"""Definition of the Ring Resonator cell"""
class Ring(Cell):
    def __init__(self, name_="R", radius_=10, width_=0.5, layer_="RIB_"):
        self.radius = radius_
        self.width = width_
        self.layer = layer_
        self.name = name_
        self.inst = gf.Component(name_)
        self.inst.add_ref(gf.components.ring(radius=radius_, width=width_, layer=layer_))

"""Definition of the Straight Wavguide cell"""
class Straight(Cell):
    def __init__(self, name_="S", length_=10, width_=0.5, layer_="RIB_"):
        self.length = length_
        self.width = width_
        self.layer = layer_
        self.name = name_
        self.inst = gf.Component(name_)
        self.inst.add_ref(gf.components.straight(length=self.length, width=self.width, layer=self.layer))

"""Definition of the Taper or terminator cell"""
class Taper(Cell):
    def __init__(self, n="Taper", w1=0.5, w2=0.005, l=5, layer_ = "RIB_"):
        self.name = n
        self.width1 = w1
        self.width2 = w2
        self.lenght = l
        self.layer = layer_
        self.inst = gf.Component(self.name)
        self.inst.add_ref(gf.components.taper(self.lenght, self.width1, self.width2, layer="RIB_"))

"""---------------------------------------------
LEVEL 1
---------------------------------------------"""

"""Definition of the SecondOrderRing cell composed of 2 rings"""
class SecondOrderRing(Cell):
    def __init__(self, name_="SOR", rings_=[Ring(radius_=7), Ring(radius_=7.5)], gaps_=[0.2, 0.1, 0.2], width_=0.5, layer_="RIB_"):
        self.inst = gf.Component(name_)
        self.rings = rings_
        self.gaps = gaps_
        self.width = width_
        self.layer = layer_
        self.order = len(self.rings)
        max_r = np.max([self.rings[0].radius,self.rings[1].radius])
        wg = Straight(length_=self.width+2*max_r, width_=self.width, layer_=self.layer)
        if (len(self.rings) + 1 != len(self.gaps)) or (self.order != len(self.rings)):
            raise Exception("Error in the number of rings, gaps or order mentioned")
        self.inst.add_ref(wg.inst)
        d = np.array([max_r + self.width/2, self.rings[0].radius + self.width + self.gaps[0]])
        self.inst.add_ref(self.rings[0].inst).move((d[0], d[1]))
        d[1] = d[1] + self.rings[0].radius + self.width + self.rings[1].radius + self.gaps[1]
        self.inst.add_ref(self.rings[1].inst).move((d[0], d[1]))
        self.inst.add_ref(wg.inst).movey(d[1] + self.rings[1].radius + self.gaps[2] + self.width)

class MMI1x2Stage(Cell):
    def __init__(self, stage_=2, dy_=50, mmi_=amf_1x2mmi_cband):
        self.stage = stage_
        self.mmi = mmi_
        self.name = "MMI_1x2_stage"+str(self.stage)
        self.dy = dy_
        self.inst = gf.Component(self.name)
        for i in range(int(2**(self.stage - 1))):
            self.inst.add_ref(self.mmi).movey(i*self.dy)


MMI1x2Stage(4).show()
