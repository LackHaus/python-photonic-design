from classes import *

top = gf.Component("TOP")

edge_coupler_cband = PDK.get_component("AMF_Si_EdgeCoupler_Cband_v3p0_SiEPIC").rotate(180)
mmi_1x2_cband = PDK.get_component("AMF_Si_1X2MMI_Cband_v3p0_SiEPIC")
pbrs_cband = PDK.get_component("AMF_Si_PBRS_Cband_v3p0_SiEPIC")

top.add_ref(edge_coupler_cband)
top.add_ref(mmi_1x2_cband).movex(120)
top.add_ref(pbrs_cband).movex(300)

top.show()
