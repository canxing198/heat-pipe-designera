import streamlit as st
from design import design_engine
from window import create_process_window
from excel_export import export_excel

st.set_page_config(page_title="热管研发 Web 平台", layout="wide")
st.title("🏭 热管研发 Web 平台")

with st.sidebar:
    st.header("基础设计参数")

    Q = st.number_input("目标功率 Q (W)", 10.0, 500.0, 100.0)
    L_total = st.number_input("热管总长 L (mm)", 50.0, 800.0, 300.0) * 1e-3
    L_cond = st.number_input("散热长度 L_cond (mm)", 20.0, 600.0, 150.0) * 1e-3

    D_out = st.number_input("外径 D_out (mm)", 4.0, 12.0, 8.0) * 1e-3
    b_flat = st.number_input("打扁厚度 (mm)", 1.0, 6.0, 3.0) * 1e-3
    A_evap = st.number_input("加热面积 (mm²)", 10.0, 500.0, 100.0) * 1e-6
    T_v = st.number_input("工作温度 (℃)", 20.0, 120.0, 60.0)

    inputs = dict(
        Q=Q,
        L=L_total,
        L_cond=L_cond,
        D_out=D_out,
        b_flat=b_flat,
        A_evap=A_evap,
        T_v=T_v,
        t_wall=0.4e-3
    )

    if st.button("🚀 开始设计"):
        with st.spinner("计算中..."):
            res = design_engine(inputs)
            st.session_state.res = res

if "res" in st.session_state:
    res = st.session_state.res
    if res["status"] == "OK":
        st.success("✅ 设计成功")
        st.json(res)
        if st.button("📥 导出 Excel"):
            export_excel(res)
    else:
        st.error(f"❌ 设计失败: {res['reason']}")
        st.json(res)

create_process_window(inputs)
