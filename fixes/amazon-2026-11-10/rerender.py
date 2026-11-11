import sys, os
sys.path.insert(0, '/home/claude/cgap/pipeline')
import cgap_batch as cb
jobs = [
    {"header": "CAUTION", "sku": "CGAP-C18024-812", "lines": ["TRIP HAZARD", "PRESS STAGING PAD", "FLAT EDGES MUST STAY DOWN", "REPORT CURLED EDGES"]},
    {"header": "NOTICE", "sku": "CGAP-N25326-812", "lines": ["MANWAY COVER STAGING PAD", "SET COVER ON MAT", "KEEP GASKET FACE UP AND CLEAN", "RETURN COVER TO SAME MANWAY"]},
]
for j in jobs:
    s = j["sku"].lower() + "-r2"
    j["img"] = [f"{s}.jpg", f"{s}-durability.jpg", f"{s}-mnt2.jpg"]
    j["reads"] = " / ".join(j["lines"])
    n = cb._work(j)
    print(j["sku"], "rendered" if n else "skipped", [os.path.getsize(os.path.join(cb.IMGDIR, x)) for x in j["img"]])
