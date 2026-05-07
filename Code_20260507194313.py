import numpy as np

def flattened_geometry(D_out, t_wall, b_flat):
    D_in = D_out - 2 * t_wall
    a = D_in
    b = b_flat

    Dh = 2 * a * b / (a + b)
    t_wick = (b - Dh) / 2
    A_flow = a * b

    return Dh, t_wick, A_flow
