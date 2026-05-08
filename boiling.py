# boiling.py

def check_boiling(q_prime, A_evap, T_v, P_vac, h_fg):
    """
    校验热管的沸腾极限
    """
    # 这里先返回一个模拟数据，后续再补全真实逻辑
    print(f"正在校验沸腾极限：热流密度={q_prime}, 蒸发面积={A_evap}")
    
    # 模拟返回的结果
    result = {
        "is_ok": True,
        "message": "沸腾极限校验通过 (Mock)",
        "q_max": 10000  # 假设的极限值
    }
    
    return result