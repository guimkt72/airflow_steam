import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config for white background
st.set_page_config(
    page_title="CS2 Steam Market Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for white background and black text
st.markdown("""
    <style>
        .stApp {
            background-color: white;
            color: black;
        }
        .stSelectbox label, .stMultiSelect label {
            color: black !important;
        }
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        [data-testid="stMetricLabel"] {
            color: black !important;
        }
        [data-testid="stMetricValue"] {
            color: black !important;
        }
        [data-testid="stMetricDelta"] {
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

# Database connection configuration
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'your_db_name'),
    'user': os.getenv('DB_USER', 'your_username'),
    'password': os.getenv('DB_PASSWORD', 'your_password'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

# Metric name mappings
METRIC_NAMES = {
    'med_offers': 'Sum of Offers',
    'med_price': 'Price Mean',
    'var_price': 'Price Varying',
    'var_buff': 'Buff Varying',
    'var_steam': 'Steam Varying',
    'var_real': 'Real Varying'
}

def get_db_connection():
    """Create a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Unable to connect to the database: {e}")
        return None

@st.cache_data(ttl=3600)
def load_wallet_data():
    """Load wallet data from the database"""
    conn = get_db_connection()
    if conn:
        try:
            query = "select * from wallet_data_dbt"
            df = pd.read_sql_query(query, conn)
            return df
        finally:
            conn.close()
    return None

@st.cache_data(ttl=3600)
def load_historical_data():
    """Load historical data from the database"""
    conn = get_db_connection()
    if conn:
        try:
            query = "select * from agg_data_dbt"
            df = pd.read_sql_query(query, conn)
            return df
        finally:
            conn.close()
    return None

@st.cache_data(ttl=3600)
def load_current_price_data():
    """Load current price variation data"""
    conn = get_db_connection()
    if conn:
        try:
            query = "select * from current_price_data_dbt"
            df = pd.read_sql_query(query, conn)
            return df
        finally:
            conn.close()
    return None

@st.cache_data(ttl=3600)
def load_cagr_data():
    """Load CAGR data"""
    conn = get_db_connection()
    if conn:
        try:
            query = "select * from cagr_data_dbt"
            df = pd.read_sql_query(query, conn)
            return df
        finally:
            conn.close()
    return None

def plot_historical_metrics(df, selected_items, selected_metric):
    """Create a line plot for historical metrics"""
    if df is None or df.empty:
        return None
    
    fig = px.line(
        df[df['item'].isin(selected_items)],
        x='date_month',
        y=selected_metric,
        color='item',
        title=f'{METRIC_NAMES[selected_metric]} Over Time by Item'
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='black',
        title_font_color='black',
        xaxis=dict(
            showgrid=False,
            linecolor='black',
            linewidth=1,
            title_font_color='black',
            tickfont_color='black'
        ),
        yaxis=dict(
            showgrid=False,
            linecolor='black',
            linewidth=1,
            title_font_color='black',
            tickfont_color='black'
        ),
        legend_font_color='black'
    )
    return fig

def plot_price_variations_comparison(df, selected_metric):
    """Create a bar plot comparing all items for a given metric"""
    if df is None or df.empty:
        return None
    
    # Calculate the mean of the metric for each item
    df_mean = df.groupby('item')[selected_metric].mean().sort_values(ascending=True)
    
    fig = go.Figure(data=[
        go.Bar(
            x=df_mean.values,
            y=df_mean.index,
            orientation='h',
            marker_color='blue'
        )
    ])
    
    fig.update_layout(
        title=f'{METRIC_NAMES[selected_metric]} Comparison Across Items',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='black',
        title_font_color='black',
        height=max(400, len(df_mean) * 25),  # Adjust height based on number of items
        xaxis=dict(
            title=METRIC_NAMES[selected_metric],
            showgrid=False,
            linecolor='black',
            linewidth=1,
            title_font_color='black',
            tickfont_color='black'
        ),
        yaxis=dict(
            title='Items',
            showgrid=False,
            linecolor='black',
            linewidth=1,
            title_font_color='black',
            tickfont_color='black'
        )
    )
    return fig

def plot_cagr_comparison(df, selected_items=None):
    """Create a bar plot comparing CAGR for all or selected items"""
    if df is None or df.empty:
        return None
    
    if selected_items is None:
        df_filtered = df
    else:
        df_filtered = df[df['item'].isin(selected_items)]
    
    # Sort by CAGR percentage
    df_filtered = df_filtered.sort_values('cagr_percent', ascending=True)
    
    fig = go.Figure(data=[
        go.Bar(
            x=df_filtered['cagr_percent'],
            y=df_filtered['item'],
            orientation='h',
            marker_color='blue'
        )
    ])
    
    fig.update_layout(
        title='CAGR Percentage Comparison Across Items',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='black',
        title_font_color='black',
        height=max(400, len(df_filtered) * 25),  # Adjust height based on number of items
        xaxis=dict(
            title='CAGR %',
            showgrid=False,
            linecolor='black',
            linewidth=1,
            title_font_color='black',
            tickfont_color='black'
        ),
        yaxis=dict(
            title='Items',
            showgrid=False,
            linecolor='black',
            linewidth=1,
            title_font_color='black',
            tickfont_color='black'
        )
    )
    return fig

# Streamlit UI
st.title('CS2 Steam Market Analytics Dashboard')

# Load all data
wallet_data = load_wallet_data()
historical_data = load_historical_data()
current_price_data = load_current_price_data()
cagr_data = load_cagr_data()

# Wallet Summary Section
st.header('Wallet Summary')
if wallet_data is not None:
    # Calculate total metrics
    payment_price = wallet_data['sum_price_real'].sum()
    current_price = wallet_data['sum_last_real'].sum()
    profit_loss = current_price - payment_price
    price_variation = ((current_price - payment_price) / payment_price * 100) if payment_price != 0 else 0
    
    # Create three columns for metrics
    col_wallet1, col_wallet2, col_wallet3 = st.columns(3)
    
    with col_wallet1:
        st.metric(
            "Total Investment",
            f"R${payment_price:,.2f}",
            help="Total amount invested in items"
        )
    
    with col_wallet2:
        st.metric(
            "Current Value",
            f"R${current_price:,.2f}",
            f"{price_variation:+.2f}%",
            delta_color="off" if price_variation < 0 else "normal",
            help="Current total value of items"
        )
    
    with col_wallet3:
        st.metric(
            "Total Profit/Loss",
            f"R${profit_loss:,.2f}",
            delta_color="off",
            help="Absolute profit or loss"
        )

st.markdown("---")  # Add a divider

# Create columns for layout
col1, col2 = st.columns(2)

# Historical Data Section
with col1:
    st.header('Historical Metrics')
    if historical_data is not None:
        items = historical_data['item'].unique()
        metrics = ['med_offers', 'med_price', 'var_price']
        
        # Set default selections
        default_items = items[:3]  # Select first 3 items by default
        selected_items = st.multiselect('Select Items', items, default=default_items)
        selected_metric = st.selectbox(
            'Select Metric',
            metrics,
            index=1,  # Select 'med_price' by default (index 1)
            format_func=lambda x: METRIC_NAMES[x]
        )
        
        # Always show the graph, even with default selections
        fig = plot_historical_metrics(historical_data, selected_items if selected_items else default_items, selected_metric)
        st.plotly_chart(fig, use_container_width=True)

# Price Variations Section
with col2:
    st.header('Price Variations Comparison')
    if current_price_data is not None:
        metrics = ['var_steam', 'var_real', 'var_buff']
        
        selected_var_metric = st.selectbox(
            'Select Variation Metric',
            metrics,
            format_func=lambda x: METRIC_NAMES[x],
            key='price_var_metric'
        )
        
        fig = plot_price_variations_comparison(current_price_data, selected_var_metric)
        st.plotly_chart(fig, use_container_width=True)

# CAGR Section
st.header('CAGR Analysis')
if cagr_data is not None:
    items = cagr_data['item'].unique()
    selected_cagr_items = st.multiselect(
        'Select Items for CAGR Analysis (leave empty to show all)',
        items,
        key='cagr_items'
    )
    
    # If no items selected, show all
    if not selected_cagr_items:
        selected_cagr_items = None
    
    col3, col4 = st.columns([1, 2])
    
    with col3:
        # Display CAGR table
        st.subheader('CAGR Details')
        if selected_cagr_items:
            filtered_data = cagr_data[cagr_data['item'].isin(selected_cagr_items)]
        else:
            filtered_data = cagr_data
        
        cagr_display_cols = ['item', 'year_diff', 'price_real', 'last_real', 'cagr_percent']
        st.dataframe(
            filtered_data[cagr_display_cols].sort_values('cagr_percent', ascending=False),
            hide_index=True
        )
    
    with col4:
        # Display CAGR plot
        fig = plot_cagr_comparison(cagr_data, selected_cagr_items)
        st.plotly_chart(fig, use_container_width=True)


