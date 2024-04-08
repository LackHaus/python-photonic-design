# type: ignore
import gdsfactory as gf

from amfpdk.import_gds import import_gds_siepic as import_gds


@gf.functions.cache
def BondPad_100um() -> gf.Component:
    """Returns BondPad_100um fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.BondPad_100um()
      c.plot()
    """
    return import_gds("BondPad_100um.GDS")


@gf.functions.cache
def BondPad_75um() -> gf.Component:
    """Returns BondPad_75um fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.BondPad_75um()
      c.plot()
    """
    return import_gds("BondPad_75um.GDS")


@gf.functions.cache
def amf_Adiabatic_3dB_Coupler() -> gf.Component:
    """Returns amf_Adiabatic_3dB_Coupler fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Adiabatic_3dB_Coupler()
      c.plot()
    """
    return import_gds("amf_Adiabatic_3dB_Coupler.GDS")


@gf.functions.cache
def amf_Broadband_3dB_TE_1550() -> gf.Component:
    """Returns amf_Broadband_3dB_TE_1550 fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Broadband_3dB_TE_1550()
      c.plot()
    """
    return import_gds("amf_Broadband_3dB_TE_1550.GDS")


@gf.functions.cache
def amf_Broadband_3dB_TM_1550() -> gf.Component:
    """Returns amf_Broadband_3dB_TM_1550 fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Broadband_3dB_TM_1550()
      c.plot()
    """
    return import_gds("amf_Broadband_3dB_TM_1550.GDS")


@gf.functions.cache
def amf_Crossing() -> gf.Component:
    """Returns amf_Crossing fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Crossing()
      c.plot()
    """
    return import_gds("amf_Crossing.GDS")


@gf.functions.cache
def amf_Edge_Coupler_1310() -> gf.Component:
    """Returns amf_Edge_Coupler_1310 fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Edge_Coupler_1310()
      c.plot()
    """
    return import_gds("amf_Edge_Coupler_1310.GDS")


@gf.functions.cache
def amf_Edge_Coupler_1550() -> gf.Component:
    """Returns amf_Edge_Coupler_1550 fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Edge_Coupler_1550()
      c.plot()
    """
    return import_gds("amf_Edge_Coupler_1550.GDS")


@gf.functions.cache
def amf_GC_TE_1310_13d_Oxide() -> gf.Component:
    """Returns amf_GC_TE_1310_13d_Oxide fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_GC_TE_1310_13d_Oxide()
      c.plot()
    """
    return import_gds("amf_GC_TE_1310_13d_Oxide.GDS")


@gf.functions.cache
def amf_GC_TE_1310_20d_Oxide() -> gf.Component:
    """Returns amf_GC_TE_1310_20d_Oxide fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_GC_TE_1310_20d_Oxide()
      c.plot()
    """
    return import_gds("amf_GC_TE_1310_20d_Oxide.GDS")


@gf.functions.cache
def amf_GC_TE_1310_weis() -> gf.Component:
    """Returns amf_GC_TE_1310_weis fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_GC_TE_1310_weis()
      c.plot()
    """
    return import_gds("amf_GC_TE_1310_weis.GDS")


@gf.functions.cache
def amf_GC_TE_1550_13d_Oxide() -> gf.Component:
    """Returns amf_GC_TE_1550_13d_Oxide fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_GC_TE_1550_13d_Oxide()
      c.plot()
    """
    return import_gds("amf_GC_TE_1550_13d_Oxide.GDS")


@gf.functions.cache
def amf_GC_TE_1550_20d_Oxide() -> gf.Component:
    """Returns amf_GC_TE_1550_20d_Oxide fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_GC_TE_1550_20d_Oxide()
      c.plot()
    """
    return import_gds("amf_GC_TE_1550_20d_Oxide.GDS")


@gf.functions.cache
def amf_GC_TE_1550_20d_Polished() -> gf.Component:
    """Returns amf_GC_TE_1550_20d_Polished fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_GC_TE_1550_20d_Polished()
      c.plot()
    """
    return import_gds("amf_GC_TE_1550_20d_Polished.GDS")


