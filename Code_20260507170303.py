import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="热管参数设计", layout="wide")
st.title("🌡️ 热管参数设计与仿真系统")

st.sidebar.header("热管参数")

Q = st.sidebar.number_input("功率 Q (W)", 10.0, 1000.0, 200.0)
Le = st.sidebar.number_input("蒸发段长度 Le (mm)", 10.0, 300.0, 100.0)
La = st.sidebar.number_input("绝热段长度 La (mm)", 0.0, 300.0, 50.0)
Lc = st.sidebar.number_input("冷凝段长度 Lc (mm)", 10.0, 300.0, 100.0)
T = st.sidebar.number_input("工作温度 (℃)", 20.0, 150.0, 80.0)

st.sidebar.header("吸液芯参数")
wick_type = st.sidebar.selectbox("芯型", ["丝网"])

wire_d = st.sidebar.number_input("丝径 (mm)", 0.05, 0.5, 0.1)
mesh = st.sidebar.number_input("目数", 50, 200, 100)

r_eff = 0.0254 / mesh / 2
Q_max = 300  # 占位

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 计算结果")
    st.metric("最大传热能力 Qmax", f"{Q_max:.1f} W")
    if Q < Q_max:
        st.success("✅ 设计安全")
    else:
        st.error("⚠️ 超过极限")

with col2:
    st.subheader("📈 温度分布")
    x = [0, Le, Le+La, Le+La+Lc]
    Tv = [T, T-2, T-3, T-5]
    fig, ax = plt.subplots()
    ax.plot(x, Tv, marker="o")
    ax.set_xlabel("长度 (mm)")
    ax.set_ylabel("温度 (℃)")
    st.pyplot(fig)
