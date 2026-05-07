import numpy as np
from geometry import flattened_geometry

def capillary_limit(
    d, eps, A_w, L_eff,
    sigma, mu, h_fg,
    D_out, t_wall, b_flat
):
    _, t_wick, _ = flattened_geometry(D_out, t_wall, b_flat)

    r_eff = (d / 2) * np.sqrt((1 - eps)**2 / eps**3) * (t_wick / (d / 2))
    K = (d**2 * eps**3) / (150 * (1 - eps)**2)

    return 2 * sigma / r_eff * K * A_w / (mu * L_eff) / h_fg


def boiling_limit(L_e, k_eff, T_v, h_fg, rho_v, r_i, r_w, delta_T_eb):
    return np.pi * L_e * k_eff * T_v / (
        h_fg * rho_v * np.log(r_i / r_w)
    ) * delta_T_eb


def viscous_limit():
    return 300


def allowed_power(params):
    Qc = capillary_limit(**params["cap"])
    Qb = boiling_limit(**params["boil"])
    Qv = viscous_limit()
    return min(Qc, Qb, Qv), Qc, Qb, Qv
