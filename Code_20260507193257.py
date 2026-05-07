import numpy as np
import plotly.graph_objects as go
from limits import allowed_power

def process_window(params_template):
    fill = np.linspace(0.6, 1.2, 25)
    vac = np.linspace(10, 1000, 25)
    FF, VV = np.meshgrid(fill, vac)

    Q = np.zeros_like(FF)

    for i in range(FF.shape[0]):
        for j in range(FF.shape[1]):
            p = params_template.copy()
            p["cap"]["fill"] = FF[i, j]
            p["cap"]["vac"] = VV[i, j]
            Q[i, j], _, _, _ = allowed_power(p)

    fig = go.Figure(
        go.Surface(x=FF, y=VV, z=Q, colorscale="Viridis")
    )
    fig.update_layout(
        title="热管三维工艺窗口",
        scene=dict(
            xaxis_title="充液系数",
            yaxis_title="真空度 (Pa)",
            zaxis_title="Qmax (W)"
        )
    )
    return fig
