import gdsfactory as gf
import gdstk

from amfpdk import layer_map
from amfpdk.config import PATH

port_width_o = 0.5
port_width_e = 10.0

layers_dict = {
    "si": "RIB_",
    "Si": "RIB_",
    "sin": "SiNwg1_",
    "MT1": "MT1_",
    "MT2": "MT2_",
    "opt": "RIB_",
    "elec": "MT2_",
}

port_type_dict = {
    "opt": "optical",
    "elec": "electrical",
}

port_width_dict = {
    "opt": port_width_o,
    "elec": port_width_e,
}


def get_port_orientation_bbox(label: gdstk.Label, bbox_polygon: gdstk.Polygon) -> int:
    """
    Description : Guess the port orientation based on label origin position
    Args:
        label (gdstk.Label): port label
        bbox (gdstk.Polygon): bbox polygon
    Returns:
        int: port orientation in degrees
    """
    bbox = bbox_polygon.bounding_box()
    if label.origin[0] == bbox[0][0]:
        return 180
    elif label.origin[0] == bbox[1][0]:
        return 0
    elif label.origin[1] == bbox[0][1]:
        return 270
    else:
        return 90


#######################################################################################
# Port tools for bbox components
#######################################################################################


def add_ports_bbox(component: gf.Component) -> gf.Component:
    """
    Description : Add ports to the component based on bbox polygon and opt/elec ports polygons
    Args:
        component (gf.Component): component to add ports to
    Returns:
        gf.Component: component with ports
    """
    labels = component.get_labels()

    c_polygons = component.get_polygons(by_spec=True, as_array=False, as_shapely=True)
    bbox_polygon = c_polygons[layer_map.LAYER.BLACKBOX_][0]

    # Iterate over opt port polygon lists, guess the orientation and add port to the component
    for i, label in enumerate(labels):
        label_name = label.text.split("_")
        if label_name[0] in ["opt", "elec"] and label.layer not in [
            999,
            997,
        ]:  # Exclude SiEPIC ports layer
            port_orientation = get_port_orientation_bbox(label, bbox_polygon)
            port = gf.Port(
                name=label_name[0][0] + str(i),
                center=label.origin,
                width=port_width_dict[label_name[0]],
                orientation=port_orientation,
                layer=layers_dict[label_name[2]],
                port_type=port_type_dict[label_name[0]],
                enforce_ports_on_grid=True,
            )
            component.add_port(port)
    component.auto_rename_ports()
    return component


#######################################################################################
# Port tools for SiEPIC components
#######################################################################################


def add_ports_siepic(component: gf.Component) -> gf.Component:
    """
    Description : Add ports to the component based on PinRec layer and PinRecM layer
    Args:
        component (gf.Component): component to add ports to
    Returns:
        gf.Component: component with ports
    """
    # Get bounding box polygon
    labels = component.get_labels()
    c_polygons = component.get_polygons(by_spec=True, as_array=False, as_shapely=True)
    bbox_polygon = c_polygons[layer_map.LAYER.DevRec][0]

    # Iterate over opt port polygon, guess the orientation and add port to the component
    for label in labels:
        name = label.text
        if name[:-1] in ["opt", "elec"]:
            port_orientation = get_port_orientation_bbox(label, bbox_polygon)
            port = gf.Port(
                name=name[0] + name[-1],
                center=label.origin,
                width=port_width_dict[name[:-1]],
                orientation=port_orientation,
                layer=layers_dict[
                    name[:-1]
                ],  # Generic port layer, we don't know the true layer of the ports.
                enforce_ports_on_grid=True,
                port_type=port_type_dict[name[:-1]],
            )
            component.add_port(port)

    return component


#######################################################################################
# import_gds tools
#######################################################################################
def import_gds_bbox(gdspath: str, **kwargs):  # type: ignore
    return gf.import_gds(
        gdspath,
        gdsdir=PATH.gds_amf_bb,
        library="AMF PDK BB",
        model=gdspath.split(".")[0],
        decorator=add_ports_bbox,
        **kwargs,
    )


def import_gds_siepic(gdspath: str, **kwargs):  # type: ignore
    return gf.import_gds(
        gdspath,
        gdsdir=PATH.gds_siepiclib,
        library="SiEPIC AMF",
        model=gdspath.split(".")[0],
        decorator=add_ports_siepic,
        **kwargs,
    )
