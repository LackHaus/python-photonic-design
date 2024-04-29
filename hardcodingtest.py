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

edge_coupler = gf.components.edge_coupler_silicon()


mmi = PDK.get_component("AMF_Si_1X2MMI_Cband_v3p0")


pbrs = PDK.get_component("AMF_Si_PBRS_Cband_v3p0")


rings = gf.components.ring_crow(gaps=[0.2, 0.2, 0.2], radius=[10, 10])
pbrs2 = PDK.get_component("AMF_Si_PBRS_Cband_v3p0")

pd = PDK.get_component("AMF_Ge_PD56G_Cband_v3p0")




edge_coup_1 = top.add_ref(edge_coupler).rotate(180)
mmi_1 = top.add_ref(mmi).movex(10)
pbrs_1 = top.add_ref(pbrs).move((150, 100))
pbrs_2 = top.add_ref(pbrs).move((150, -100))
rings_1 = top.add_ref(rings).move((650, 50))
rings_2 = top.add_ref(rings).move((650, 120))
rings_3 = top.add_ref(rings).move((650, -80))
rings_4 = top.add_ref(rings).move((650, -150))
pbrs_3 = (top.add_ref(pbrs).rotate(180)).move((1150, 115))
pbrs_4 = (top.add_ref(pbrs).rotate(180)).move((1150, -85))
pd_1 = top.add_ref(pd).move((1300, 150))
pd_2 = top.add_ref(pd).move((1300, -150))

route1 = gf.routing.get_route(edge_coup_1.ports["o1"], mmi_1.ports["o1"])
route2 = gf.routing.get_route(mmi_1.ports["o2"], pbrs_1.ports["o1"])
route3 = gf.routing.get_route(mmi_1.ports["o3"], pbrs_2.ports["o1"])
route4 = gf.routing.get_route(pbrs_1.ports["o2"], rings_2.ports["o1"])
route5 = gf.routing.get_route(pbrs_1.ports["o3"], rings_1.ports["o1"])
route6 = gf.routing.get_route(pbrs_2.ports["o2"], rings_3.ports["o1"])
route7 = gf.routing.get_route(pbrs_2.ports["o3"], rings_4.ports["o1"])
route8 = gf.routing.get_route(rings_2.ports["o4"], pbrs_3.ports["o3"])
route9 = gf.routing.get_route(rings_1.ports["o4"], pbrs_3.ports["o2"])
route10 = gf.routing.get_route(rings_3.ports["o4"], pbrs_4.ports["o3"])
route11 = gf.routing.get_route(rings_4.ports["o4"], pbrs_4.ports["o2"])
route12 = gf.routing.get_route(pbrs_3.ports["o1"], pd_1.ports["o1"])
route13 = gf.routing.get_route(pbrs_4.ports["o1"], pd_2.ports["o1"])

top.add(route1.references)
top.add(route2.references)
top.add(route3.references)
top.add(route4.references)
top.add(route5.references)
top.add(route6.references)
top.add(route7.references)
top.add(route8.references)
top.add(route9.references)
top.add(route10.references)
top.add(route11.references)
top.add(route12.references)
top.add(route13.references)

top.show()
