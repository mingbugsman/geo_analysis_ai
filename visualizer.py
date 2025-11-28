
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import HeatMap

from src import constants as c

TEMPLATE = "plotly_white"

def create_flexible_time_series(df_grouped, x_col, x_label, y1_col=c.COL_TEMP, y2_col=c.COL_NDVI):
    """1. Ve bieu do Time Series linh hoat 2 truc"""
    if df_grouped.empty:
        return go.Figure()  # Tra ve bieu do rong neu du lieu khong hop le
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Truc 1: Nhiet do (hoac y1_col)
    fig.add_trace(
        go.Scatter(x=df_grouped[x_col], y=df_grouped[y1_col], name=f"{y1_col} (°C)", mode='lines+markers', line=dict(color='#d32f2f', width=3)),
        secondary_y=False
    )
    # Truc 2: NDVI (hoac y2_col)
    fig.add_trace(
        go.Bar(x=df_grouped[x_col], y=df_grouped[y2_col], name=f"{y2_col} (Cay xanh)", marker_color='rgba(46, 125, 50, 0.6)'),
        secondary_y=True
    )
    fig.update_layout(
        title=f"<b>BIEN DONG THEO: {x_label.upper()}</b>",
        template=TEMPLATE,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1)
    )
    fig.update_xaxes(type='category', title_text=x_label)
    fig.update_yaxes(title_text=f"{y1_col} (°C)", secondary_y=False)
    fig.update_yaxes(title_text=y2_col, secondary_y=True, range=[0, 1])
    return fig

def create_enhanced_scatter(df: pd.DataFrame, x_col=c.COL_NDVI, y_col=c.COL_TEMP):
    """2. Ve bieu do tuong quan (Scatter)"""
    if df.empty:
        return px.scatter()
    
    fig = px.scatter(
        df, x=x_col, y=y_col, color=y_col, size=y_col,
        hover_data={c.COL_LON: ":.4f", c.COL_LAT: ":.4f", x_col: ":.2f", y_col: ":.2f"},
        trendline="ols", trendline_color_override="red",
        color_continuous_scale="RdYlBu_r",
        title=f"<b>TUONG QUAN: {x_col.upper()} & {y_col.upper()}</b>"
    )
    fig.update_layout(template=TEMPLATE, xaxis_title=x_col, yaxis_title=f"{y_col} (°C)")
    return fig

def create_advanced_distribution(df: pd.DataFrame, column: str, label_vn: str):
    """3. Ve bieu do phan phoi (Violin/Boxplot)"""
    if df.empty:
        return px.violin()
    
    fig = px.violin(
        df, y=column, box=True, points="all",
        color_discrete_sequence=['teal'],
        title=f"<b>PHAN PHOI MAT DO DU LIEU: {label_vn.upper()}</b>"
    )
    fig.update_layout(template=TEMPLATE, yaxis_title=label_vn, xaxis_title="Mat do")
    return fig

def create_3d_scatter(df: pd.DataFrame):
    """4. Ve bieu do 3D"""
    if df.empty:
        return px.scatter_3d()
    
    fig = px.scatter_3d(
        df, x=c.COL_LON, y=c.COL_LAT, z=c.COL_TEMP,
        color=c.COL_TEMP, color_continuous_scale="Turbo",
        title="<b>KHONG GIAN NHIET DO 3D</b>"
    )
    fig.update_layout(template=TEMPLATE, margin=dict(l=0, r=0, b=0, t=40),
                      scene=dict(xaxis_title='Kinh do', yaxis_title='Vi do', zaxis_title='Nhiet do'))
    return fig

def create_interactive_map(df: pd.DataFrame) -> folium.Map:
    """5. Ve ban do voi Popup HTML"""
    if df.empty:
        return folium.Map()
    
    center_lat = df[c.COL_LAT].mean()
    center_lon = df[c.COL_LON].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="CartoDB positron")
    # Heatmap
    heat_data = [[row[c.COL_LAT], row[c.COL_LON], row[c.COL_TEMP]] for index, row in df.iterrows()]
    HeatMap(heat_data, name="Ban do Nhiet", radius=15, blur=12).add_to(m)
    # Markers
    top_points = df.nlargest(100, c.COL_TEMP)
    for i, row in top_points.iterrows():
        lat_str = f"{row[c.COL_LAT]:.4f}"
        lon_str = f"{row[c.COL_LON]:.4f}"
        popup_html = f"""
        <div style="font-family: 'Segoe UI', sans-serif; width: 200px; padding: 5px;">
        <div style="background-color: #d32f2f; color: white; padding: 8px; border-radius: 5px 5px 0 0;">
        <h5 style="margin: 0; font-weight: bold;">Diem do: {lat_str[:6]}, {lon_str[:6]}...</h5>
        </div>
        <div style="border: 1px solid #ddd; border-top: none; padding: 10px; border-radius: 0 0 5px 5px; background: white;">
        <b style="color: #d32f2f; font-size: 16px;">Temp: {row[c.COL_TEMP]:.2f} °C</b><br>
        <hr style="margin: 5px 0;">
        <span style="color: #2e7d32;"><b>NDVI:</b> {row[c.COL_NDVI]:.2f}</span><br>
        <span style="color: #1976d2;"><b>TDVI:</b> {row[c.COL_TDVI]:.2f}</span><br>
        <i style="font-size: 11px; color: gray;">(Toa do day du: {lat_str}, {lon_str})</i>
        </div>
        </div>
        """
        folium.CircleMarker(
            location=[row[c.COL_LAT], row[c.COL_LON]],
            radius=8, color='#d32f2f', fill=True, fill_color='#ff7961', fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"Temp: {row[c.COL_TEMP]:.1f}°C | Click xem chi tiet"
        ).add_to(m)
    return m

