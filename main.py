import streamlit as st
from limits import flattened_geometry
from window import process_window
from database import init_db, save, load_df

st.set_page_config(page_title="热管研发 Web 平台", layout="wide")
st.title("🏭 热管研发 Web 平台")

init_db()

# ===== 输入 =====
st.sidebar.header("铜粉")
d = st.sidebar.slider("粒径 (μm)", 50, 250, 100) * 1e-6
eps = st.sidebar.slider("孔隙率 (%)", 45, 65, 55) / 100

st.sidebar.header("打扁 & 长度")
D_out = st.sidebar.number_input("外径 Do (mm)", 4.0, 12.0, 8.0) * 1e-3
t_wall = st.sidebar.number_input("壁厚 (mm)", 0.2, 1.0, 0.4) * 1e-3
b_flat = st.sidebar.number_input("打扁厚度 (mm)", 1.0, 6.0, 3.0) * 1e-3
L_eff = st.sidebar.number_input("有效长度 (mm)", 50.0, 800.0, 300.0) * 1e-3

# ===== 参数组装 =====
params = {
    "cap": dict(
        d=d, eps=eps, A_w=2e-6, L_eff=L_eff,
        sigma=0.058, mu=2.82e-4, h_fg=2.26e6,
        D_out=D_out, t_wall=t_wall, b_flat=b_flat
    ),
    "boil": dict(
        L_e=0.3*L_eff, k_eff=10, T_v=350,
        h_fg=2.26e6, rho_v=0.2,
        r_i=4e-3, r_w=3.5e-3, delta_T_eb=10
    )
}

# ===== 计算 =====
Q_allow, Qc, Qb, Qv = allowed_power(params)
st.success(f"✅ 允许最大功率：{Q_allow:.1f} W")

# ===== 三维窗口 =====
st.plotly_chart(process_window(params), use_container_width=True)

# ===== 数据库 =====
if st.button("💾 保存实验"):
    save((
        "Cu", d*1e6, eps*100,
        D_out*1e3, b_flat*1e3, L_eff*1e3,
        Qc, Qb, Qv, Q_allow,
        "OK" if Q_allow > 50 else "FAIL"
    ))

st.dataframe(load_df())
