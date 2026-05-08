import numpy as np
from copper_powder import match_copper_powder
from boiling import check_boiling

def design_engine(inputs):
    # 几何
    if "D_out" not in inputs:
    st.warning("缺少 'D_out' 参数，将使用默认值 8.0 mm") 
    D_out = 8.0  
else:
    D_out = inputs["D_out"]
    t_wall = inputs["t_wall"]
    b_flat = inputs["b_flat"]
    L = inputs["L"]

    D_in = D_out - 2*t_wall
    a, b = D_in, b_flat
    Dh = 2*a*b/(a+b)
    t_wick_max = (b - Dh)/2
    A_w = (b - Dh)*a

    # 沸腾校验
    ok, Q_boil = check_boiling(
        inputs["Q"], inputs["A_evap"],
        t_wick_max, inputs["T_v"]
    )
    if not ok:
        return {"status": "FAIL", "reason": "沸腾极限不足"}

    # 毛细反设计（简化）
    d_req = 100e-6
    eps_req = 0.56

    matches = match_copper_powder(d_req, eps_req)
    if not matches:
        return {"status": "FAIL", "reason": "无匹配铜粉"}

    best = matches[0]

    return {
        "status": "OK",
        "grade": best["grade"],
        "d50_um": best["d50_um"],
        "eps_range": best["eps_range"],
        "t_wick_mm": t_wick_max*1e3,
        "Q_boil_W": Q_boil
    }
