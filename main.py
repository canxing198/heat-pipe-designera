import streamlit as st
from window import create_process_window
from design import design_engine

st.set_page_config(page_title="热管研发 Web 平台", layout="wide")
st.title("🏭 热管研发 Web 平台")

# ===== 基础输入 =====
with st.sidebar:
    st.header("基础设计参数")
    Q = st.number_input("目标功率 Q (W)", 10.0, 500.0, 100.0)
    L = st.number_input("长度 L (mm)", 50.0, 800.0, 300.0) * 1e-3
    b_flat = st.number_input("打扁厚度 (mm)", 1.0, 6.0, 3.0) * 1e-3
    # ... 其他参数 ...

# 收集基础输入
base_inputs = {
    "Q": Q,
    "L": L,
    "b_flat": b_flat,
    # ... 其他参数 ...
}

# ===== Tab 布局 =====
tab1, tab2 = st.tabs(["📐 参数设计", "📊 工艺窗口"])

with tab1:
    st.subheader("单点设计")
    if st.button("🚀 开始设计"):
        res = design_engine(base_inputs)
        st.json(res)

with tab2:
    st.subheader("三维工艺窗口（充液 × 真空）")
    st.info("生成此图可能需要几秒钟，请耐心等待...")

    fig = create_process_window(base_inputs)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### 🧠 工程解读
    - **高功率区**（暖色区域）：推荐工艺区间
    - **边缘陡峭区**：工艺容错率低，慎用
    - **塌陷区（蓝色）**：干烧或液堵风险区
    """)
