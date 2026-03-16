
"""
================================================================================
ELECTUDE AFRICA TVET ANALYTICS DASHBOARD - PROFESSIONAL EDITION
================================================================================

A comprehensive, enterprise-grade analytics dashboard for Technical and 
Vocational Education (TVET) data across Africa.

Version: 2.0.0
Author: Electude Africa Data Science Team

Features:
- Modern, professional UI with custom CSS styling
- Interactive Plotly visualizations
- Real-time data filtering and exploration
- AI-powered insights and recommendations
- Data quality monitoring and reporting
- Multi-format data export capabilities

Usage:
    streamlit run electude_dashboard_pro.py

Requirements:
    streamlit>=1.28.0
    pandas>=2.0.0
    plotly>=5.18.0
    numpy>=1.24.0
================================================================================
"""

# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import warnings

warnings.filterwarnings('ignore')


# =============================================================================
# CONFIGURATION & THEME
# =============================================================================

@dataclass
class ThemeColors:
    """Professional color palette for the dashboard."""
    primary: str = "#1E3A5F"
    secondary: str = "#2E86AB"
    accent: str = "#F18F01"
    success: str = "#28A745"
    warning: str = "#FFC107"
    danger: str = "#DC3545"
    info: str = "#17A2B8"
    dark: str = "#1A1A2E"
    light: str = "#F8F9FA"
    teal: str = "#20C997"
    purple: str = "#6F42C1"
    pink: str = "#E83E8C"
    indigo: str = "#6610F2"


# Initialize theme
THEME = ThemeColors()

# Chart color sequences
CHART_COLORS = [
    THEME.primary, THEME.secondary, THEME.accent,
    THEME.teal, THEME.purple, THEME.pink
]

DIVERGENT_COLORS = [
    "#0d47a1", "#1976d2", "#42a5f5", "#90caf9",
    "#ffcc80", "#ffa726", "#f57c00", "#e65100"
]

# Country flag mappings
COUNTRY_FLAGS = {
    "Kenya": "\ud83c\uddf0\ud83c\uddea", "Uganda": "\ud83c\uddfa\ud83c\uddec", "Tanzania": "\ud83c\uddf9\ud83c\uddff", "Rwanda": "\ud83c\uddf7\ud83c\uddfc",
    "Ethiopia": "\ud83c\uddea\ud83c\uddf9", "Ghana": "\ud83c\uddec\ud83c\udded", "Nigeria": "\ud83c\uddf3\ud83c\uddec", "South Africa": "\ud83c\uddff\ud83c\udde6",
    "Zambia": "\ud83c\uddff\ud83c\uddf2", "Malawi": "\ud83c\uddf2\ud83c\uddfc", "Burundi": "\ud83c\udde7\ud83c\uddee", "DRC": "\ud83c\udde8\ud83c\udde9"
}


# =============================================================================
# CUSTOM CSS STYLES
# =============================================================================

