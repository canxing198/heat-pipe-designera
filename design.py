import numpy as np
from scipy.optimize import fsolve
from copper_powder import match_copper_powder
from boiling import check_boiling

# --- Physical Properties ---
def props(T_C):
    """Returns physical properties of water at a given temperature."""
    T = T_C + 273.15
    return dict(
        sigma=0.058,      # N/m
        mu=2.82e-4,       # Pa.s
        h_fg=2.26e6,      # J/kg
        rho_l=1000,      # kg/m³
        rho_v=0.2,       # kg/m³
        k_eff=10         # W/m.K (effective wick conductivity)
    )

def design_engine(inputs):
    # Unpack inputs
    D_out = inputs["D_out"]
    t_wall = inputs["t_wall"]
    b_flat = inputs["b_flat"]
    L = inputs["L"]
    Q = inputs["Q"]
    A_evap = inputs["A_evap"]
    T_v = inputs["T_v"]

    # --- Geometry ---
    D_in = D_out - 2 * t_wall
    Dh = 2 * D_in * b_flat / (D_in + b_flat)
    t_wick_max = (b_flat - Dh) / 2
    A_w = (b_flat - Dh) * D_in

    # --- Boiling Check ---
    ok, Q_boil = check_boiling(Q, A_evap, t_wick_max, T_v)
    if not ok:
        return {"status": "FAIL", "reason": "沸腾极限不足"}

    # --- Capillary Limit (Inverse Design) ---
    p = props(T_v)
    
    def eq(vars):
        d, eps = vars
        r_eff = (d / 2) * np.sqrt((1 - eps) ** 2 / eps ** 3)
        K = (d ** 2 * eps ** 3) / (150 * (1 - eps) ** 2)
        Qc = (2 * p["sigma"] / r_eff) * (K * A_w) / (p["mu"] * L * p["h_fg"])
        return Qc - Q  # Target is to make Qc equal to Q

    d0, eps0 = 100e-6, 0.55
    d, eps = fsolve(eq, [d0, eps0])

    # --- Copper Powder Matching ---
    matches = match_copper_powder(d, eps)
    if not matches:
        return {"status": "FAIL", "reason": "无匹配铜粉"}
    best = matches[0]

    # --- Fill Volume Calculation ---
    t_wick = 0.8 * t_wick_max
    V_fill = eps * A_w * L * 1.1
    m_fill = p["rho_l"] * V_fill

    return {
        "status": "OK",
        "grade": best.get("grade"),
        "d50_um": best.get("d50_um"),
        "eps": eps,
        "t_wick_mm": t_wick * 1e3,
        "m_fill_g": m_fill * 1e3,
        "Q_boil_W": Q_boil,
    }
