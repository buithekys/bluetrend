import os
import folium
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="BlueTrend — Southeast Asia Multi-Basin Explorer",
    page_icon="🌊",
    layout="wide",
)

TIMESERIES_PATH = "data/processed/tabular/timeseries_all.parquet"
TREND_PATH = "outputs/statistics/trend_results_all.csv"
CATALOG_PATH = "metadata/data_catalog.csv"

# Bounding boxes [west, south, east, north] extracted from NASA Giovanni CSV headers
REGION_BBOXES = {
    "basin_01": [94.5, 16.0, 98.5, 22.0],
    "basin_02": [100.5, -1.0, 103.5, 4.5],
    "basin_03": [109.5, -2.5, 117.5, 1.5],
    "basin_04": [100.0, 8.5, 108.0, 22.0],
    "basin_05": [107.5, 13.5, 109.3, 16.0],
    "basin_06": [116.5, 5.0, 122.5, 18.5],
    "basin_07": [102.5, 19.5, 108.0, 23.5],
    "marine_01": [95.0, 6.5, 98.3, 15.5],
    "marine_02": [118.0, 2.0, 125.5, 13.5],
    "marine_03": [108.3, 11.8, 109.8, 17.0],
    "marine_04": [106.0, -9.5, 134.0, 0.5],
    "marine_05": [97.5, 1.0, 103.5, 6.0],
    "marine_06": [99.0, 6.5, 105.5, 13.5],
    "marine_07": [106.2, 17.8, 109.5, 21.2],
    "region_sea": [92.0, -11.0, 141.0, 28.5],
}


@st.cache_data
def load_data():
    ts = pd.read_parquet(TIMESERIES_PATH) if os.path.exists(TIMESERIES_PATH) else pd.DataFrame()
    trends = pd.read_csv(TREND_PATH) if os.path.exists(TREND_PATH) else pd.DataFrame()
    catalog = pd.read_csv(CATALOG_PATH) if os.path.exists(CATALOG_PATH) else pd.DataFrame()
    return ts, trends, catalog


def generate_insight(row: pd.Series) -> str:
    """Generate a scientifically accurate, non-causal insight from trend statistics."""
    name = row["basin_name"]
    var = row["variable_id"]
    slope = row["sen_slope"]
    units = row["slope_units"]
    p = row["p_value"]
    sig = row["significance"]

    if sig == "insufficient_data":
        return f"**{name}** ({var}): Dữ liệu không đủ để kiểm định xu hướng ({int(row['n_observations'])} quan sát)."
    if sig == "significant":
        direction = "tăng" if slope > 0 else "giảm"
        return (
            f"**{name}** ({var}): Có bằng chứng thống kê cho thấy xu hướng **{direction}** "
            f"(Sen's slope = `{slope:+.4f} {units}`, `p = {p:.5f} < 0.05`). "
            f"Lưu ý: đây là xu hướng đơn điệu giai đoạn 2018–2024, chưa tách mùa vụ."
        )
    return (
        f"**{name}** ({var}): Chưa phát hiện xu hướng có ý nghĩa thống kê "
        f"(Sen's slope = `{slope:+.4f} {units}`, `p = {p:.4f} >= 0.05`). "
        f"Không đồng nghĩa chắc chắn không thay đổi."
    )


def build_interactive_map(trend_df: pd.DataFrame, layer_filter: str) -> folium.Map:
    m = folium.Map(location=[8.0, 112.0], zoom_start=4, tiles="OpenStreetMap")

    if layer_filter == "River Basins (Precipitation)":
        sub = trend_df[trend_df["region_type"] == "river_basin"]
    elif layer_filter == "Marine Regions (Kd490)":
        sub = trend_df[trend_df["region_type"] == "marine_region"]
    else:
        sub = trend_df[trend_df["region_type"].isin(["river_basin", "marine_region"])]

    for _, row in sub.iterrows():
        bid = row["basin_id"]
        bbox = REGION_BBOXES.get(bid)
        if not bbox:
            continue
        west, south, east, north = bbox
        is_sig = row["significance"] == "significant"
        is_river = row["region_type"] == "river_basin"

        if is_sig:
            color = "#d62728" if row["sen_slope"] > 0 else "#1f77b4"
            fill_opacity = 0.45
        else:
            color = "#2ca02c" if is_river else "#7f7f7f"
            fill_opacity = 0.20

        popup_html = f"""
        <div style="font-family: sans-serif; width: 260px;">
            <h4 style="margin:0 0 6px 0;">{row['basin_name']}</h4>
            <b>ID:</b> {bid} ({row['region_type']})<br>
            <b>Variable:</b> {row['variable_id']}<br>
            <b>Sen's Slope:</b> {row['sen_slope']:+.4f} {row['slope_units']}<br>
            <b>p-value:</b> {row['p_value']:.5f}<br>
            <b>Significance:</b> <b>{row['significance']}</b><br>
            <hr style="margin:6px 0;">
            <small>Approximate bounding box (2018–2024 monthly)</small>
        </div>
        """

        folium.Rectangle(
            bounds=[[south, west], [north, east]],
            color=color,
            weight=2.5 if is_sig else 1.5,
            fill=True,
            fill_color=color,
            fill_opacity=fill_opacity,
            tooltip=f"{row['basin_name']} | {row['variable_id']} | {row['significance']} (p={row['p_value']:.4f})",
            popup=folium.Popup(popup_html, max_width=280),
        ).add_to(m)

    return m