@gf.functions.cache
def amf_GC_TE_1550_8d_Polished() -> gf.Component:
    """Returns amf_GC_TE_1550_8d_Polished fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_GC_TE_1550_8d_Polished()
      c.plot()
    """
    return import_gds("amf_GC_TE_1550_8d_Polished.GDS")


@gf.functions.cache
def amf_GC_TM_1550_13d_Oxide() -> gf.Component:
    """Returns amf_GC_TM_1550_13d_Oxide fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_GC_TM_1550_13d_Oxide()
      c.plot()
    """
    return import_gds("amf_GC_TM_1550_13d_Oxide.GDS")


@gf.functions.cache
def amf_GC_TM_1550_20d_Oxide() -> gf.Component:
    """Returns amf_GC_TM_1550_20d_Oxide fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_GC_TM_1550_20d_Oxide()
      c.plot()
    """
    return import_gds("amf_GC_TM_1550_20d_Oxide.GDS")


@gf.functions.cache
def amf_Heater_N() -> gf.Component:
    """Returns amf_Heater_N fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Heater_N()
      c.plot()
    """
    return import_gds("amf_Heater_N.GDS")


@gf.functions.cache
def amf_Modulator_Michelson() -> gf.Component:
    """Returns amf_Modulator_Michelson fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Modulator_Michelson()
      c.plot()
    """
    return import_gds("amf_Modulator_Michelson.GDS")


@gf.functions.cache
def amf_Photodetector_floating() -> gf.Component:
    """Returns amf_Photodetector_floating fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Photodetector_floating()
      c.plot()
    """
    return import_gds("amf_Photodetector_floating.GDS")


@gf.functions.cache
def amf_Photodetector_optimized() -> gf.Component:
    """Returns amf_Photodetector_optimized fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Photodetector_optimized()
      c.plot()
    """
    return import_gds("amf_Photodetector_optimized.GDS")


@gf.functions.cache
def amf_Polarization_Beam_Splitter() -> gf.Component:
    """Returns amf_Polarization_Beam_Splitter fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Polarization_Beam_Splitter()
      c.plot()
    """
    return import_gds("amf_Polarization_Beam_Splitter.GDS")


@gf.functions.cache
def amf_Polarization_Splitter_Rotator() -> gf.Component:
    """Returns amf_Polarization_Splitter_Rotator fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Polarization_Splitter_Rotator()
      c.plot()
    """
    return import_gds("amf_Polarization_Splitter_Rotator.GDS")


@gf.functions.cache
def amf_Terminator_TE_1550() -> gf.Component:
    """Returns amf_Terminator_TE_1550 fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Terminator_TE_1550()
      c.plot()
    """
    return import_gds("amf_Terminator_TE_1550.GDS")


@gf.functions.cache
def amf_Terminator_TM_1550() -> gf.Component:
    """Returns amf_Terminator_TM_1550 fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Terminator_TM_1550()
      c.plot()
    """
    return import_gds("amf_Terminator_TM_1550.GDS")


@gf.functions.cache
def amf_Thermal_Switch_2x2() -> gf.Component:
    """Returns amf_Thermal_Switch_2x2 fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_Thermal_Switch_2x2()
      c.plot()
    """
    return import_gds("amf_Thermal_Switch_2x2.GDS")


@gf.functions.cache
def amf_YBranch_TE_1550() -> gf.Component:
    """Returns amf_YBranch_TE_1550 fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_YBranch_TE_1550()
      c.plot()
    """
    return import_gds("amf_YBranch_TE_1550.GDS")


@gf.functions.cache
def amf_strip2rib() -> gf.Component:
    """Returns amf_strip2rib fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_strip2rib()
      c.plot()
    """
    return import_gds("amf_strip2rib.GDS")


@gf.functions.cache
def amf_strip2rib_lowloss() -> gf.Component:
    """Returns amf_strip2rib_lowloss fixed cell.

    .. plot::
      :include-source:

      import amfpdk

      c = amfpdk.component.components_siepic.amf_strip2rib()
      c.plot()
    """
    return import_gds("amf_strip2rib_lowloss.GDS")