def get_custom_css() -> str:
    """Return comprehensive custom CSS for professional dashboard styling."""
    return """
    <style>
        /* ===== ROOT VARIABLES ===== */
        :root {
            --primary-color: #1E3A5F;
            --secondary-color: #2E86AB;
            --accent-color: #F18F01;
            --success-color: #28A745;
            --warning-color: #FFC107;
            --danger-color: #DC3545;
            --info-color: #17A2B8;
            --dark-color: #1A1A2E;
            --light-color: #F8F9FA;
            --gradient-primary: linear-gradient(135deg, #1E3A5F 0%, #2E86AB 100%);
            --gradient-accent: linear-gradient(135deg, #F18F01 0%, #C73E1D 100%);
            --gradient-success: linear-gradient(135deg, #28A745 0%, #20C997 100%);
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.08);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.12);
            --shadow-lg: 0 8px 24px rgba(0,0,0,0.16);
            --border-radius: 12px;
            --transition: all 0.3s ease;
        }

        /* ===== GLOBAL STYLES ===== */
        .stApp {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* ===== HEADER STYLING ===== */
        .main-header {
            background: var(--gradient-primary);
            padding: 2.5rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
        }

        .main-header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            transform: rotate(30deg);
        }

        .main-header h1 {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
        }

        .main-header .subtitle {
            color: rgba(255,255,255,0.9);
            font-size: 1.1rem;
            margin-top: 0.5rem;
            position: relative;
            z-index: 1;
        }

        .main-header .header-stats {
            display: flex;
            gap: 2rem;
            margin-top: 1.5rem;
            position: relative;
            z-index: 1;
        }

        .main-header .stat-item {
            text-align: center;
        }

        .main-header .stat-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: white;
        }

        .main-header .stat-label {
            font-size: 0.85rem;
            color: rgba(255,255,255,0.8);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* ===== METRIC CARDS ===== */
        .metric-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 1rem;
            margin-bottom: 2rem;
        }

        @media (max-width: 1200px) {
            .metric-container {
                grid-template-columns: repeat(3, 1fr);
            }
        }

        @media (max-width: 768px) {
            .metric-container {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        .metric-card {
            background: white;
            border-radius: var(--border-radius);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
        }

        .metric-card.students::before { background: var(--gradient-primary); }
        .metric-card.teachers::before { background: var(--gradient-accent); }
        .metric-card.institutions::before { background: var(--gradient-success); }
        .metric-card.avg-students::before { background: linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%); }
        .metric-card.satisfaction::before { background: linear-gradient(135deg, #17a2b8 0%, #6610f2 100%); }

        .metric-card .icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .metric-card .label {
            font-size: 0.8rem;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.25rem;
        }

        .metric-card .value {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary-color);
        }

        .metric-card .delta {
            font-size: 0.75rem;
            margin-top: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }

        .metric-card .delta.positive { color: var(--success-color); }
        .metric-card .delta.negative { color: var(--danger-color); }

        /* ===== SECTION HEADERS ===== */
        .section-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #e9ecef;
        }

        .section-header .icon {
            font-size: 1.5rem;
        }

        .section-header h2 {
            margin: 0;
            font-size: 1.35rem;
            font-weight: 600;
            color: var(--primary-color);
        }

        /* ===== CHART CARDS ===== */
        .chart-card {
            background: white;
            border-radius: var(--border-radius);
            padding: 1.5rem;
            box-shadow: var(--shadow-sm);
            margin-bottom: 1.5rem;
            transition: var(--transition);
        }

        .chart-card:hover {
            box-shadow: var(--shadow-md);
        }

        .chart-card h3 {
            margin: 0 0 1rem 0;
            font-size: 1rem;
            font-weight: 600;
            color: var(--primary-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* ===== SIDEBAR STYLING ===== */
        [data-testid="stSidebar"] {
            background: var(--gradient-primary) !important;
        }

        [data-testid="stSidebar"] > div {
            padding: 1.5rem 1rem;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label {
            color: white !important;
        }

        [data-testid="stSidebar"] label {
            font-weight: 500;
        }

        [data-testid="stSidebar"] .stMultiSelect > div > div {
            background: white;
            border-radius: 8px;
        }

        .sidebar-header {
            text-align: center;
            padding: 1rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 1.5rem;
        }

        .sidebar-header h2 {
            font-size: 1.5rem;
            margin: 0;
        }

        .sidebar-header p {
            color: rgba(255,255,255,0.8);
            font-size: 0.9rem;
            margin: 0.25rem 0 0 0;
        }

        /* ===== BUTTONS ===== */
        .stButton button,
        .stDownloadButton button {
            background: var(--gradient-primary) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.25rem !important;
            font-weight: 600 !important;
            transition: var(--transition) !important;
            box-shadow: var(--shadow-sm) !important;
        }

        .stButton button:hover,
        .stDownloadButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: var(--shadow-md) !important;
        }

        /* ===== DATA TABLE STYLING ===== */
        .stDataFrame {
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--shadow-sm);
        }

        .stDataFrame th {
            background: var(--primary-color) !important;
            color: white !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.5px;
            padding: 1rem !important;
        }

        .stDataFrame td {
            padding: 0.75rem 1rem !important;
            border-bottom: 1px solid #e9ecef;
        }

        .stDataFrame tr:hover td {
            background: #f8f9fa;
        }

        /* ===== INSIGHT BOX ===== */
        .insight-box {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border-left: 4px solid var(--info-color);
            padding: 1.25rem;
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
            margin: 1rem 0;
        }

        .insight-box h4 {
            margin: 0 0 0.75rem 0;
            color: var(--primary-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .insight-box ul {
            margin: 0;
            padding-left: 1.25rem;
        }

        .insight-box li {
            margin-bottom: 0.5rem;
            color: #495057;
            line-height: 1.5;
        }

        /* ===== QUALITY INDICATOR ===== */
        .quality-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1rem;
            background: #f8f9fa;
            border-radius: 8px;
            margin-bottom: 0.5rem;
        }

        .quality-indicator .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }

        .quality-indicator .status-dot.good { background: var(--success-color); }
        .quality-indicator .status-dot.warning { background: var(--warning-color); }
        .quality-indicator .status-dot.danger { background: var(--danger-color); }

        /* ===== TABS STYLING ===== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            background: white;
            border-radius: 8px 8px 0 0;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            color: #6c757d;
            transition: var(--transition);
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: #f8f9fa;
            color: var(--primary-color);
        }

        .stTabs [aria-selected="true"] {
            background: white !important;
            color: var(--primary-color) !important;
            border-bottom: 3px solid var(--accent-color) !important;
        }

        /* ===== FOOTER ===== */
        .dashboard-footer {
            text-align: center;
            padding: 2rem;
            margin-top: 2rem;
            border-top: 1px solid #e9ecef;
            color: #6c757d;
        }

        .dashboard-footer .logo {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }

        /* ===== PASSWORD SCREEN ===== */
        .password-container {
            max-width: 400px;
            margin: 8% auto;
            background: white;
            padding: 2.5rem;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-lg);
            text-align: center;
        }

        .password-container .lock-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }

        .password-container h1 {
            color: var(--primary-color);
            margin-bottom: 0.5rem;
            font-size: 1.5rem;
        }

        .password-container p {
            color: #6c757d;
            margin-bottom: 1.5rem;
        }

        /* ===== ANIMATIONS ===== */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .animate-fade-in {
            animation: fadeIn 0.5s ease-out;
        }

        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--secondary-color);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--primary-color);
        }

        /* ===== RECOMMENDATION CARDS ===== */
        .recommendation-card {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
            box-shadow: var(--shadow-sm);
            border-left: 4px solid var(--warning-color);
        }

        .recommendation-card h5 {
            margin: 0;
            color: var(--primary-color);
            font-size: 0.95rem;
        }

        .recommendation-card p {
            margin: 0.5rem 0 0 0;
            color: #6c757d;
            font-size: 0.85rem;
        }

        .recommendation-card .priority {
            float: right;
            background: var(--warning-color);
            color: #1A1A2E;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
        }

        .recommendation-card .priority.high {
            background: var(--danger-color);
            color: white;
        }

        .recommendation-card .priority.low {
            background: var(--success-color);
            color: white;
        }
    </style>
    """


