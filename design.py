import numpy as np
from scipy.optimize import fsolve
from copper_powder import match_copper_powder
from boiling import check_boiling

def design_engine(inputs):
    D_out = inputs["D_out"]
    t_wall = inputs["t_wall"]
    b_flat = inputs["b_flat"]
    L = inputs["L"]
    Q = inputs["Q"]
    A_evap = inputs["A_evap"]
    T_v = inputs["T_v"]

    # ===== 几何 =====
    D_in = D_out - 2*t_wall
    Dh = 2*D_in*b_flat/(D_in+b_flat)
    t_wick_max = (b_flat - Dh)/2
    A_w = (b_flat - Dh)*D_in

    # ===== 沸腾校验 =====
    ok, Q_boil = check_boiling(Q, A_evap, t_wick_max, T_v)
    if not ok:
        return {"status":"FAIL","reason":"沸腾极限不足"}

    # ===== 毛细反设计 =====
    def eq(vars):
        d, eps = vars
        sigma, mu, h_fg, _, _, _ = props(T_v)
        r_eff = (d/2)*np.sqrt((1-eps)**2/eps**3)
        K = (d**2*eps**3)/(150*(1-eps)**2)
        Qc = 2*sigma/r_eff * K*A_w/(mu*L*h_fg)
        return Qc - Q

    d0, eps0 = 100e-6, 0.55
    d, eps = fsolve(eq, [d0, eps0])

    # ===== 铜粉匹配 =====
    matches = match_copper_powder(d, eps)
    if not matches:
        return {"status":"FAIL","reason":"无匹配铜粉"}

    best = matches[0]

    # ===== 充液量 =====
    t_wick = 0.8*t_wick_max
    V_fill = eps*A_w*L*1.1
    m_fill = props(T_v)[3]*V_fill

    return {
        "status":"OK",
        "grade": best["grade"],
        "d50_um": best["d50_um"],
        "eps_range": best["eps_range"],
        "t_wick_mm": t_wick*1e3,
        "m_fill_g": m_fill*1e3,
        "Q_boil_W": Q_boil
    }