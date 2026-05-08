COPPER_DB = [
    {"grade":"CP-80", "d50":80e-6, "eps":(0.50,0.58)},
    {"grade":"CP-100","d50":100e-6,"eps":(0.52,0.60)},
    {"grade":"CP-150","d50":150e-6,"eps":(0.55,0.63)},
]

def match_copper_powder(d_req, eps_req):
    out = []
    for p in COPPER_DB:
        if p["eps"][0] <= eps_req <= p["eps"][1]:
            out.append({
                "grade": p["grade"],
                "d50_um": p["d50"]*1e6,
                "eps_range": p["eps"]
            })
    return out