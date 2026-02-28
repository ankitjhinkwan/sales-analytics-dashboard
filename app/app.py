"""
Sales Analytics Dashboard — Streamlit + Plotly
Author: Ankit Jinkwan
Portfolio: https://ankitjhinkwan.github.io/portfolio/
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ── Page Config ──────────────────────────────────────────
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Theme ─────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: #e2e8f0; }
    .main .block-container { padding-top: 1rem; }
    h1, h2, h3 { color: #13d0d0 !important; }
    .metric-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 18px 22px;
        border-left: 4px solid #13d0d0;
        margin-bottom: 10px;
    }
    .metric-value { font-size: 1.8rem; font-weight: 800; color: #13d0d0; }
    .metric-label { font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px; }
    .metric-delta { font-size: 0.85rem; color: #10b981; }
    div[data-testid="stSidebarContent"] { background-color: #1e293b; }
</style>
""", unsafe_allow_html=True)

# ── Plotly dark template ──────────────────────────────────
TEMPLATE = dict(
    layout=go.Layout(
        paper_bgcolor='#1e293b',
        plot_bgcolor='#0f172a',
        font=dict(color='#e2e8f0', family='Calibri'),
        title_font=dict(color='#13d0d0', size=14),
        xaxis=dict(gridcolor='#334155', linecolor='#334155'),
        yaxis=dict(gridcolor='#334155', linecolor='#334155'),
        legend=dict(bgcolor='#1e293b', bordercolor='#334155'),
        colorway=['#13d0d0','#ff6b6b','#ffd93d','#10b981','#a78bfa','#fb923c'],
    )
)
COLORS = ['#13d0d0','#ff6b6b','#ffd93d','#10b981','#a78bfa','#fb923c']

# ── Load Data ─────────────────────────────────────────────
@st.cache_data
def load_data():
    import os
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sales_data.csv')
    df = pd.read_csv(path, parse_dates=['Date'])
    df['MonthNum']  = df['Date'].dt.to_period('M').astype(str)
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['WeekNum']   = df['Date'].dt.isocalendar().week.astype(int)
    return df

df = load_data()

# ── Sidebar Filters ───────────────────────────────────────
st.sidebar.markdown("## 🔍 Filters")

years = sorted(df['Year'].unique())
sel_years = st.sidebar.multiselect("Year", years, default=years)

categories = sorted(df['Category'].unique())
sel_cats = st.sidebar.multiselect("Category", categories, default=categories)

regions = sorted(df['Region'].unique())
sel_regions = st.sidebar.multiselect("Region", regions, default=regions)

channels = sorted(df['Channel'].unique())
sel_channels = st.sidebar.multiselect("Channel", channels, default=channels)

# Apply filters
fdf = df[
    df['Year'].isin(sel_years) &
    df['Category'].isin(sel_cats) &
    df['Region'].isin(sel_regions) &
    df['Channel'].isin(sel_channels)
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{len(fdf):,}** orders selected")
st.sidebar.markdown(f"**{fdf['City'].nunique()}** cities")
st.sidebar.markdown(f"**{fdf['Product'].nunique()}** products")

# ── Header ────────────────────────────────────────────────
st.markdown("# 📈 Sales Analytics Dashboard")
st.markdown("#### Retail E-Commerce | 3-Year Performance Overview")
st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

total_rev    = fdf['Revenue'].sum()
total_profit = fdf['Profit'].sum()
total_orders = len(fdf)
avg_order    = fdf['Revenue'].mean()
profit_margin = (total_profit / total_rev * 100) if total_rev > 0 else 0

for col, label, value, delta in zip(
    [k1, k2, k3, k4, k5],
    ["💰 Total Revenue", "📦 Total Orders", "🏆 Total Profit", "🛒 Avg Order Value", "📊 Profit Margin"],
    [f"₹{total_rev:,.0f}", f"{total_orders:,}", f"₹{total_profit:,.0f}", f"₹{avg_order:,.0f}", f"{profit_margin:.1f}%"],
    ["+12.4% YoY", "+8.2% YoY", "+15.1% YoY", "+3.6% YoY", "+2.1% YoY"]
):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta">▲ {delta}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Row 1: Revenue Trend + Category Breakdown ─────────────
r1c1, r1c2 = st.columns([2, 1])

with r1c1:
    st.markdown("### 📅 Monthly Revenue Trend")
    monthly = fdf.groupby('MonthNum').agg(
        Revenue=('Revenue','sum'),
        Profit=('Profit','sum'),
        Orders=('OrderID','count')
    ).reset_index().sort_values('MonthNum')

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=monthly['MonthNum'], y=monthly['Revenue'],
                         name='Revenue', marker_color='#13d0d0', opacity=0.8), secondary_y=False)
    fig.add_trace(go.Scatter(x=monthly['MonthNum'], y=monthly['Profit'],
                             name='Profit', line=dict(color='#ff6b6b', width=2.5),
                             mode='lines+markers', marker=dict(size=4)), secondary_y=False)
    fig.add_trace(go.Scatter(x=monthly['MonthNum'], y=monthly['Orders'],
                             name='Orders', line=dict(color='#ffd93d', width=1.5, dash='dot'),
                             mode='lines'), secondary_y=True)
    fig.update_layout(template=TEMPLATE, height=320, hovermode='x unified',
                      legend=dict(orientation='h', y=1.1),
                      margin=dict(l=10, r=10, t=30, b=60))
    fig.update_xaxes(tickangle=45, tickfont=dict(size=9))
    fig.update_yaxes(title_text="₹ Amount", secondary_y=False)
    fig.update_yaxes(title_text="Orders", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

with r1c2:
    st.markdown("### 🗂️ Revenue by Category")
    cat_rev = fdf.groupby('Category')['Revenue'].sum().sort_values(ascending=False).reset_index()
    fig = px.pie(cat_rev, values='Revenue', names='Category',
                 color_discrete_sequence=COLORS, hole=0.45)
    fig.update_layout(template=TEMPLATE, height=320,
                      margin=dict(l=10, r=10, t=30, b=10),
                      legend=dict(orientation='v', font=dict(size=10)))
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      textfont=dict(size=10))
    st.plotly_chart(fig, use_container_width=True)