ts_df, trend_df, catalog_df = load_data()

st.sidebar.title("🌊 BlueTrend")
st.sidebar.caption("Southeast Asia Multi-Basin Earth System Trend Explorer")
page = st.sidebar.radio(
    "Navigation",
    [
        "1. Interactive Map & Insights",
        "2. Basin Explorer (Time Series)",
        "3. Trend Analysis Table",
        "4. Cross-Basin Comparison",
        "5. Data Provenance & Methodology",
    ],
)

if ts_df.empty or trend_df.empty:
    st.error("Processed data not found. Run `loader.py` and `trend.py` first.")
    st.stop()

if page == "1. Interactive Map & Insights":
    st.title("Interactive Multi-Basin & Marine Trend Map (2018–2024)")
    st.caption(
        "Màu đỏ: xu hướng tăng có ý nghĩa thống kê (p < 0.05) | "
        "Màu xanh lá / xám: chưa có ý nghĩa thống kê. Click vào từng vùng để xem chi tiết."
    )

    layer_choice = st.radio(
        "Hiển thị lớp dữ liệu:",
        ["All (Basins + Marine)", "River Basins (Precipitation)", "Marine Regions (Kd490)"],
        horizontal=True,
    )

    fmap = build_interactive_map(trend_df, layer_choice)
    components.html(fmap._repr_html_(), height=520)

    st.subheader("Key Statistical Insights (2018–2024)")
    sig_df = trend_df[trend_df["significance"] == "significant"]
    for _, r in sig_df.iterrows():
        st.success(generate_insight(r))

    st.warning(
        "Lưu ý khoa học: Các vùng hiện đang hiển thị theo khung chữ nhật (bounding box) từ NASA Giovanni "
        "do chưa có polygon thủy văn chính thức. Không suy diễn quan hệ nhân quả từ kết quả Mann-Kendall."
    )

elif page == "2. Basin Explorer (Time Series)":
    st.title("Basin & Region Explorer")
    regions = trend_df[["basin_id", "basin_name", "region_type"]].drop_duplicates()
    selected_name = st.selectbox("Select Basin / Region", regions["basin_name"].tolist())
    sub_ts = ts_df[ts_df["basin_name"] == selected_name].sort_values("time").copy()
    sub_trend = trend_df[trend_df["basin_name"] == selected_name].iloc[0]

    st.info(generate_insight(sub_trend))

    var_id = sub_ts["variable_id"].iloc[0]
    units = sub_ts["units"].iloc[0]

    fig = px.line(
        sub_ts,
        x="time",
        y="value",
        markers=True,
        title=f"{selected_name} — {var_id} (Monthly Area-Averaged)",
        labels={"time": "Time (Monthly)", "value": f"{var_id} ({units})"},
    )

    # Add OLS trendline overlay
    t_num = (sub_ts["time"] - sub_ts["time"].iloc[0]).dt.days.to_numpy() / 365.25
    y_vals = sub_ts["value"].to_numpy(dtype=float)
    valid_mask = ~np.isnan(y_vals)
    if valid_mask.sum() >= 2:
        coeffs = np.polyfit(t_num[valid_mask], y_vals[valid_mask], 1)
        trend_y = np.polyval(coeffs, t_num)
        fig.add_trace(
            go.Scatter(
                x=sub_ts["time"],
                y=trend_y,
                mode="lines",
                name=f"OLS Trend ({sub_trend['slope']:+.3f} {units}/yr)",
                line=dict(dash="dash", color="red", width=2),
            )
        )

    st.plotly_chart(fig, use_container_width=True)

elif page == "3. Trend Analysis Table":
    st.title("Trend Analysis")
    var_filter = st.selectbox("Select Variable", sorted(trend_df["variable_id"].unique()))
    sub_trend = trend_df[trend_df["variable_id"] == var_filter]
    st.dataframe(
        sub_trend[
            [
                "basin_id",
                "basin_name",
                "n_observations",
                "slope",
                "sen_slope",
                "slope_units",
                "p_value",
                "alpha",
                "trend_direction",
                "significance",
            ]
        ],
        use_container_width=True,
    )

elif page == "4. Cross-Basin Comparison":
    st.title("Cross-Basin Comparison")
    var_choice = st.selectbox("Select Variable to Compare", sorted(trend_df["variable_id"].unique()))
    comp_df = trend_df[trend_df["variable_id"] == var_choice].copy()
    fig = px.bar(
        comp_df,
        x="basin_name",
        y="sen_slope",
        color="significance",
        title=f"Sen's Slope Comparison — {var_choice}",
        labels={"basin_name": "Basin / Region", "sen_slope": f"Sen's Slope ({comp_df['slope_units'].iloc[0]})"},
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "5. Data Provenance & Methodology":
    st.title("Data Provenance & Methodology")
    st.markdown(
        """
        - **Precipitation:** NASA GPM IMERG Final Run (`GPM_3IMERGM_07`), monthly, `mm/hr`, 2018-01 to 2024-12.
        - **Kd490:** NASA MODIS-Aqua (`MODISA_L3m_KD_Mo_4km_R2022_0`), monthly, `m^-1`, 2018-01 to 2024-12.
        - **Statistical Methods:** Mann-Kendall test (`alpha = 0.05`), Sen's slope, and OLS linear regression.
        """
    )
    if not catalog_df.empty:
        st.dataframe(catalog_df, use_container_width=True)
