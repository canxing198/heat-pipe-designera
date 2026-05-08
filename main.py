import streamlit as st
from design import design_engine
from window import create_process_window
from excel_export import export_excel

st.set_page_config(page_title="热管研发 Web 平台", layout="wide")
st.title("🏭 热管研发 Web 平台")

with st.sidebar:
    st.header("基础设计参数")
    Q = st.number_input("目标功率 Q (W)", 10.0, 500.0, 100.0)
    L = st.number_input("长度 L (mm)", 50.0, 800.0, 300.0) * 1e-3
    D_out = st.number_input("外径 D_out (mm)", 4.0, 12.0, 8.0) * 1e-3
    b_flat = st.number_input("打扁厚度 (mm)", 1.0, 6.0, 3.0) * 1e-3
    A_evap = st.number_input("加热面积 (mm²)", 10.0, 500.0, 100.0) * 1e-6
    T_v = st.number_input("工作温度 (℃)", 20.0, 120.0, 60.0)

inputs = dict(
    Q=Q, L=L, D_out=D_out,
    b_flat=b_flat, A_evap=A_evap, T_v=T_v,
    t_wall=0.4e-3,
)

tab1, tab2 = st.tabs(["📐 参数设计", "📊 工艺窗口"])

with tab1:
if 'design_result' not in st.session_state:
    st.session_state.design_result = None

# 在“开始设计”按钮点击时，保存结果到 session_state
if st.button("🚀 开始设计"):
    res = design_engine(inputs)
    st.session_state.design_result = res  # 保存到 session_state

    if res and isinstance(res, dict) and res.get("status") == "OK":
        st.success("✅ 设计成功")
        st.json(res)
    else:
        st.error(f"❌ 设计失败: {res.get('reason', '未知错误')}" if res else "函数未返回数据")
        st.json(res)

# 在“导出 Excel”按钮点击时，从 session_state 中读取结果
if st.button("📤 导出 Excel 工艺卡"):
    if st.session_state.design_result:
        export_excel(st.session_state.design_result)
    else:
        st.warning("请先点击‘开始设计’")
                export_excel(res)

with tab2:
    st.subheader("三维工艺窗口")
    fig = create_process_window(inputs)
    st.plotly_chart(fig, use_container_width=True)
