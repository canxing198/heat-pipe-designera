import numpy as np
import plotly.graph_objects as go

def create_process_window(inputs):
    fill_range = np.linspace(0.6,1.2,25)
    vac_range = np.linspace(10,1000,25)
    FF, VV = np.meshgrid(fill_range, vac_range)

    Q_surface = 100*(1-np.exp(-(FF-0.6)**2/0.1))*(1-VV/1500)

    fig = go.Figure(data=[
        go.Surface(x=FF, y=VV, z=Q_surface, colorscale="Viridis")
    ])
    fig.update_layout(
        title="热管三维工艺窗口",
        scene=dict(
            xaxis_title="充液系数",
            yaxis_title="真空度 (Pa)",
            zaxis_title="Qmax (W)"
        )
    )
    return fig