# =============================================================================
# HTML COMPONENT GENERATORS
# =============================================================================

def get_metric_card_html(icon: str, label: str, value: str, card_class: str) -> str:
    """Generate HTML for a professional metric card."""
    return f"""
    <div class="metric-card {card_class} animate-fade-in">
        <div class="icon">{icon}</div>
        <div class="label">{label}</div>
        <div class="value">{value}</div>
    </div>
    """


def get_section_header_html(icon: str, title: str) -> str:
    """Generate HTML for a section header."""
    return f"""
    <div class="section-header">
        <span class="icon">{icon}</span>
        <h2>{title}</h2>
    </div>
    """


def get_insight_box_html(title: str, insights: List[str]) -> str:
    """Generate HTML for an insight box."""
    insights_html = "\
".join([f"<li>{insight}</li>" for insight in insights])
    return f"""
    <div class="insight-box">
        <h4>\ud83d\udca1 {title}</h4>
        <ul>{insights_html}</ul>
    </div>
    """


def get_quality_indicator_html(label: str, value: int, status: str) -> str:
    """Generate HTML for a data quality indicator."""
    return f"""
    <div class="quality-indicator">
        <span class="status-dot {status}"></span>
        <span>{label}: <strong>{value}</strong></span>
    </div>
    """


# =============================================================================
# CHART UTILITIES
# =============================================================================

def apply_chart_style(fig: go.Figure, title: str = None) -> go.Figure:
    """Apply consistent professional styling to any Plotly figure."""
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Segoe UI, sans-serif", size=11, color="#2c3e50"),
        title=dict(
            text=title,
            font=dict(size=14, color=THEME.primary),
            x=0.5,
            xanchor="center"
        ) if title else None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,249,250,0.5)",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(
            gridcolor="#e9ecef",
            linecolor="#dee2e6",
            ticks="outside"
        ),
        yaxis=dict(
            gridcolor="#e9ecef",
            linecolor="#dee2e6",
            ticks="outside"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor=THEME.primary,
            font_size=12
        )
    )
    return fig


def create_bar_chart(df, x, y, title, color=None, orientation="v", 
                     color_scale=None, show_values=False):
    """Create a professionally styled bar chart."""
    if color_scale is None:
        color_scale = [THEME.primary, THEME.secondary]
    
    fig = px.bar(
        df, x=x, y=y,
        color=color if color else y,
        orientation=orientation,
        color_continuous_scale=color_scale
    )
    
    apply_chart_style(fig, title)
    
    if show_values:
        fig.update_traces(
            texttemplate='%{y:,.0f}',
            textposition='outside',
            textfont=dict(size=10, color="#6c757d")
        )
    
    if not color:
        fig.update_coloraxes(showscale=False)
    
    fig.update_traces(
        marker_line_width=0,
        marker_opacity=0.9
    )
    
    return fig


