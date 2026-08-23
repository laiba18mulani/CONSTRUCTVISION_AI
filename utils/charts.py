import plotly.graph_objects as go
import numpy as np

DARK_THEME = dict(
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(10, 23, 40, 0.4)',
    font=dict(color='#94A3B8', family='Plus Jakarta Sans, sans-serif', size=11),
    margin=dict(l=30, r=20, t=20, b=30),
    xaxis=dict(gridcolor='rgba(0, 200, 255, 0.08)', zerolinecolor='rgba(0, 200, 255, 0.15)'),
    yaxis=dict(gridcolor='rgba(0, 200, 255, 0.08)', zerolinecolor='rgba(0, 200, 255, 0.15)'),
)

def create_sparkline(y_data, color="#00C8FF"):
    """Generates a micro-sparkline plot for KPI cards."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=y_data,
        mode='lines',
        line=dict(color=color, width=2),
        hoverinfo='none'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        height=32
    )
    return fig

def create_gradient_area_chart(x, y, title="Structural Strain Trend (με)"):
    """Creates a line chart with a smooth gradient fill under the curve."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        name='Strain',
        line=dict(color='#00C8FF', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(0, 200, 255, 0.08)',
        hovertemplate='<b>Time:</b> %{x}<br><b>Strain:</b> %{y:.1f} με<extra></extra>'
    ))
    
    fig.update_layout(
        **DARK_THEME,
        title=dict(text=title, font=dict(color='#F5F7FA', size=13)),
        height=240,
        showlegend=False
    )
    return fig