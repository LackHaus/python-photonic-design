"""
Description : Generate AMF PDK important scripts (Import GDS and Layer Views) if executed. Else, contains function to import pdk and activate amf tech.
"""
import gdsfactory as gf

from amfpdk.config import PATH

if __name__ == "__main__":
    component_script_bbox = gf.write_cells.get_import_gds_script(
        dirpath=PATH.gds_amf_bb,
        module="amfpdk.component.components_bbox",
    )

    component_script_siepic = gf.write_cells.get_import_gds_script(
        dirpath=PATH.gds_siepiclib,
        module="amfpdk.component.components_siepic",
    )

    # LAYER_VIEWS = gf.technology.LayerViews(filepath=PATH.lyp)
    # LAYER_VIEWS.to_yaml(PATH.layer_yaml)
