import gdsfactory as gf
from gdsfactory.technology import LayerLevel, LayerMap, LayerStack

from amfpdk.layer_map import LAYER

nm = 1e-3


class LayerStackParameters:
    """Values used by get_layer_stack and get_process"""

    # Passive fixed parameters
    total_oxide: float = 3.0
    substrate_thickness: float = 0.5
    box_thickness: float = 2.0
    soi_thickness: float = 0.220
    soi_grat_thickness: float = 0.150
    soi_slab_thickness: float = 0.090
    sin_thickness: float = 0.4
    ge_thickness: float = 0.5
    psin_imd: float = 0.25

    # Active fixed parameters
    m1_thickness: float = 0.75
    htr_thickness: float = 0.12
    m2_thickness: float = 2.0
    m1_imd: float = 0.7
    htr_imd: float = 2.0
    htr_mt2_imd: float = 0.66

    # Passive variable parameters (User defined)
    zmin_psin: float = soi_thickness + psin_imd

    # Active variable parameters (User defined)
    zmin_via1: float = soi_slab_thickness
    zmin_m1: float = zmin_via1 + m1_imd
    zmin_htr: float = soi_thickness + htr_imd
    zmin_via2: float = zmin_htr + htr_thickness
    via2_thickness: float = total_oxide - zmin_via2
    zmin_m2: float = zmin_via2 + via2_thickness


def get_layer_stack(params: LayerStackParameters, layers: LayerMap) -> LayerStack:
    """Returns AMF LayerStack

    Based on AMF process manual available under NDA.

    Args:
        layer_stack_parameters: parameters used to build the layer stack
    """
    layers = dict(
        # Passive layers
        substrate=LayerLevel(
            layer=layers.WAFER,
            thickness=params.substrate_thickness,
            zmin=-params.substrate_thickness - params.box_thickness,
            material="si",
            mesh_order=101,
            orientation="100",
        ),
        box=LayerLevel(
            layer=layers.WAFER,
            thickness=params.box_thickness,
            zmin=-params.box_thickness,
            material="sio2",
            mesh_order=9,
        ),
        core=LayerLevel(
            layer=layers.RIB_,
            thickness=params.soi_thickness,
            zmin=0.0,
            material="si",
            mesh_order=2,
            orientation="100",
            info={"active": True},
        ),
        clad=LayerLevel(
            layer=layers.WAFER,
            thickness=params.total_oxide,
            material="sio2",
            zmin=0.0,
            mesh_order=10,
        ),
        slab150=LayerLevel(
            layer=layers.GRAT_,
            thickness=params.soi_grat_thickness,
            zmin=0.0,
            material="si",
            mesh_order=3,
        ),
        slab90=LayerLevel(
            layer=layers.SLAB_,
            thickness=params.soi_slab_thickness,
            zmin=0.0,
            material="si",
            mesh_order=2,
        ),
        psin=LayerLevel(
            layer=layers.SiNwg1_,
            thickness=params.sin_thickness,
            zmin=params.zmin_psin,
            material="sin",
            mesh_order=2,
        ),
        ge=LayerLevel(
            layer=layers.GeEP_,
            thickness=params.ge_thickness,
            zmin=params.soi_thickness,
            material="ge",
            mesh_order=1,
        ),
        # Active layers
        via1=LayerLevel(
            layer=layers.VIA1_,
            thickness=params.m1_imd,
            zmin=params.zmin_via1,
            material="Aluminum",
            mesh_order=1,
        ),
        metal1=LayerLevel(
            layer=layers.MT1_,
            thickness=params.m1_thickness,
            zmin=params.zmin_m1,
            material="Aluminum",
            mesh_order=2,
        ),
        via2=LayerLevel(
            layer=layers.VIA2_,
            thickness=params.via2_thickness,
            zmin=params.zmin_via2,
            material="Aluminum",
            mesh_order=1,
        ),
        metal2=LayerLevel(
            layer=layers.MT2_,
            thickness=params.m2_thickness,
            zmin=params.zmin_m2,
            material="Aluminum",
            mesh_order=2,
        ),
        htr=LayerLevel(
            layer=layers.HTR_,
            thickness=params.htr_thickness,
            zmin=params.zmin_htr,
            material="tin",
            mesh_order=1,
        ),
    )

    return LayerStack(layers=layers)


LAYER_STACK = get_layer_stack(LayerStackParameters(), LAYER)

WAFER_STACK = LayerStack(
    layers={
        k: get_layer_stack(LayerStackParameters(), LAYER).layers[k]
        for k in (
            "substrate",
            "box",
            "core",
        )
    }
)

if __name__ == "__main__":
    ls = get_layer_stack(LayerStackParameters(), LAYER)
    c = gf.Component("test")
    _ = c << gf.components.straight(length=10, cross_section="xs_sc", layer="SiNwg1_")
    scene = c.to_3d(layer_stack=ls)
    scene.show(blocked=True)
