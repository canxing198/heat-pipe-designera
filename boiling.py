def check_boiling(Q, A_evap, t_wick, T_v):
    """
    Simple boiling limit check.
    Returns: (ok: bool, Q_boil: float)
    """
    # Simplified model: Assume a max heat flux based on wick thickness
    # This is a placeholder model for demonstration
    q_max = 50e4  # W/m² (example value)
    Q_boil = q_max * A_evap
    
    # Add a safety margin
    ok = Q < Q_boil * 0.8
    
    return ok, Q_boil
