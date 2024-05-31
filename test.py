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

TOP = gf.Component("TOP")


three_straights = gf.Component("TS")

straight1 = three_straights.add_ref(gf.components.straight())
straight2 = three_straights.add_ref(gf.components.straight()).move((50,10))
straight3 = three_straights.add_ref(gf.components.straight()).move((100,-10))
three_straights.cells=[straight1, straight2, straight3]

route1 = gf.routing.get_route(straight1.ports["o2"], straight2.ports["o1"], with_sbend=True)
route2 = gf.routing.get_route(straight2.ports["o2"], straight3.ports["o1"], with_sbend=True)

three_straights.add(route1.references)
three_straights.add(route2.references)



three_straights2 = gf.Component("TS2")

straight4 = three_straights.add_ref(gf.components.straight())
straight5 = three_straights.add_ref(gf.components.straight()).move((50,10))
straight6 = three_straights.add_ref(gf.components.straight()).move((100,-10))
three_straights2.cells=[straight4, straight5, straight6]

route1 = gf.routing.get_route(straight4.ports["o2"], straight5.ports["o1"], with_sbend=True)
route2 = gf.routing.get_route(straight5.ports["o2"], straight6.ports["o1"], with_sbend=True)

three_straights2.add(route1.references)
three_straights2.add(route2.references)

TOP.add_ref(three_straights)
TOP.add_ref(three_straights).movex(200)

route3 = gf.routing.get_route(three_straights.cells[-1].ports["o2"], three_straights2.cells[0].ports["o1"], with_sbend=True)
TOP.add(route3.references)

TOP.show()

print(three_straights.cells)
print(three_straights2.cells)