def create_pie_chart(df, names, values, title, hole=0.45, colors=None):
    """Create a professionally styled donut/pie chart."""
    if colors is None:
        colors = CHART_COLORS
    
    fig = px.pie(
        df, names=names, values=values,
        hole=hole,
        color_discrete_sequence=colors
    )
    
    apply_chart_style(fig, title)
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(size=11, color="white"),
        marker=dict(line=dict(color="white", width=2)),
        pull=[0.02] * len(df)
    )
    
    if hole > 0:
        total = df[values].sum()
        fig.add_annotation(
            text=f"<b>{total:,}</b><br><span style='font-size:9px'>Total</span>",
            x=0.5, y=0.5,
            font_size=14,
            font_color=THEME.primary,
            showarrow=False
        )
    
    return fig


def create_gauge_chart(value, title, max_value=100, thresholds=(40, 70)):
    """Create a gauge chart for KPI visualization."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title=dict(text=title, font=dict(size=12)),
        gauge={
            'axis': {'range': [0, max_value], 'tickwidth': 1},
            'bar': {'color': THEME.primary},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e9ecef",
            'steps': [
                {'range': [0, thresholds[0]], 'color': "#dc3545"},
                {'range': [thresholds[0], thresholds[1]], 'color': "#ffc107"},
                {'range': [thresholds[1], max_value], 'color': "#28a745"}
            ],
            'threshold': {
                'line': {'color': "#1A1A2E", 'width': 3},
                'thickness': 0.75,
                'value': value
            }
        },
        number={'font': {'size': 20, 'color': THEME.primary}}
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(l=30, r=30, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig


def create_empty_chart(message="No data available"):
    """Create a placeholder chart when no data is available."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=14, color="#6c757d")
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        paper_bgcolor="rgba(0,0,0,0)",
        height=250
    )
    return fig


# =============================================================================
# DATA PROCESSING UTILITIES
# =============================================================================

