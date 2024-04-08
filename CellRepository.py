from collections.abc import Callable
from functools import partial
from amfpdk import *
from pydantic import BaseModel

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
print(PDK.layers)
disp_layers()

# Parameter Definition

# Ring radii (will become a list eventually)
ring_radii = [7, 7, 7, 7]
# Ring gaps (will become a list eventually)
ring_gaps = [0.3, 0.3, 0.3, 0.3]
# Ring heater width (will probably remain constant)
heater_width = 0.5
# Ring heater discontinuity: The distance between V+ and GND ports on the ring heater
ring_heater_discontinuity = 4
# Waveguide width 
wg_width = 0.5


# Cell definition

# AMF BLACKBOXES
#--------------#
# AMF Edge Coupler blackbox instance
edge_coupler_left = PDK.get_component("AMF_Si_EdgeCoupler_Cband_v3p0_SiEPIC")
# AMF 1x2 Multimode Interferometer blackbox instance
mmi_1x2 = PDK.get_component("AMF_Si_1X2MMI_Cband_v3p0_SiEPIC")
# AMF Polarization Beam Rotator Splitter blackbox instance
pbrs = PDK.get_component("AMF_Si_PBRS_Cband_v3p0_SiEPIC")

# CUSTOM CELLS
#------------#
ring_stage_1 = gf.components.ring_crow(radius=[ring_radii[0], ring_radii[1]], gaps = [ring_gaps[0], ring_gaps[1]])
ring_stage_2 = gf.components.ring_crow(radius=[ring_radii[2], ring_radii[3]], gaps = [ring_gaps[2], ring_gaps[3]])


# Building a ring heater Layer 223 si dummy for boolean operations
def build_partial_ring_heater_HTR(r, htr_width, htr_disc, l="HTR_"):
    part_ring_heater = gf.Component()
    part_ring_heater.add_ref(gf.components.ring(radius=r, width=htr_width, layer=l))
    square_ring_heater = gf.Component()
    square_ring_heater.add_ref(gf.components.rectangle((htr_disc,2*htr_width), layer=l)).move((-htr_disc/2, -r-htr_width))
    c = gf.geometry.boolean(A=part_ring_heater, B=square_ring_heater, operation="not", layer=l).rotate(90)
    return c

MRR = gf.Component()

ring_heater_htr = build_partial_ring_heater_HTR(ring_radii[0], heater_width, ring_heater_discontinuity)
MRR.add_ref(ring_heater_htr).movey(ring_gaps[0]+ring_radii[0]+0.5)
MRR.add_ref(ring_stage_1)

MRR.show()






