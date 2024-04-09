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

def disp_layers():
    for i in PDK.layers:
        print(i, PDK.layers[i])

print("Using "+PDK.name+"'s PDK\n")
disp_layers()

#LEVEL 0
def build_ring(name, width, radius, layer):
    c = gf.Component(name)
    ring = gf.component.ring(radius, width, layer)
    c.add_ref(ring)
    return c

def build_straight(name, length, width, layer):
    c = gf.Component(name)
    straight = gf.components.straight(length, width=width, layer=layer)
    c.add_ref(straight)
    return c

#LEVEL 1

