def match_copper_powder(target_d, target_eps):
    powder_db = [
        {"grade":"CP-100","d50_um":100,"eps_range":(0.50,0.60)},
        {"grade":"CP-80","d50_um":80,"eps_range":(0.52,0.62)},
        {"grade":"CP-150","d50_um":150,"eps_range":(0.45,0.55)}
    ]

    matches = []
    for p in powder_db:
        if abs(p["d50_um"]*1e-6 - target_d) < 30e-6 and \
           p["eps_range"][0] <= target_eps <= p["eps_range"][1]:
            matches.append(p)
    return matches
