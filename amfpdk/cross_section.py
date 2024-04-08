"""
Descriptions : Cross sections based on AMF technology.
"""

import sys
from functools import partial

import gdsfactory as gf
import gdsfactory.cross_section as gcs

from amfpdk.layer_map import LAYER

nm = 1e-3

############################
# Add pins functions
############################
add_pins_optical = partial(gf.add_pins.add_pins_siepic_optical, layer_pin=LAYER.PinRec)
add_pins_electrical = partial(
    gf.add_pins.add_pins_siepic, layer_pin=LAYER.PinRecM, port_type="electrical"
)


############################
# Cross-sections functions
############################
strip = partial(
    gcs.strip,
    width=0.5,
    layer="RIB_",
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

strip_auto_widen = partial(
    gcs.strip,
    width=0.5,
    layer="RIB_",
    auto_widen=True,
    width_wide=3.0,
    taper_length=50.0,
    auto_widen_minimum_length=300.0,
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

strip_no_pins = partial(
    gcs.strip_no_pins,
    width=0.5,
    layer="RIB_",
)

rib = partial(
    gcs.strip,
    layer="RIB_",
    bbox_layers=["DevRec"],
    bbox_offsets=[0.0],
    sections=(gcs.Section(width=6, layer="SLAB_", name="slab", simplify=50 * nm),),
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)
rib2 = partial(
    gcs.strip,
    layer="RIB_",
    cladding_layers=("SLAB_",),
    cladding_offsets=(3,),
    cladding_simplify=(50 * nm,),
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

rib_bbox = partial(
    gcs.strip,
    layer="RIB_",
    bbox_layers=["SLAB_"],
    bbox_offsets=(3,),
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

nitride = partial(
    gcs.strip,
    layer="SiNwg1_",
    width=1.0,
)

strip_rib_tip = partial(
    gcs.strip,
    layer="RIB_",
    sections=(gcs.Section(width=0.2, layer="SLAB_", name="slab"),),
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

l_wg = partial(
    gcs.strip,
    sections=(gcs.Section(width=4, layer="SLAB_", name="slab", offset=-2 - 0.25),),
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

strip_heater_metal = partial(
    gcs.strip_heater_metal,
    layer="RIB_",
    layer_heater="HTR_",
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

strip_heater_metal_undercut = partial(
    gcs.strip_heater_metal_undercut,
    layer="RIB_",
    layer_heater="HTR_",
    layer_trench="DTR_",
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)


def slot(
    width: float = 0.5,
    layer: gcs.LayerSpec = "RIB_",
    slot_width: float = 0.04,
    sections: tuple[gcs.Section, ...] | None = None,
    add_pins_function_name: str = "add_pins_optical",
    add_pins_function_module: str = "amfpdk.cross_section",
) -> gcs.CrossSection:
    """Return CrossSection Slot (with an etched region in the center).

    Args:
        width: main Section width (um) or function parameterized from 0 to 1. \
                the width at t==0 is the width at the beginning of the Path. \
                the width at t==1 is the width at the end.
        layer: main section layer.
        slot_width: in um.
        sections: list of Sections(width, offset, layer, ports).

    .. plot::
        :include-source:

        import gdsfactory as gf

        xs = gf.cross_section.slot(width=0.5, slot_width=0.05, layer='WG')
        p = gf.path.arc(radius=10, angle=45)
        c = p.extrude(xs)
        c.plot()
    """
    rail_width = (width - slot_width) / 2
    rail_offset = (rail_width + slot_width) / 2

    sections = sections or ()
    sections += (
        gcs.Section(
            width=rail_width, offset=rail_offset, layer=layer, name="left_rail"
        ),
        gcs.Section(
            width=rail_width, offset=-rail_offset, layer=layer, name="right rail"
        ),
    )

    return strip(
        width=width,
        layer=None,
        sections=sections,
        add_pins_function_name=add_pins_function_name,
        add_pins_function_module=add_pins_function_module,
    )


metal1 = partial(
    gcs.cross_section,
    layer="MT1_",
    width=10.0,
    port_names=gcs.port_names_electrical,
    port_types=gcs.port_types_electrical,
    add_pins_function_name="add_pins_electrical",
    add_pins_function_module="amfpdk.cross_section",
    min_length=5,
    gap=5,
)

metal2 = partial(
    metal1,
    layer="MT2_",
)

heater_metal = partial(
    metal1,
    width=2.5,
    layer="HTR_",
)

npp = partial(metal1, layer="NCONT_", width=0.5, add_pins_function_name=None)

strip_heater_doped = partial(
    gcs.strip_heater_doped,
    layer="RIB_",
    layers_heater=("RIB_", "NCONT_"),
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

strip_heater_doped_via_stack = partial(
    strip_heater_doped,
    layers_heater=("RIB_", "NCONT_", "VIA1_"),
    bbox_offsets_heater=(0, 0.1, -0.2),
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

rib_heater_doped = partial(
    gcs.rib_heater_doped,
    layer="RIB_",
    layer_heater="NCONT_",
    layer_slab="SLAB_",
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

rib_heater_doped_via_stack = partial(
    gcs.rib_heater_doped_via_stack,
    layer="RIB_",
    layer_heater="NCONT_",
    layer_slab="SLAB_",
    layers_via_stack=("NCONT_", "VIA1_"),
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

pn_ge_detector_si_contacts = partial(
    gcs.pn_ge_detector_si_contacts,
    layer_si="RIB_",
    layer_ge="GeEP_",
    layer_p="PIM_",
    layer_pp="IPD_",
    layer_ppp="PCONT_",
    layer_n="NIM_",
    layer_np="IND_",
    layer_npp="NCONT_",
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

rib_with_trenches = partial(
    gcs.rib_with_trenches,
    layer="RIB_",
    layer_trench="DTR_",
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

pn = partial(
    gcs.pn,
    layer="RIB_",
    layer_slab="SLAB_",
    layer_p="PIM_",
    layer_pp="IPD_",
    layer_ppp="PCONT_",
    layer_n="NIM_",
    layer_np="IND_",
    layer_npp="NCONT_",
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

pin = partial(
    gcs.pin,
    layer="RIB_",
    layer_slab="SLAB_",
    layers_via_stack1=("PCONT_",),
    layers_via_stack2=("NCONT_",),
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

pn_with_trenches = partial(
    gcs.pn_with_trenches,
    layer_p="PIM_",
    layer_pp="IPD_",
    layer_ppp="PCONT_",
    layer_n="NIM_",
    layer_np="IND_",
    layer_npp="NCONT_",
    layer_trench="DTR_",
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

pn_with_trenches_asymmetric = partial(
    gcs.pn_with_trenches_asymmetric,
    layer_p="PIM_",
    layer_pp="IPD_",
    layer_ppp="PCONT_",
    layer_n="NIM_",
    layer_np="IND_",
    layer_npp="NCONT_",
    layer_trench="DTR_",
    add_pins_function_name="add_pins_optical",
    add_pins_function_module="amfpdk.cross_section",
)

# Cross sections variables
xs_sc = strip()
xs_sc_auto_widen = strip_auto_widen()
xs_sc_no_pins = strip_no_pins()

xs_rc = rib()
xs_rc2 = rib2()
xs_rc_bbox = rib_bbox()

xs_sc_rc_tip = strip_rib_tip()
xs_sc_heater_metal = strip_heater_metal()
xs_sc_heater_metal_undercut = strip_heater_metal_undercut()
xs_slot = slot()

xs_heater_metal = heater_metal()
xs_sc_heater_doped = strip_heater_doped()
xs_sc_heater_doped_via_stack = strip_heater_doped_via_stack()

xs_rc_heater_doped = rib_heater_doped()
xs_rc_heater_doped_via_stack = rib_heater_doped_via_stack()
xs_pn_ge = pn_ge_detector_si_contacts()

xs_m1 = metal1()
xs_m2 = metal2()
xs_metal_routing = xs_m2

xs_pn = pn()
xs_pin = pin()
xs_npp = npp()


cross_sections = gcs.get_cross_sections(sys.modules[__name__])