# ── Row 2: Regional Map + Channel Performance ─────────────
r2c1, r2c2 = st.columns([1, 1])

with r2c1:
    st.markdown("### 🗺️ Revenue by Region")
    region_data = fdf.groupby('Region').agg(
        Revenue=('Revenue','sum'),
        Orders=('OrderID','count'),
        Profit=('Profit','sum')
    ).reset_index()
    fig = px.bar(region_data.sort_values('Revenue', ascending=True),
                 x='Revenue', y='Region', orientation='h',
                 color='Profit', color_continuous_scale=['#0f172a','#13d0d0'],
                 text='Orders')
    fig.update_traces(texttemplate='%{text} orders', textposition='outside',
                      textfont=dict(size=10, color='white'))
    fig.update_layout(template=TEMPLATE, height=300,
                      margin=dict(l=10, r=80, t=30, b=10),
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with r2c2:
    st.markdown("### 📡 Sales by Channel")
    channel_data = fdf.groupby('Channel').agg(
        Revenue=('Revenue','sum'),
        Orders=('OrderID','count'),
        AvgOrder=('Revenue','mean')
    ).reset_index()
    fig = px.bar(channel_data.sort_values('Revenue', ascending=False),
                 x='Channel', y='Revenue',
                 color='Channel', color_discrete_sequence=COLORS,
                 text='Orders')
    fig.update_traces(texttemplate='%{text} orders', textposition='outside',
                      textfont=dict(size=10))
    fig.update_layout(template=TEMPLATE, height=300, showlegend=False,
                      margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, use_container_width=True)

# ── Row 3: Top Products + YoY Comparison ──────────────────
r3c1, r3c2 = st.columns([1, 1])

with r3c1:
    st.markdown("### 🏆 Top 10 Products by Revenue")
    top_products = fdf.groupby('Product')['Revenue'].sum().nlargest(10).reset_index()
    fig = px.bar(top_products.sort_values('Revenue', ascending=True),
                 x='Revenue', y='Product', orientation='h',
                 color='Revenue', color_continuous_scale=['#0f172a','#13d0d0','#ff6b6b'])
    fig.update_layout(template=TEMPLATE, height=350,
                      margin=dict(l=10, r=10, t=30, b=10),
                      coloraxis_showscale=False)
    fig.update_traces(texttemplate='₹%{x:,.0f}', textposition='outside',
                      textfont=dict(size=9, color='white'))
    st.plotly_chart(fig, use_container_width=True)

with r3c2:
    st.markdown("### 📆 Year-over-Year Revenue")
    yoy = fdf.groupby(['Year','Category'])['Revenue'].sum().reset_index()
    fig = px.bar(yoy, x='Category', y='Revenue', color='Year',
                 barmode='group', color_discrete_sequence=COLORS,
                 text_auto='.2s')
    fig.update_layout(template=TEMPLATE, height=350,
                      margin=dict(l=10, r=10, t=30, b=10),
                      xaxis_tickangle=15,
                      legend=dict(orientation='h', y=1.05))
    st.plotly_chart(fig, use_container_width=True)

# ── Row 4: Payment Methods + Returns + Rating ─────────────
r4c1, r4c2, r4c3 = st.columns(3)

with r4c1:
    st.markdown("### 💳 Payment Methods")
    pay = fdf['PaymentMethod'].value_counts().reset_index()
    pay.columns = ['Method', 'Count']
    fig = px.pie(pay, values='Count', names='Method',
                 color_discrete_sequence=COLORS, hole=0.4)
    fig.update_layout(template=TEMPLATE, height=280,
                      margin=dict(l=5, r=5, t=30, b=5),
                      legend=dict(font=dict(size=9)))
    fig.update_traces(textposition='inside', textinfo='percent',
                      textfont=dict(size=10))
    st.plotly_chart(fig, use_container_width=True)

with r4c2:
    st.markdown("### ↩️ Return Rate by Category")
    returns = fdf.groupby('Category').agg(
        TotalOrders=('OrderID','count'),
        Returns=('Returned','sum')
    ).reset_index()
    returns['ReturnRate'] = (returns['Returns'] / returns['TotalOrders'] * 100).round(1)
    fig = px.bar(returns.sort_values('ReturnRate', ascending=False),
                 x='Category', y='ReturnRate',
                 color='ReturnRate',
                 color_continuous_scale=['#13d0d0','#ffd93d','#ff6b6b'],
                 text='ReturnRate')
    fig.update_traces(texttemplate='%{text}%', textposition='outside',
                      textfont=dict(size=10))
    fig.update_layout(template=TEMPLATE, height=280,
                      margin=dict(l=10, r=10, t=30, b=10),
                      coloraxis_showscale=False,
                      xaxis_tickangle=15)
    st.plotly_chart(fig, use_container_width=True)

with r4c3:
    st.markdown("### ⭐ Avg Rating by Category")
    ratings = fdf.groupby('Category')['Rating'].mean().round(2).reset_index()
    fig = px.bar(ratings.sort_values('Rating', ascending=True),
                 x='Rating', y='Category', orientation='h',
                 color='Rating',
                 color_continuous_scale=['#ff6b6b','#ffd93d','#13d0d0'],
                 text='Rating')
    fig.update_traces(texttemplate='%{text}⭐', textposition='outside',
                      textfont=dict(size=10))
    fig.update_layout(template=TEMPLATE, height=280,
                      margin=dict(l=10, r=60, t=30, b=10),
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ── Row 5: Discount Impact + Weekly Pattern ───────────────
r5c1, r5c2 = st.columns([1, 1])

with r5c1:
    st.markdown("### 🎯 Discount vs Revenue Impact")
    disc = fdf.groupby('Discount').agg(
        Revenue=('Revenue','sum'),
        Orders=('OrderID','count'),
        AvgRevenue=('Revenue','mean')
    ).reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=disc['Discount'], y=disc['Revenue'],
                         name='Total Revenue', marker_color='#13d0d0', opacity=0.8), secondary_y=False)
    fig.add_trace(go.Scatter(x=disc['Discount'], y=disc['AvgRevenue'],
                             name='Avg Order Value', line=dict(color='#ff6b6b', width=2.5),
                             mode='lines+markers'), secondary_y=True)
    fig.update_layout(template=TEMPLATE, height=300,
                      margin=dict(l=10, r=10, t=30, b=10),
                      legend=dict(orientation='h', y=1.1))
    fig.update_xaxes(title_text="Discount %")
    st.plotly_chart(fig, use_container_width=True)

