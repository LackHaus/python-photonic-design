from classes import *

top = gf.Component("TOP")
edge_coupler_cband = PDK.get_component("AMF_Si_EdgeCoupler_Cband_v3p0_SiEPIC").rotate(180)
mmi_1x2_cband = PDK.get_component("AMF_Si_1X2MMI_Cband_v3p0_SiEPIC")
pbrs_cband = PDK.get_component("AMF_Si_PBRS_Cband_v3p0_SiEPIC")

edge_coupler_cband = top.add_ref(PDK.get_component("AMF_Si_EdgeCoupler_Cband_v3p0_SiEPIC").rotate(180))
mmi_1x2_cband = top.add_ref(PDK.get_component("AMF_Si_1X2MMI_Cband_v3p0_SiEPIC")).movex(120)

route = gf.routing.get_route(edge_coupler_cband.ports["o1"], mmi_1x2_cband.ports["o1"])

top.add(route.references)

top.show()