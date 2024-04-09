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

# LEVEL 0
class AMF_EdgeCoupler_CBand():
    def __init__(self, name_="AMF_Si_EdgeCoupler_Cband_v3p0_SiEPIC", orientation_=0):
        self.name = name_
        self.inst = gf.Component(self.name)
        self.orientation = orientation_
        self.inst.add_ref(PDK.get_component(self.name)).rotate(self.orientation)
    def show(self):
        self.inst.show()

class AMF_MMI1x2_CBand():
    def __init__(self, name_="AMF_Si_1X2MMI_Cband_v3p0_SiEPIC", orientation_=0):
        self.name = name_
        self.inst = gf.Component(self.name)
        self.orientation = orientation_
        self.inst.add_ref(PDK.get_component(self.name)).rotate(self.orientation)
    def show(self):
        self.inst.show()

class AMF_PBRS_CBand():
    def __init__(self, name_="AMF_Si_PBRS_Cband_v3p0_SiEPIC", orientation_=0):
        self.name = name_
        self.inst = gf.Component(self.name)
        self.orientation = orientation_
        self.inst.add_ref(PDK.get_component(self.name)).rotate(self.orientation)
    def show(self):
        self.inst.show()

class Ring():
    def __init__(self, name_="R", radius_=10, width_=0.5, layer_="RIB_"):
        self.radius = radius_
        self.width = width_
        self.layer = layer_
        self.name = name_
        self.inst = gf.Component(name_)
        self.inst.add_ref(gf.components.ring(radius=radius_, width=width_, layer=layer_))

    def show(self):
        self.inst.show()

class Straight():
    def __init__(self, name_="S", length_=10, width_=0.5, layer_="RIB_"):
        self.length = length_
        self.width = width_
        self.layer = layer_
        self.name = name_
        self.inst = gf.Component(name_)
        self.inst.add_ref(gf.components.straight(length=self.length, width=self.width, layer=self.layer))
    def show(self):
        self.inst.show()

#LEVEL 1
class SecondOrderRing():
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
    def show(self):
        self.inst.show()



