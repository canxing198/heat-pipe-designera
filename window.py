import numpy as np
import plotly.graph_objects as go
from design import design_engine  # 复用你的设计引擎

def create_process_window(inputs):
    """
    生成三维工艺窗口
    inputs: 来自 Web 界面的基础输入参数
    """

    # ===== 参数扫描范围 =====
    fill_range = np.linspace(0.6, 1.2, 25)   # 充液系数
    vac_range = np.linspace(10, 1000, 25)    # 真空度 Pa

    FF, VV = np.meshgrid(fill_range, vac_range)
    Q_surface = np.zeros_like(FF)

    # ===== 遍历计算 =====
    for i in range(FF.shape[0]):
        for j in range(FF.shape[1]):

            # 构造临时输入参数
            temp_inputs = inputs.copy()
            temp_inputs["fill_ratio"] = FF[i, j]
            temp_inputs["vacuum"] = VV[i, j]

            # 调用设计引擎，获取功率
            # 这里假设 design_engine 返回 Q_allow
            try:
                res = design_engine(temp_inputs)
                Q_surface[i, j] = res.get("Q_allow", 0)
            except:
                Q_surface[i, j] = 0

    # ===== Plotly 三维曲面 =====
    fig = go.Figure(data=[
        go.Surface(
            x=FF,
            y=VV,
            z=Q_surface,
            colorscale="Viridis",
            contours={
                "z": {"show": True, "start": 20, "end": 200, "size": 20}
            }
        )
    ])

    fig.update_layout(
        title="热管三维工艺窗口",
        scene=dict(
            xaxis_title="充液系数",
            yaxis_title="真空度 (Pa)",
            zaxis_title="Qmax (W)"
        ),
        autosize=True
    )

    return fig