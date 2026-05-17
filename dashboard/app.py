import sys
import os

# Allow imports from project root
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from etl.transform import transform_data

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SalesIQ — Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Dark luxury theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}

/* ── Main area background ── */
.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 50%, #0a0f15 100%);
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d18 0%, #0a0f1a 100%);
    border-right: 1px solid rgba(99, 202, 183, 0.15);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Syne', sans-serif;
    color: #63cab7;
}

/* ── Hero header ── */
.hero-header {
    background: linear-gradient(135deg, rgba(99,202,183,0.08) 0%, rgba(99,140,202,0.05) 100%);
    border: 1px solid rgba(99,202,183,0.2);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(99,202,183,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #63cab7, #638cca);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}
.hero-subtitle {
    font-size: 0.95rem;
    color: rgba(232,232,240,0.5);
    margin-top: 8px;
    font-weight: 300;
    letter-spacing: 0.5px;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,202,183,0.12);
    border: 1px solid rgba(99,202,183,0.3);
    color: #63cab7;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 12px;
}

/* ── KPI Cards ── */
.kpi-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 24px 28px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.kpi-card:hover { border-color: rgba(99,202,183,0.3); }
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 0 0 16px 16px;
}
.kpi-card.green::after  { background: linear-gradient(90deg, #63cab7, transparent); }
.kpi-card.blue::after   { background: linear-gradient(90deg, #638cca, transparent); }
.kpi-card.amber::after  { background: linear-gradient(90deg, #e8a838, transparent); }
.kpi-card.rose::after   { background: linear-gradient(90deg, #e86889, transparent); }

.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: rgba(232,232,240,0.45);
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #e8e8f0;
    line-height: 1;
}
.kpi-delta {
    font-size: 0.78rem;
    margin-top: 8px;
    font-weight: 500;
}
.kpi-delta.up   { color: #63cab7; }
.kpi-delta.down { color: #e86889; }

/* ── Section headers ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8e8f0;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}
.section-sub {
    font-size: 0.8rem;
    color: rgba(232,232,240,0.4);
    margin-bottom: 20px;
}

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,202,183,0.3), transparent);
    margin: 36px 0;
}

/* ── Status pill ── */
.pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.pill-success { background: rgba(99,202,183,0.15); color: #63cab7; }
.pill-warn    { background: rgba(232,168,56,0.15);  color: #e8a838; }

/* ── Selectbox & widgets ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
}
[data-testid="stSelectbox"] label {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    color: rgba(232,232,240,0.5) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(99,202,183,0.25) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06);
}

/* ── Buttons ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #63cab7, #638cca) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.8px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    transition: opacity 0.2s !important;
}
.stDownloadButton > button:hover { opacity: 0.85 !important; }

/* ── Success / info messages ── */
[data-testid="stSuccess"] {
    background: rgba(99,202,183,0.1) !important;
    border: 1px solid rgba(99,202,183,0.3) !important;
    border-radius: 10px !important;
    color: #63cab7 !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATABASE SETUP
# ─────────────────────────────────────────────
DB_PATH = os.path.join(
    os.path.dirname(__file__), "..", "database", "sales.db"
)
engine = create_engine(f"sqlite:///{DB_PATH}")


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def format_inr(value: float) -> str:
    """Format a number as Indian Rupee with lakh/crore notation."""
    if value >= 1_00_00_000:
        return f"₹{value/1_00_00_000:.2f} Cr"
    elif value >= 1_00_000:
        return f"₹{value/1_00_000:.2f} L"
    else:
        return f"₹{int(value):,}"


def load_data_from_db() -> pd.DataFrame:
    """Load sales table; return empty DataFrame with schema on failure."""
    try:
        df = pd.read_sql("SELECT * FROM sales", engine)
        # ── BUG FIX: if revenue column missing, compute it ──
        if "revenue" not in df.columns:
            if "quantity" in df.columns and "price" in df.columns:
                df = transform_data(df)
            else:
                st.error("⚠️ Database is missing required columns. Please run the ETL pipeline first (`python run_pipeline.py`) or upload a CSV below.")
                st.stop()
        return df
    except Exception:
        return pd.DataFrame()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 24px;'>
        <div style='font-family:Syne,sans-serif; font-size:1.3rem; font-weight:800;
                    background:linear-gradient(135deg,#63cab7,#638cca);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;'>
            SalesIQ
        </div>
        <div style='font-size:0.72rem; color:rgba(232,232,240,0.4);
                    letter-spacing:1.5px; text-transform:uppercase; margin-top:2px;'>
            Analytics Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Upload ──
    st.markdown("<div class='section-title' style='font-size:0.82rem;'>📂 Data Source</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload new CSV", type=["csv"], label_visibility="collapsed")

    if uploaded_file:
        raw_df = pd.read_csv(uploaded_file)
        # Auto-transform if revenue missing
        if "revenue" not in raw_df.columns:
            raw_df = transform_data(raw_df)
        raw_df.to_sql("sales", con=engine, if_exists="replace", index=False)
        st.success("✓ Data uploaded & transformed")

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    # ── Load data for filters ──
    df_full = load_data_from_db()

    if df_full.empty:
        st.warning("No data found. Run `python run_pipeline.py` first.")
        st.stop()

    st.markdown("<div class='section-title' style='font-size:0.82rem;'>🎛️ Filters</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    regions   = ["All"] + sorted(df_full["region"].dropna().unique().tolist())
    products  = ["All"] + sorted(df_full["product"].dropna().unique().tolist())
    reps      = ["All"] + sorted(df_full["sales_rep"].dropna().unique().tolist())

    sel_region  = st.selectbox("Region",    regions)
    sel_product = st.selectbox("Product",   products)
    sel_rep     = st.selectbox("Sales Rep", reps)

    st.markdown("<br>", unsafe_allow_html=True)

    # Month range slider
    if "month" in df_full.columns:
        months = sorted(df_full["month"].dropna().unique().tolist())
        if len(months) > 1:
            month_range = st.select_slider(
                "Month Range",
                options=months,
                value=(months[0], months[-1])
            )
        else:
            month_range = (months[0], months[0]) if months else (None, None)
    else:
        month_range = (None, None)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:0.7rem; color:rgba(232,232,240,0.3); text-align:center;'>"
        "Sales Data Analytics Pipeline<br>v2.0 · Built with Streamlit"
        "</div>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
fdf = df_full.copy()

if sel_region  != "All": fdf = fdf[fdf["region"]    == sel_region]
if sel_product != "All": fdf = fdf[fdf["product"]   == sel_product]
if sel_rep     != "All": fdf = fdf[fdf["sales_rep"] == sel_rep]

if month_range[0] and "month" in fdf.columns:
    fdf = fdf[(fdf["month"] >= month_range[0]) & (fdf["month"] <= month_range[1])]


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class='hero-header'>
    <div class='hero-badge'>Live Analytics</div>
    <div class='hero-title'>Sales Intelligence Dashboard</div>
    <div class='hero-subtitle'>
        Real-time insights across products, regions & sales reps — powered by your ETL pipeline
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────────
total_rev   = fdf["revenue"].sum()
total_ord   = len(fdf)
avg_order   = fdf["revenue"].mean() if total_ord > 0 else 0
top_rep_row = fdf.groupby("sales_rep")["revenue"].sum()
top_rep     = top_rep_row.idxmax() if not top_rep_row.empty else "—"
top_rep_rev = top_rep_row.max()    if not top_rep_row.empty else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='kpi-card green'>
        <div class='kpi-label'>Total Revenue</div>
        <div class='kpi-value'>{format_inr(total_rev)}</div>
        <div class='kpi-delta up'>↑ Filtered view</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='kpi-card blue'>
        <div class='kpi-label'>Total Orders</div>
        <div class='kpi-value'>{total_ord:,}</div>
        <div class='kpi-delta up'>↑ Clean records</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='kpi-card amber'>
        <div class='kpi-label'>Avg Order Value</div>
        <div class='kpi-value'>{format_inr(avg_order)}</div>
        <div class='kpi-delta up'>↑ Per transaction</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='kpi-card rose'>
        <div class='kpi-label'>Top Sales Rep</div>
        <div class='kpi-value' style='font-size:1.5rem;'>{top_rep}</div>
        <div class='kpi-delta up'>{format_inr(top_rep_rev)}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#a0a0b8", size=12),
    margin=dict(l=16, r=16, t=40, b=16),
    title_font=dict(family="Syne", color="#e8e8f0", size=15),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
)

COLORS = ["#63cab7", "#638cca", "#e8a838", "#e86889", "#a863ca", "#63a8e8"]


# ─────────────────────────────────────────────
# ROW 1 — Revenue by Product + Revenue by Region
# ─────────────────────────────────────────────
col_a, col_b = st.columns([3, 2])

with col_a:
    st.markdown("<div class='section-title'>Revenue by Product</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Total revenue contribution per product category</div>", unsafe_allow_html=True)

    prod_df = fdf.groupby("product")["revenue"].sum().reset_index().sort_values("revenue", ascending=True)
    fig_prod = go.Figure(go.Bar(
        x=prod_df["revenue"],
        y=prod_df["product"],
        orientation="h",
        marker=dict(
            color=COLORS[:len(prod_df)],
            line=dict(color="rgba(0,0,0,0)", width=0),
        ),
        text=[format_inr(v) for v in prod_df["revenue"]],
        textposition="outside",
        textfont=dict(color="#a0a0b8", size=11),
    ))
    fig_prod.update_layout(**PLOTLY_LAYOUT, title="", height=280)
    st.plotly_chart(fig_prod, use_container_width=True)

with col_b:
    st.markdown("<div class='section-title'>Revenue by Region</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Geographic distribution of sales</div>", unsafe_allow_html=True)

    reg_df = fdf.groupby("region")["revenue"].sum().reset_index()
    fig_reg = go.Figure(go.Pie(
        labels=reg_df["region"],
        values=reg_df["revenue"],
        hole=0.6,
        marker=dict(colors=COLORS, line=dict(color="#0a0a0f", width=2)),
        textinfo="label+percent",
        textfont=dict(color="#e8e8f0", size=12),
    ))
    fig_reg.update_layout(**PLOTLY_LAYOUT, title="", height=280,
                          showlegend=False)
    st.plotly_chart(fig_reg, use_container_width=True)


# ─────────────────────────────────────────────
# ROW 2 — Monthly Trend + Sales Rep Performance
# ─────────────────────────────────────────────
col_c, col_d = st.columns([3, 2])

with col_c:
    st.markdown("<div class='section-title'>Monthly Revenue Trend</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Revenue trajectory over time</div>", unsafe_allow_html=True)

    if "month" in fdf.columns:
        month_df = fdf.groupby("month")["revenue"].sum().reset_index().sort_values("month")
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=month_df["month"],
            y=month_df["revenue"],
            mode="lines+markers",
            line=dict(color="#63cab7", width=2.5, shape="spline"),
            marker=dict(color="#63cab7", size=7, line=dict(color="#0a0a0f", width=2)),
            fill="tozeroy",
            fillcolor="rgba(99,202,183,0.07)",
        ))
        fig_trend.update_layout(**PLOTLY_LAYOUT, height=280)
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Month data not available. Re-run the ETL pipeline.")

with col_d:
    st.markdown("<div class='section-title'>Sales Rep Leaderboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Top performers by revenue</div>", unsafe_allow_html=True)

    rep_df = fdf.groupby("sales_rep")["revenue"].sum().reset_index().sort_values("revenue", ascending=False)
    fig_rep = go.Figure(go.Bar(
        x=rep_df["sales_rep"],
        y=rep_df["revenue"],
        marker=dict(
            color=COLORS[:len(rep_df)],
            line=dict(color="rgba(0,0,0,0)", width=0),
        ),
        text=[format_inr(v) for v in rep_df["revenue"]],
        textposition="outside",
        textfont=dict(color="#a0a0b8", size=10),
    ))
    fig_rep.update_layout(**PLOTLY_LAYOUT, height=280)
    st.plotly_chart(fig_rep, use_container_width=True)


# ─────────────────────────────────────────────
# ROW 3 — Orders by Product (count) + Heatmap
# ─────────────────────────────────────────────
col_e, col_f = st.columns(2)

with col_e:
    st.markdown("<div class='section-title'>Order Volume by Product</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Number of orders, not revenue</div>", unsafe_allow_html=True)

    vol_df = fdf.groupby("product").size().reset_index(name="orders").sort_values("orders", ascending=False)
    fig_vol = go.Figure(go.Bar(
        x=vol_df["product"],
        y=vol_df["orders"],
        marker=dict(color=COLORS[:len(vol_df)]),
        text=vol_df["orders"],
        textposition="outside",
        textfont=dict(color="#a0a0b8", size=11),
    ))
    fig_vol.update_layout(**PLOTLY_LAYOUT, height=260)
    st.plotly_chart(fig_vol, use_container_width=True)

with col_f:
    st.markdown("<div class='section-title'>Region × Product Revenue Heatmap</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Cross-dimensional analysis</div>", unsafe_allow_html=True)

    heat_df = fdf.groupby(["region", "product"])["revenue"].sum().unstack(fill_value=0)
    fig_heat = go.Figure(go.Heatmap(
        z=heat_df.values,
        x=heat_df.columns.tolist(),
        y=heat_df.index.tolist(),
        colorscale=[[0, "#0a0f15"], [0.5, "#1a3a35"], [1, "#63cab7"]],
        showscale=True,
        text=[[format_inr(v) for v in row] for row in heat_df.values],
        texttemplate="%{text}",
        textfont=dict(size=10, color="#e8e8f0"),
        colorbar=dict(tickfont=dict(color="#a0a0b8")),
    ))
    fig_heat.update_layout(**PLOTLY_LAYOUT, height=260)
    st.plotly_chart(fig_heat, use_container_width=True)


st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA TABLE
# ─────────────────────────────────────────────
st.markdown("<div class='section-title'>📋 Transaction Data</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Full detail view of all filtered orders</div>", unsafe_allow_html=True)

# Format display copy
display_df = fdf.copy()
if "revenue" in display_df.columns:
    display_df["revenue"] = display_df["revenue"].apply(lambda x: f"₹{int(x):,}")
if "price" in display_df.columns:
    display_df["price"] = display_df["price"].apply(lambda x: f"₹{int(x):,}")

st.dataframe(
    display_df,
    use_container_width=True,
    height=340,
    column_config={
        "order_id":   st.column_config.NumberColumn("Order ID"),
        "product":    st.column_config.TextColumn("Product"),
        "region":     st.column_config.TextColumn("Region"),
        "sales_rep":  st.column_config.TextColumn("Sales Rep"),
        "quantity":   st.column_config.NumberColumn("Qty"),
        "price":      st.column_config.TextColumn("Unit Price"),
        "order_date": st.column_config.TextColumn("Date"),
        "revenue":    st.column_config.TextColumn("Revenue"),
        "month":      st.column_config.TextColumn("Month"),
    }
)

# ─────────────────────────────────────────────
# DOWNLOAD
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
dl_col, _ = st.columns([1, 3])
with dl_col:
    csv_data = fdf.to_csv(index=False)
    st.download_button(
        label="⬇ Export Filtered Data",
        data=csv_data,
        file_name="salesiq_filtered_export.csv",
        mime="text/csv",
    )