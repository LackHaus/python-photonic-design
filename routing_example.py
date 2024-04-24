import math
from classes import *

top = gf.Component("TOP")

mmi_stage_1 = MMI1x2Stage(n_mmis_=1)
mmi_stage_2 = MMI1x2Stage(n_mmis_=2)
mmi_stage_3 = MMI1x2Stage(n_mmis_=4)

for i in [mmi_stage_1, mmi_stage_2, mmi_stage_3]:
    for j in i.mmis:
        print(j)

top.add_ref(mmi_stage_1.inst)
top.add_ref(mmi_stage_2.inst).movex(120)
top.add_ref(mmi_stage_3.inst).movex(240)

print(top.ports)

route = gf.routing.get_route(mmi_stage_1.mmis[0].inst.ports["o2"], mmi_stage_2.mmis[1].inst.ports["o1"])

top.add(route.references)

top.show()