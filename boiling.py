def check_boiling(Q, A_evap, t_wick, T_v):
    k_eff = 10
    h_fg = 2.26e6
    rho_v = 0.2
    delta_T = 10

    q_max = k_eff*(T_v+273)*delta_T/(h_fg*rho_v*t_wick)
    Q_boil = q_max * A_evap

    return Q_boil > Q, Q_boil