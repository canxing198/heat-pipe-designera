def check_boiling(Q, A_evap, t_wick_max, T_v):
    """
    简化沸腾极限校验
    """
    q_max = 80e4  # W/m²
    q_actual = Q / A_evap
    ok = q_actual < q_max
    return ok, q_max
