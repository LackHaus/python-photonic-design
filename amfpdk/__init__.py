"""amfpdk - GDS factory implementation of the AMF PDK."""
import pathlib

from gdsfactory.config import logger
from gdsfactory.generic_tech import get_generic_pdk
from gdsfactory.get_factories import get_cells
from gdsfactory.pdk import Pdk

from amfpdk.components_library import components_bbox, components_siepic_lib
from amfpdk.config import module_path
from amfpdk.cross_section import cross_sections
from amfpdk.layer_map import LAYER, LAYER_VIEWS

__version__ = "1.0.0"
__author__ = "Pascal Audet <paudet@outlook.com>"

__all__ = ["PDK", "cells"]

logger.info(f"Found AMFpdk {__version__!r} installed at {module_path!r}")

constants = {
    "fiber_array_spacing": 127.0,
    "fiber_spacing": 50.0,
    "fiber_input_to_output_spacing": 200.0,
    "metal_spacing": 10.0,
    "pad_spacing": 125.0,
    "pad_size": (100, 100),
}
cells = get_cells(components_bbox) | get_cells(components_siepic_lib)
PDK = Pdk(
    name="AMF",
    cells=get_cells(components_bbox) | get_cells(components_siepic_lib),
    cross_sections=cross_sections,
    layers=dict(LAYER),
    layer_views=LAYER_VIEWS,
    constants=constants,
    base_pdk=get_generic_pdk(),
)

PDK.register_cells_yaml(dirpath=pathlib.Path(__file__).parent.absolute())
PDK.activate()

if __name__ == "__main__":
    f = PDK.cells
    print(f.keys())