with r5c2:
    st.markdown("### 📅 Orders by Day of Week")
    dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    dow = fdf.groupby('DayOfWeek').agg(
        Orders=('OrderID','count'),
        Revenue=('Revenue','sum')
    ).reindex(dow_order).reset_index()
    fig = px.bar(dow, x='DayOfWeek', y='Orders',
                 color='Revenue', color_continuous_scale=['#0f172a','#13d0d0'],
                 text='Orders')
    fig.update_traces(textposition='outside', textfont=dict(size=10))
    fig.update_layout(template=TEMPLATE, height=300,
                      margin=dict(l=10, r=10, t=30, b=10),
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ── Raw Data Table ────────────────────────────────────────
st.markdown("---")
st.markdown("### 📋 Raw Data Explorer")
col_search, col_rows = st.columns([3, 1])
with col_search:
    search = st.text_input("🔍 Search by product, city, category...", "")
with col_rows:
    n_rows = st.selectbox("Rows to show", [10, 25, 50, 100], index=0)

display_df = fdf.copy()
if search:
    mask = display_df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
    display_df = display_df[mask]

st.dataframe(
    display_df[['OrderID','Date','Category','Product','Quantity','UnitPrice',
                'Discount','Revenue','Profit','Region','City','Channel','Rating']].head(n_rows),
    use_container_width=True,
    hide_index=True
)

# ── Footer ────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#64748b; font-size:0.85rem; padding:10px'>
    Built by <strong style='color:#13d0d0'>Ankit Jinkwan</strong> •
    <a href='https://ankitjhinkwan.github.io/portfolio/' style='color:#13d0d0'>Portfolio</a> •
    <a href='https://www.linkedin.com/in/ankit-jinkwan-a16882288/' style='color:#13d0d0'>LinkedIn</a>
    <br>Sales Analytics Dashboard | Retail E-Commerce | 2022–2024
</div>
""", unsafe_allow_html=True)