def create_quality_pie_chart(df: pd.DataFrame):
    """6. Ve bieu do Tron phan loai chat luong"""
    if df.empty:
        return px.pie()
    
    def classify(temp):
        if temp < 30: return "Mat me (Ly tuong)"
        elif temp < 35: return "Binh thuong"
        else: return "Nong (Canh bao)"
    
    df_class = df.copy()
    df_class['Phan loai'] = df_class[c.COL_TEMP].apply(classify)
    df_pie = df_class['Phan loai'].value_counts().reset_index()
    df_pie.columns = ['Loai', 'So luong']
    fig = px.pie(
        df_pie, values='So luong', names='Loai',
        title="<b>TI LE CAC VUNG NHIET DO</b>",
        color='Loai', color_discrete_map={
            "Mat me (Ly tuong)": "#2e7d32",
            "Binh thuong": "#fbc02d",
            "Nong (Canh bao)": "#d32f2f"
        }, hole=0.4
    )
    fig.update_layout(template=TEMPLATE)
    return fig

# Cac ham moi them de toi uu hoa

def create_correlation_heatmap(df: pd.DataFrame, columns=[c.COL_TEMP, c.COL_NDVI, c.COL_TDVI]):
    """7. Ve heatmap tuong quan giua cac chi so"""
    if df.empty or len(columns) < 2:
        return go.Figure()
    
    corr = df[columns].corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=columns,
        y=columns,
        colorscale='RdBu',
        zmin=-1, zmax=1,
        text=corr.values.round(2),
        hovertemplate='%{x} vs %{y}: %{z:.2f}<extra></extra>'
    ))
    fig.update_layout(
        title="<b>HEATMAP TUONG QUAN CAC CHI SO</b>",
        template=TEMPLATE
    )
    return fig

def create_histogram_distribution(df: pd.DataFrame, column: str, label_vn: str, bins=30):
    """8. Ve histogram phan phoi chi tiet"""
    if df.empty:
        return px.histogram()
    
    fig = px.histogram(
        df, x=column, nbins=bins,
        color_discrete_sequence=['#1f77b4'],
        title=f"<b>HISTOGRAM PHAN PHOI: {label_vn.upper()}</b>"
    )
    fig.update_layout(template=TEMPLATE, xaxis_title=label_vn, yaxis_title="So luong")
    return fig

def create_boxplot_comparison(df: pd.DataFrame, y_col=c.COL_TEMP, group_col='Month', label_vn="Nhiet do theo thang"):
    """9. Ve boxplot so sanh giua cac nhom"""
    if df.empty or group_col not in df.columns:
        return px.box()
    
    fig = px.box(
        df, x=group_col, y=y_col,
        color=group_col,
        title=f"<b>SO SANH PHAN PHOI: {label_vn.upper()}</b>"
    )
    fig.update_layout(template=TEMPLATE, xaxis_title=group_col, yaxis_title=y_col)
    return fig

def create_contour_map(df: pd.DataFrame):
    """10. Ve contour plot 2D cho nhiet do tren toa do"""
    if df.empty:
        return go.Figure()
    
    fig = go.Figure(data=go.Contour(
        z=df[c.COL_TEMP],
        x=df[c.COL_LON],
        y=df[c.COL_LAT],
        colorscale="Hot",
        contours=dict(showlabels=True, labelfont=dict(size=12, color="white"))
    ))
    fig.update_layout(
        title="<b>CONTOUR MAP NHIET DO KHONG GIAN</b>",
        template=TEMPLATE,
        xaxis_title='Kinh do', yaxis_title='Vi do'
    )
    return fig

def create_pairplot(df: pd.DataFrame, columns=[c.COL_TEMP, c.COL_NDVI, c.COL_TDVI]):
    """11. Ve pairplot de kham pha moi quan he"""
    if df.empty or len(columns) < 2:
        return px.scatter_matrix()
    
    fig = px.scatter_matrix(
        df[columns],
        dimensions=columns,
        color=c.COL_TEMP,
        title="<b>PAIRPLOT KHAM PHA DU LIEU</b>"
    )
    fig.update_traces(diagonal_visible=False)
    fig.update_layout(template=TEMPLATE)
    return fig

def create_bar_comparison(df: pd.DataFrame, group_col='Month', y_col=c.COL_TEMP, label_vn="Trung binh nhiet do theo thang"):
    """12. Ve bar chart so sanh trung binh giua cac nhom"""
    if df.empty or group_col not in df.columns:
        return px.bar()
    
    df_group = df.groupby(group_col)[y_col].mean().reset_index()
    fig = px.bar(
        df_group, x=group_col, y=y_col,
        color=y_col, color_continuous_scale="RdYlBu_r",
        title=f"<b>SO SANH TRUNG BINH: {label_vn.upper()}</b>"
    )
    fig.update_layout(template=TEMPLATE, xaxis_title=group_col, yaxis_title=y_col)
    return fig

def create_tdvi_time_series(df_grouped, x_col, x_label):
    """13. Ve time series rieng cho TDVI"""
    if df_grouped.empty:
        return go.Figure()
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=df_grouped[x_col], y=df_grouped[c.COL_TDVI], name="TDVI (Do am dat)", mode='lines+markers', line=dict(color='#1976d2', width=3))
    )
    fig.update_layout(
        title=f"<b>BIEN DONG TDVI THEO: {x_label.upper()}</b>",
        template=TEMPLATE,
        hovermode="x unified"
    )
    fig.update_xaxes(type='category', title_text=x_label)
    fig.update_yaxes(title_text="TDVI", range=[0, 1])
    return fig