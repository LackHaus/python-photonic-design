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
print(PDK.layers)
disp_layers()

## Parameter Definition
# Ring radii (will become a list eventually)
ring_radii = [7, 7, 7, 7]
# Ring gaps for stage 1 (will become a list eventually)
ring_gaps_1 = [0.3, 1, 0.6]
# Ring gaps for stage 2 (will become a list eventually)
ring_gaps_2 = [2, 3, 0.1]
# Ring heater width (will probably remain constant)
heater_width = 0.5
# Ring heater discontinuity: The distance between V+ and GND ports on the ring heater
ring_heater_discontinuity = 3
# Waveguide width 
wg_width = 0.5
# Heater via dimensions
htr_via_size = (1, 6)

# Cell definition

# AMF BLACKBOXES
#--------------#
# AMF Edge Coupler blackbox instance
edge_coupler_left = PDK.get_component("AMF_Si_EdgeCoupler_Cband_v3p0_SiEPIC")
# AMF 1x2 Multimode Interferometer blackbox instance
mmi_1x2 = PDK.get_component("AMF_Si_1X2MMI_Cband_v3p0_SiEPIC")
# AMF Polarization Beam Rotator Splitter blackbox instance
pbrs = PDK.get_component("AMF_Si_PBRS_Cband_v3p0_SiEPIC")
phase_shifter = PDK.get_component("AMF_Si_TOPhaseShifter1_Cband_v3p0_SiEPIC")


# CUSTOM CELLS
#------------#
ring_stage_1 = gf.components.ring_crow(radius=[ring_radii[0], ring_radii[1]], gaps = [ring_gaps_1[0], ring_gaps_1[1], ring_gaps_1[2]])
ring_stage_2 = gf.components.ring_crow(radius=[ring_radii[2], ring_radii[3]], gaps = [ring_gaps_2[0], ring_gaps_2[1], ring_gaps_2[2]])


# Building a ring heater Layer 223 si dummy for boolean operations
def build_ring_heater_HTR(r, htr_width, htr_disc, l="HTR_", via_dim=(1, 4)):
    dy = np.sqrt((r-htr_width/2)**2 - htr_disc**2/4)
    part_ring_heater = gf.Component()
    part_ring_heater.add_ref(gf.components.ring(radius=r, width=htr_width, layer=l))
    square_ring_heater = gf.Component()
    square_ring_heater.add_ref(gf.components.rectangle((htr_disc,4*htr_width), layer=l)).move((-htr_disc/2, -r-2*htr_width))
    square_via = gf.Component()
    square_via.add_ref(gf.components.rectangle(via_dim, layer=l))
    c = gf.Component()
    c.add_ref(gf.geometry.boolean(A=part_ring_heater, B=square_ring_heater, operation="not", layer=l))
    c.add_ref(square_via).move((htr_disc/2 - via_dim[0],-dy-via_dim[1]))
    c.add_ref(square_via).move((-htr_disc/2,-dy-via_dim[1]))
    c = c.rotate(90)
    return c

# Stage 1 Cell Definition
stage_1 = gf.Component()
ring_heater_htr_0 = build_ring_heater_HTR(ring_radii[0], heater_width, ring_heater_discontinuity, via_dim=htr_via_size)
ring_heater_htr_1 = build_ring_heater_HTR(ring_radii[1], heater_width, ring_heater_discontinuity, via_dim=htr_via_size)
stage_1.add_ref(ring_heater_htr_0).movey(ring_gaps_1[0]+ring_radii[0]+wg_width)
stage_1.add_ref(ring_heater_htr_1).movey(ring_gaps_1[0]+ring_radii[0]+wg_width+2*ring_radii[1]+ring_gaps_1[1]+wg_width)
stage_1.add_ref(ring_stage_1)

# Stage 2 Cell Definition
stage_2 = gf.Component()
ring_heater_htr_2 = build_ring_heater_HTR(ring_radii[2], heater_width, ring_heater_discontinuity, via_dim=htr_via_size)
ring_heater_htr_3 = build_ring_heater_HTR(ring_radii[3], heater_width, ring_heater_discontinuity, via_dim=htr_via_size)
stage_2.add_ref(ring_heater_htr_0).movey(ring_gaps_2[0]+ring_radii[2]+wg_width)
stage_2.add_ref(ring_heater_htr_1).movey(ring_gaps_2[0]+ring_radii[2]+wg_width+2*ring_radii[3]+ring_gaps_2[1]+wg_width)
stage_2.add_ref(ring_stage_2)

# Top Cell Construction 
TOP = gf.Component("TOP")
TOP.add_ref(stage_1)
TOP.add_ref(stage_2).movex(50)
TOP.show()