@dataclass
class DataQualityReport:
    """Container for data quality metrics."""
    total_records: int
    complete_records: int
    missing_emails: int
    missing_phones: int
    missing_students: int
    duplicate_records: int
    quality_score: float


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply comprehensive cleaning pipeline to the dataframe."""
    if df.empty:
        return df
    
    df_clean = df.copy()
    
    # Clean institution names
    if "Institution" in df_clean.columns:
        df_clean["Institution"] = df_clean["Institution"].ffill().str.strip()
    
    # Clean numeric columns
    if "Number of Students" in df_clean.columns:
        df_clean["Number of Students"] = pd.to_numeric(
            df_clean["Number of Students"], errors="coerce"
        ).fillna(0).astype(int)
    
    # Clean categorical columns
    for col in ["Electude Domain", "Language"]:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].ffill()
    
    # Handle teacher names
    if "Teacher / Trainer" in df_clean.columns:
        df_clean["Teacher / Trainer"] = df_clean["Teacher / Trainer"].fillna("Unknown").str.strip()
    
    # Clean contact info
    if "EMAIL" in df_clean.columns:
        df_clean["EMAIL"] = df_clean["EMAIL"].str.lower().str.strip()
    
    if "Phone number" in df_clean.columns:
        df_clean["Phone number"] = df_clean["Phone number"].astype(str).str.strip()
    
    # Extract country from institution name
    if "Institution" in df_clean.columns:
        df_clean["Country"] = df_clean["Institution"].str.split("-").str[-1].str.strip()
    
    return df_clean


def generate_quality_report(df: pd.DataFrame) -> DataQualityReport:
    """Generate a comprehensive data quality report."""
    if df.empty:
        return DataQualityReport(0, 0, 0, 0, 0, 0, 0.0)
    
    total = len(df)
    missing_emails = df["EMAIL"].isna().sum() if "EMAIL" in df.columns else 0
    missing_phones = df["Phone number"].isna().sum() if "Phone number" in df.columns else 0
    missing_students = (df["Number of Students"] == 0).sum() if "Number of Students" in df.columns else 0
    duplicates = df.duplicated().sum()
    
    required = ["Institution", "Teacher / Trainer", "EMAIL"]
    complete = df[required].notna().all(axis=1).sum()
    
    # Calculate quality score
    score = (
        (complete / total) * 40 +
        ((total - missing_emails - missing_phones) / (total * 2)) * 30 +
        ((total - duplicates) / total) * 30
    )
    
    return DataQualityReport(
        total_records=total,
        complete_records=int(complete),
        missing_emails=int(missing_emails),
        missing_phones=int(missing_phones),
        missing_students=int(missing_students),
        duplicate_records=int(duplicates),
        quality_score=min(100, max(0, score))
    )


# =============================================================================
# SAMPLE DATA GENERATOR
# =============================================================================

def generate_sample_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generate realistic sample data for demonstration."""
    
    COUNTRIES = ["Kenya", "Uganda", "Tanzania", "Rwanda", "Ethiopia",
                 "Ghana", "Nigeria", "South Africa", "Zambia", "Malawi"]
    
    LANGUAGES = ["English", "French", "Swahili", "Portuguese", "Arabic"]
    
    INSTITUTION_TEMPLATES = [
        "{country} Technical Training College",
        "{country} Institute of Technology",
        "{country} TVET Academy",
        "{country} Vocational Training Center",
        "{country} Technical Institute",
        "{country} Polytechnic College"
    ]
    
    FIRST_NAMES = ["James", "Mary", "John", "Sarah", "Peter", "Grace", "David",
                   "Ruth", "Michael", "Esther", "Daniel", "Elizabeth", "Joseph"]
    
    LAST_NAMES = ["Ochieng", "Kamau", "Njoroge", "Wanjiku", "Muthoni", "Kipchoge",
                  "Mwangi", "Otieno", "Wambui", "Kimani", "Akinyi", "Ndungu"]
    
    DOMAINS = ["Automotive Technology", "Electrical Engineering", "Mechanical Engineering",
               "Renewable Energy", "Digital Electronics", "Hydraulic Systems"]
    
    FEEDBACK = {
        "positive": ["Excellent platform with comprehensive learning materials.",
                     "Very satisfied with the hands-on simulations.",
                     "Great improvement in practical skills among students.",
                     "The interactive modules keep students engaged."],
        "neutral": ["Good platform overall, some minor improvements needed.",
                    "Students find it helpful but suggest more practice tests."],
        "negative": ["Would benefit from more local language support.",
                     "Internet connectivity challenges in rural areas."]
    }
    
    random.seed(42)
    np.random.seed(42)
    
    # Generate institutions
    institutions = {}
    for country in COUNTRIES:
        for _ in range(random.randint(2, 4)):
            name = random.choice(INSTITUTION_TEMPLATES).format(country=country)
            institutions[f"{name} - {country}"] = {
                "country": country,
                "language": random.choice(LANGUAGES),
                "domain": random.choice(DOMAINS)
            }
    
    # Generate main data
    records = []
    for _ in range(350):
        inst = random.choice(list(institutions.keys()))
        data = institutions[inst]
        teacher = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        
        records.append({
            "Institution": inst,
            "Teacher / Trainer": teacher,
            "Number of Students": random.randint(15, 180),
            "EMAIL": f"{teacher.lower().replace(' ', '.')}@example.com",
            "Phone number": f"+{random.randint(250, 275)} {random.randint(100, 999)} {random.randint(100, 999)} {random.randint(100, 999)}",
            "Language": data["language"],
            "Electude Domain": data["domain"]
        })
    
    main_df = pd.DataFrame(records)
    
    # Add some missing values
    main_df.loc[main_df.sample(15).index, "EMAIL"] = np.nan
    main_df.loc[main_df.sample(20).index, "Phone number"] = np.nan
    
    # Generate survey data
    survey_records = []
    for inst in institutions.keys():
        for _ in range(random.randint(5, 15)):
            score = np.clip(np.random.normal(3.5, 0.9), 1, 5)
            if score >= 4:
                feedback = random.choice(FEEDBACK["positive"])
            elif score >= 3:
                feedback = random.choice(FEEDBACK["neutral"])
            else:
                feedback = random.choice(FEEDBACK["negative"])
            
            survey_records.append({
                "Institution": inst,
                "Satisfaction Score": round(score, 1),
                "Feedback": feedback,
                "Respondent Type": random.choice(["Teacher", "Student", "Administrator"])
            })
    
    survey_df = pd.DataFrame(survey_records)
    
    return main_df, survey_df


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="\ud83c\udf0d Electude Africa TVET Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': f"""
        **Electude Africa TVET Analytics Dashboard**
        
        Version 2.0.0 | \u00a9 {datetime.now().year} Electude Africa
        
        Professional TVET Analytics Platform
        """
    }
)


# =============================================================================
# AUTHENTICATION
# =============================================================================

def check_password() -> bool:
    """Secure password authentication with modern UI."""
    
    def password_entered():
        """Validate password and update session state."""
        stored_password = st.secrets.get("passwords", {}).get("password", "admin") if hasattr(st, 'secrets') else "admin"
        if st.session_state.get("password") == stored_password:
            st.session_state["password_correct"] = True
            st.session_state.pop("password", None)
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="password-container">
            <div class="lock-icon">\ud83d\udd10</div>
            <h1>Authentication Required</h1>
            <p>Enter your credentials to access the dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_input(
            "Password",
            type="password",
            on_change=password_entered,
            key="password",
            placeholder="Enter your password...",
            label_visibility="collapsed"
        )
        
        if "password_correct" in st.session_state and not st.session_state.password_correct:
            st.error("\u26a0\ufe0f Invalid password. Please try again.")
    
    return False


# =============================================================================
# RENDER FUNCTIONS
# =============================================================================

def render_header():
    """Render the professional dashboard header."""
    st.markdown("""
    <div class="main-header">
        <h1>\ud83c\udf0d Electude Africa TVET Analytics</h1>
        <p class="subtitle">
            Comprehensive analytics platform for Technical and Vocational Education across Africa
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """Render the professional sidebar with filters."""
    
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h2>\ud83c\udf0d Electude Africa</h2>
            <p>Analytics Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Filters
        st.markdown("### \ud83d\udcca Data Filters")
        
        languages = sorted(df["Language"].dropna().unique().tolist()) if "Language" in df.columns else []
        language_filter = st.multiselect(
            "\ud83c\udf10 Language",
            languages,
            default=languages,
            help="Filter institutions by teaching language"
        )
        
        countries = sorted(df["Country"].dropna().unique().tolist()) if "Country" in df.columns else []
        country_filter = st.multiselect(
            "\ud83c\udff3\ufe0f Country",
            countries,
            default=countries,
            help="Filter by country"
        )
        
        st.markdown("---")
        
        # Display settings
        st.markdown("### \u2699\ufe0f Display Settings")
        show_metrics = st.checkbox("Show Key Metrics", value=True)
        show_charts = st.checkbox("Show Visualizations", value=True)
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### \ud83d\udcc8 Quick Stats")
        st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Apply filters
        filtered = df.copy()
        
        if language_filter:
            filtered = filtered[filtered["Language"].isin(language_filter)]
        if country_filter:
            filtered = filtered[filtered["Country"].isin(country_filter)]
        
        st.metric("Filtered Records", len(filtered))
        
        return filtered, {
            "show_metrics": show_metrics,
            "show_charts": show_charts
        }


