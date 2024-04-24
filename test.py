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

from classes import *

top = gf.Component("TOP")
mmi1 = AMF_1x2MMI_CBand()
mmi2 = AMF_1x2MMI_CBand()


mmi1_r = top.add_ref(mmi1.inst)
mmi2_r = top.add_ref(mmi2.inst).movex(120)

route = gf.routing.get_route(mmi1_r.ports["o2"], mmi2_r.ports["o1"])

top.add(route.references)

top.show()
