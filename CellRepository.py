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

## Parameter Definition
# Ring radii for stage (will become a list eventually)
ring_radii = [10, 4, 6, 6]
# Ring gaps (will become a list eventually)
ring_gaps = [1, 2, 0.3, 0.5, 1, 0.5]
# Ring heater width (will probably remain constant)
heater_width = 2
# Ring heater discontinuity: The distance between V+ and GND ports on the ring heater
ring_heater_discontinuity = 3
# Waveguide width 
wg_width = 1
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

# Building a ring heater Layer 223 si dummy for boolean operations
def build_ring_heater(r, htr_width, htr_disc, l="HTR_", via_dim=(1, 4)):
    dy = np.sqrt((r-htr_width/2)**2 - htr_disc**2/4)
    part_ring_heater = gf.Component("d")
    part_ring_heater.add_ref(gf.components.ring(radius=r, width=htr_width, layer=l))
    square_ring_heater = gf.Component("f")
    square_ring_heater.add_ref(gf.components.rectangle((htr_disc,4*htr_width), layer=l)).move((-htr_disc/2, -r-2*htr_width))
    square_via = gf.Component("g")
    square_via.add_ref(gf.components.rectangle(via_dim, layer=l))
    c = gf.Component("h")
    c.add_ref(gf.geometry.boolean(A=part_ring_heater, B=square_ring_heater, operation="not", layer=l))
    c.add_ref(square_via).move((htr_disc/2 - via_dim[0],-dy-via_dim[1]))
    c.add_ref(square_via).move((-htr_disc/2,-dy-via_dim[1]))
    c = c.rotate(90)
    return c

def change_layer(comp, l):
    generic_component = gf.Component()
    merged_component = gf.geometry.boolean(A=comp, B=generic_component, operation="or", layer=l)
    return merged_component

def build_ring_stage(stage, ring_radii_=ring_radii, ring_gaps_=ring_gaps, wg_width_=wg_width, layer_="RIB_"):

    ring_stage = gf.Component("Ring Stage "+str(stage))
    if stage == 1:
        ring_0 = gf.components.ring(radius=ring_radii_[0], width=wg_width_, angle_resolution=2.5, layer=layer_, angle=360)
        ring_1 = gf.components.ring(radius=ring_radii_[1], width=wg_width_, angle_resolution=2.5, layer=layer_, angle=360)
        wg_1 = gf.components.straight(length = wg_width_+2*np.max([ring_radii_[0], ring_radii_[1]]), width=wg_width_)
        ring_stage.add_ref(wg_1)
        ring_stage.add_ref(ring_0).move((wg_width_/2+np.max([ring_radii_[0], ring_radii_[1]]), ring_radii_[0]+wg_width_+ring_gaps_[0]))
        ring_stage.add_ref(ring_1).move((wg_width_/2+np.max([ring_radii_[0], ring_radii_[1]]), 2*ring_radii_[0]+wg_width_+ring_gaps_[0]+ring_radii_[1]+ring_gaps_[1]+wg_width_))
        ring_stage.add_ref(wg_1).movey(2*ring_radii_[0]+wg_width_+ring_gaps_[0]+2*ring_radii_[1]+ring_gaps_[1]+wg_width_+ring_gaps_[2]+wg_width_)

    elif stage == 2:
        ring_0 = gf.components.ring(radius=ring_radii_[2], width=wg_width_, angle_resolution=2.5, layer=layer_, angle=360)
        ring_1 = gf.components.ring(radius=ring_radii_[3], width=wg_width_, angle_resolution=2.5, layer=layer_, angle=360)
        wg_1 = gf.components.straight(length = wg_width_+2*np.max([ring_radii_[2], ring_radii_[3]]), width=wg_width_)
        ring_stage.add_ref(wg_1)
        ring_stage.add_ref(ring_0).move((wg_width_/2+np.max([ring_radii_[2], ring_radii_[3]]), ring_radii_[2]+wg_width_+ring_gaps_[3]))
        ring_stage.add_ref(ring_1).move((wg_width_/2+np.max([ring_radii_[2], ring_radii_[3]]), 2*ring_radii_[2]+wg_width_+ring_gaps_[3]+ring_radii_[3]+ring_gaps_[4]+wg_width_))
        ring_stage.add_ref(wg_1).movey(2*ring_radii_[2]+wg_width_+ring_gaps_[3]+2*ring_radii_[3]+ring_gaps_[4]+wg_width_+ring_gaps_[5]+wg_width_)

    return ring_stage

def build_ring_stage_heater(stage, ring_radii_=ring_radii, ring_gaps_=ring_gaps, wg_width_=wg_width, layer_="HTR_"):
    stage_2 = gf.Component("2")
    ring_heater_htr_2 = build_ring_heater(ring_radii_[2], heater_width, ring_heater_discontinuity, via_dim=htr_via_size)
    ring_heater_htr_3 = build_ring_heater(ring_radii_[3], heater_width, ring_heater_discontinuity, via_dim=htr_via_size)
    stage_2.add_ref(ring_heater_htr_2).movey(ring_gaps_[3]+ring_radii_[2]+wg_width_)
    stage_2.add_ref(ring_heater_htr_3).movey(ring_gaps_[3]+ring_radii_[2]+wg_width_+2*ring_radii_[3]+ring_gaps_[4]+wg_width_)
    return stage_2

def build_stage(stage, ring_radii_=ring_radii, ring_gaps_=ring_gaps, wg_width_=wg_width):
    stage = gf.Component("1")
    ring_stage = build_ring_stage(stage, ring_radii_, ring_gaps_, wg_width_)
    ring_heater_stage = build_ring_stage_heater(stage, ring_radii_, ring_gaps_, wg_width_)
    stage.add_ref(ring_stage)
    stage.add_ref(ring_heater_stage).movex(-1*np.max([ring_radii_[2], ring_radii_[3]])-wg_width_/2)
    return stage

# Stage 2 Cell Definition
build_ring_stage(2).show()

