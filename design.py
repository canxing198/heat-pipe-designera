import numpy as np
from scipy.optimize import fsolve
from copper_powder import match_copper_powder
from boiling import check_boiling

def props(T_C):
    T = T_C + 273.15
    return dict(
        sigma=0.058,
        mu=2.82e-4,
        h_fg=2.26e6,
        rho_l=1000,
        rho_v=0.2,
        k_eff=10
    )

def design_engine(inputs):
    D_out = inputs["D_out"]
    t_wall = inputs["t_wall"]
    b_flat = inputs["b_flat"]
    L = inputs["L"]
    L_cond = inputs["L_cond"]
    Q = inputs["Q"]
    A_evap = inputs["A_evap"]
    T_v = inputs["T_v"]

    # ===== Geometry =====
    D_in = D_out - 2*t_wall
    Dh = 2*D_in*b_flat/(D_in+b_flat)
    t_wick_max = (b_flat - Dh)/2
    A_w = (b_flat - Dh)*D_in

    # ===== Boiling Check =====
    ok, Q_boil = check_boiling(Q, A_evap, t_wick_max, T_v)
    if not ok:
        return {"status":"FAIL","reason":"沸腾极限不足"}

    # ===== Capillary Limit =====
    p = props(T_v)
def eq(vars):
    d, eps = vars
    
    # 1. 增加保护：限制 eps 范围，防止 math domain error
    if eps >= 1.0 or eps <= 0.0:
        return [1e9, 1e9] # 返回一个很大的错误值，迫使 fsolve 调整方向
        
    # 2. 计算 r_eff
    try:
        r_eff = (d/2) * np.sqrt((1-eps)**2 / eps**3)
    except:
        return [1e9, 1e9]

    # 3. 后面的 K 和 Qc 计算保持不变...
    K = (d**2 * (1-eps)**3) / (150 * (1-eps)**2) 
    # ... (此处省略中间代码)
    
    return Qc - Q

    d0, eps0 = 100e-6, 0.55
    d, eps = fsolve(eq, [d0, eps0])

    # ===== Copper Powder Match =====
    matches = match_copper_powder(d, eps)
    if not matches:
        return {"status":"FAIL","reason":"无匹配铜粉"}
    best = matches[0]

    # ===== Fill Mass =====
    t_wick = 0.8*t_wick_max
    V_fill = eps*A_w*L_cond*1.1
    m_fill = p["rho_l"]*V_fill

    return {
        "status":"OK",
        "grade": best.get("grade"),
        "d50_um": best.get("d50_um"),
        "eps": eps,
        "t_wick_mm": t_wick*1e3,
        "m_fill_g": m_fill*1e3,
        "Q_boil_W": Q_boil,
        "L_cond_mm": L_cond*1e3
    }
