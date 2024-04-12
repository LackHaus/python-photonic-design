import math
from classes import *

top = gf.Component("TOP")
edge_coupler_cband_g = PDK.get_component("AMF_Si_EdgeCoupler_Cband_v3p0_SiEPIC")
mmi_1x2_cband_g = PDK.get_component("AMF_Si_1X2MMI_Cband_v3p0_SiEPIC")
pbrs_cband_g = PDK.get_component("AMF_Si_PBRS_Cband_v3p0_SiEPIC")



edge_coupler_cband = top.add_ref(edge_coupler_cband_g).rotate(180)
mmi_1x2_cband = top.add_ref(mmi_1x2_cband_g).movex(120)
#pbrs_cband = top.add_ref(pbrs_cband_g).move((300, 100))


route = gf.routing.get_route(edge_coupler_cband.ports["o1"], mmi_1x2_cband.ports["o1"])
#route2 = gf.routing.get_route(mmi_1x2_cband.ports["o2"], pbrs_cband.ports["o1"])

top.add(route.references)
#top.add(route2.references)

top.show()