def render_metrics(filtered: pd.DataFrame, survey_df: pd.DataFrame = None):
    """Render the key metrics section."""
    
    total_students = int(filtered["Number of Students"].sum()) if "Number of Students" in filtered.columns else 0
    total_teachers = filtered["Teacher / Trainer"].nunique() if "Teacher / Trainer" in filtered.columns else 0
    institutions = filtered["Institution"].nunique() if "Institution" in filtered.columns else 0
    avg_students = round(total_students / institutions, 1) if institutions > 0 else 0
    
    avg_satisfaction = "N/A"
    if survey_df is not None and not survey_df.empty and "Satisfaction Score" in survey_df.columns:
        avg_satisfaction = f"{survey_df['Satisfaction Score'].mean():.2f}"
    
    st.markdown(f"""
    <div class="metric-container">
        {get_metric_card_html("\ud83c\udf93", "Total Students", f"{total_students:,}", "students")}
        {get_metric_card_html("\ud83d\udc68\u200d\ud83c\udfeb", "Active Teachers", f"{total_teachers:,}", "teachers")}
        {get_metric_card_html("\ud83c\udfdb\ufe0f", "Institutions", f"{institutions:,}", "institutions")}
        {get_metric_card_html("\ud83d\udcca", "Avg Students/Institution", f"{avg_students:,.1f}", "avg-students")}
        {get_metric_card_html("\u2b50", "Avg. Satisfaction", avg_satisfaction if avg_satisfaction == "N/A" else f"{avg_satisfaction} / 5", "satisfaction")}
    </div>
    """, unsafe_allow_html=True)


def render_charts(filtered: pd.DataFrame):
    """Render all visualization charts."""
    
    st.markdown(get_section_header_html("\ud83d\udcca", "Students Distribution Analysis"), unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        students_by_inst = (
            filtered.groupby("Institution")["Number of Students"]
            .sum().reset_index()
            .sort_values("Number of Students", ascending=True)
        )
        
        if not students_by_inst.empty:
            fig = create_bar_chart(
                students_by_inst.tail(15),
                x="Number of Students", y="Institution",
                title="Students per Institution (Top 15)",
                color="Number of Students",
                orientation="h",
                color_scale=[THEME.primary, THEME.secondary]
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(create_empty_chart(), use_container_width=True)
    
    with col2:
        lang_dist = (
            filtered.groupby("Language")["Number of Students"]
            .sum().reset_index()
        )
        
        if not lang_dist.empty:
            fig = create_pie_chart(
                lang_dist,
                names="Language", values="Number of Students",
                title="Language Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(create_empty_chart("No language data"), use_container_width=True)
    
    # Country Distribution
    st.markdown(get_section_header_html("\ud83c\udf0d", "Distribution by Country"), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        country_dist = (
            filtered.groupby("Country").agg({
                "Number of Students": "sum",
                "Institution": "nunique"
            }).reset_index()
            .rename(columns={"Institution": "Institutions"})
            .sort_values("Number of Students", ascending=False)
        )
        
        if not country_dist.empty:
            fig = create_bar_chart(
                country_dist.head(10),
                x="Country", y="Number of Students",
                title="Students by Country (Top 10)",
                color="Number of Students",
                color_scale=[THEME.accent, THEME.danger],
                show_values=True
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(create_empty_chart(), use_container_width=True)
    
    with col2:
        teachers_by_inst = (
            filtered.groupby("Institution")["Teacher / Trainer"]
            .count().reset_index()
            .rename(columns={"Teacher / Trainer": "Teachers"})
            .sort_values("Teachers", ascending=False)
            .head(10)
        )
        
        if not teachers_by_inst.empty:
            fig = create_bar_chart(
                teachers_by_inst,
                x="Institution", y="Teachers",
                title="Teachers per Institution (Top 10)",
                color="Teachers",
                color_scale=[THEME.teal, THEME.success]
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(create_empty_chart(), use_container_width=True)


def render_survey_analysis(survey_df: pd.DataFrame, filtered: pd.DataFrame):
    """Render the user satisfaction analysis section."""
    
    st.markdown(get_section_header_html("\u2b50", "User Satisfaction Analysis"), unsafe_allow_html=True)
    
    if survey_df.empty or "Satisfaction Score" not in survey_df.columns:
        st.warning("\u26a0\ufe0f No survey data available. Upload `survey_data.csv` to enable analysis.")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        satisfaction_by_inst = (
            survey_df.groupby("Institution")["Satisfaction Score"]
            .mean().reset_index()
            .sort_values("Satisfaction Score", ascending=True)
        )
        
        fig = create_bar_chart(
            satisfaction_by_inst.tail(15),
            x="Satisfaction Score", y="Institution",
            title="Avg. Satisfaction by Institution",
            color="Satisfaction Score",
            orientation="h",
            color_scale=["#dc3545", "#ffc107", "#28a745"]
        )
        fig.update_xaxes(range=[0, 5])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=survey_df["Satisfaction Score"],
            marker_color=THEME.success,
            opacity=0.85,
            nbinsx=10
        ))
        apply_chart_style(fig, "Score Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    if "Feedback" in survey_df.columns:
        st.markdown("#### \ud83d\udcac Feedback Browser")
        search = st.text_input("\ud83d\udd0d Search feedback", placeholder="Enter keywords...")
        
        feedback_df = survey_df[["Institution", "Feedback", "Satisfaction Score"]].copy()
        if search:
            feedback_df = feedback_df[feedback_df["Feedback"].str.contains(search, case=False, na=False)]
        
        st.dataframe(feedback_df.sort_values("Satisfaction Score", ascending=False), use_container_width=True)


def render_ai_insights(filtered: pd.DataFrame, survey_df: pd.DataFrame = None):
    """Generate and render AI-powered insights."""
    
    st.markdown(get_section_header_html("\ud83e\udd16", "AI-Powered Insights"), unsafe_allow_html=True)
    
    total_students = int(filtered["Number of Students"].sum()) if "Number of Students" in filtered.columns else 0
    institutions = filtered["Institution"].nunique() if "Institution" in filtered.columns else 0
    
    students_by_inst = filtered.groupby("Institution")["Number of Students"].sum().reset_index()
    top_school = students_by_inst.loc[students_by_inst["Number of Students"].idxmax(), "Institution"] if not students_by_inst.empty else "N/A"
    top_students = int(students_by_inst["Number of Students"].max()) if not students_by_inst.empty else 0
    
    lang_dist = filtered.groupby("Language")["Number of Students"].sum().reset_index()
    most_language = lang_dist.loc[lang_dist["Number of Students"].idxmax(), "Language"] if not lang_dist.empty else "N/A"
    
    country_dist = filtered.groupby("Country")["Number of Students"].sum().reset_index()
    top_country = country_dist.loc[country_dist["Number of Students"].idxmax(), "Country"] if not country_dist.empty else "N/A"
    
    insights = [
        f"**{top_school}** leads with **{top_students:,} students** - the largest in the network.",
        f"**{most_language}** is the primary language of instruction.",
        f"The network spans **{institutions} active institutions** across Africa.",
        f"**Total reach: {total_students:,} learners** engaged through the platform.",
        f"**{top_country}** has the highest enrollment numbers."
    ]
    
    st.markdown(get_insight_box_html("Key Data Insights", insights), unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("#### \ud83d\udccb Strategic Recommendations")
    
    recommendations = [
        ("Expansion Opportunity", f"Consider expanding programs in {top_country} where demand is highest.", "medium"),
        ("Language Strategy", f"With {most_language} as the dominant language, ensure content optimization.", "medium"),
        ("Teacher Development", "Implement training programs to improve student-to-teacher ratios.", "high")
    ]
    
    for title, desc, priority in recommendations:
        priority_class = "high" if priority == "high" else "low" if priority == "low" else ""
        st.markdown(f"""
        <div class="recommendation-card">
            <span class="priority {priority_class}">{priority.upper()}</span>
            <h5>{title}</h5>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)


def render_teacher_directory(filtered: pd.DataFrame):
    """Render the searchable teacher directory."""
    
    st.markdown(get_section_header_html("\ud83d\udc68\u200d\ud83c\udfeb", "Teacher Directory"), unsafe_allow_html=True)
    
    search = st.text_input("\ud83d\udd0d Search teachers", placeholder="Enter name, institution, or email...", key="teacher_search")
    
    directory = filtered.copy()
    if search:
        mask = (
            directory["Teacher / Trainer"].str.contains(search, case=False, na=False) |
            directory["Institution"].str.contains(search, case=False, na=False) |
            directory["EMAIL"].str.contains(search, case=False, na=False)
        )
        directory = directory[mask]
    
    cols = ["Institution", "Teacher / Trainer", "EMAIL", "Phone number", "Number of Students", "Language"]
    available = [c for c in cols if c in directory.columns]
    
    if not directory.empty:
        st.dataframe(
            directory[available].sort_values("Number of Students", ascending=False),
            use_container_width=True
        )
    else:
        st.info("No teachers match your search criteria.")


def render_data_quality(df: pd.DataFrame, report: DataQualityReport):
    """Render the data quality panel."""
    
    st.markdown(get_section_header_html("\ud83e\uddf9", "Data Quality Report"), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig = create_gauge_chart(report.quality_score, "Quality Score")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Completeness Metrics")
        st.markdown(get_quality_indicator_html(
            "Missing Emails", report.missing_emails,
            "good" if report.missing_emails == 0 else "warning" if report.missing_emails < 10 else "danger"
        ), unsafe_allow_html=True)
        st.markdown(get_quality_indicator_html(
            "Missing Phones", report.missing_phones,
            "good" if report.missing_phones == 0 else "warning" if report.missing_phones < 10 else "danger"
        ), unsafe_allow_html=True)
        st.markdown(get_quality_indicator_html(
            "Duplicates", report.duplicate_records,
            "good" if report.duplicate_records == 0 else "warning" if report.duplicate_records < 5 else "danger"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown("#### Record Statistics")
        st.metric("Total Records", report.total_records)
        st.metric("Complete Records", report.complete_records)
        st.metric("Completion Rate", f"{(report.complete_records / report.total_records * 100):.1f}%" if report.total_records > 0 else "N/A")


def render_export_section(filtered: pd.DataFrame):
    """Render the data export section."""
    
    st.markdown(get_section_header_html("\ud83d\udce5", "Export Data"), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="\ud83d\udcc4 Download CSV",
            data=filtered.to_csv(index=False),
            file_name=f"electude_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        st.download_button(
            label="\ud83d\udccb Download JSON",
            data=filtered.to_json(orient="records", indent=2),
            file_name=f"electude_export_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    with col3:
        st.download_button(
            label="\ud83d\udcca Download Summary",
            data=filtered.describe(include="all").to_string(),
            file_name=f"electude_summary_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )


def render_footer():
    """Render the dashboard footer."""
    st.markdown(f"""
    <div class="dashboard-footer">
        <div class="logo">\ud83c\udf0d Electude Africa</div>
        <p>Professional TVET Analytics Platform | \u00a9 {datetime.now().year}</p>
        <p style="font-size: 0.75rem; color: #adb5bd;">
            Built with \u2764\ufe0f for African Technical Education
        </p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    
    # Check authentication
    if not check_password():
        st.stop()
    
    # Load CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Render header
    render_header()
    
    # Load or generate data
    @st.cache_data
    def load_data():
        try:
            main_df = pd.read_csv("electude_data.csv")
        except FileNotFoundError:
            main_df = None
        
        try:
            survey_df = pd.read_csv("survey_data.csv")
        except FileNotFoundError:
            survey_df = pd.DataFrame()
        
        if main_df is None:
            return generate_sample_data()
        
        return main_df, survey_df
    
    with st.spinner("Loading data..."):
        main_df, survey_df = load_data()
    
    # Clean data
    df_clean = clean_dataframe(main_df)
    quality_report = generate_quality_report(df_clean)
    
    # Render sidebar
    filtered, settings = render_sidebar(df_clean)
    
    # Main content
    if settings["show_metrics"]:
        render_metrics(filtered, survey_df)
    
    st.divider()
    
    if settings["show_charts"]:
        render_charts(filtered)
    
    st.divider()
    
    # Survey analysis
    if not survey_df.empty:
        render_survey_analysis(survey_df, filtered)
        st.divider()
    
    # AI Insights
    render_ai_insights(filtered, survey_df)
    st.divider()
    
    # Teacher directory
    render_teacher_directory(filtered)
    st.divider()
    
    # Data quality
    render_data_quality(df_clean, quality_report)
    st.divider()
    
    # Export
    render_export_section(filtered)
    
    # Footer
    render_footer()


if __name__ == "__main__":
    main()
