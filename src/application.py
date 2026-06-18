"""
Food Wastage Management System — Business Analytics Dashboard

Author: Shubham Diwakar (Portfolio Project)
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Local Food Wastage Management System Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── DESIGN TOKENS ───────────────────────────────────────────────────────────
# Corporate light theme: navy primary, teal accent, white background
NAV_BG      = "#0f172a"   # deep navy for top bar
PRIMARY     = "#1e3a5f"   # dark blue for headings
ACCENT      = "#0d9488"   # teal accent
ACCENT_LIGHT= "#ccfbf1"   # teal tint for backgrounds
SUCCESS     = "#166534"   # dark green for positive delta
WARNING     = "#92400e"   # amber for warning
DANGER      = "#991b1b"   # red for negative
CARD_BG     = "#ffffff"
PAGE_BG     = "#f6f8faea"
BORDER      = "#e2e8f0"
TEXT_PRIMARY= "#0f172a"
TEXT_MUTED  = "#64748b"

# Chart palette — calm, corporate
PALETTE = ["#1e3a5f", "#0d9488", "#3b82f6", "#7c3aed", "#5afa62", "#064e3b"]

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Global reset ── */
.stApp {{
    background-color: {PAGE_BG};
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}
.main .block-container {{
    padding: 0 2rem 3rem 2rem;
    max-width: 1400px;
}}

/* ── Top navigation bar ── */
.top-nav {{
    background: {NAV_BG};
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 56px;
    margin: 0 -2rem 1.5rem -2rem;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}}
.nav-brand {{
    color: #ffffff;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.02em;
    white-space: nowrap;
}}
.nav-brand span {{
    color: {ACCENT};
}}

/* ── Page title area ── */
.page-header {{
    padding: 0.5rem 0 1.25rem 0;
    border-bottom: 1px solid {BORDER};
    margin-bottom: 1.5rem;
}}
.page-title {{
    font-size: 22px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    margin: 0;
    letter-spacing: -0.01em;
}}
.page-subtitle {{
    font-size: 13px;
    color: {TEXT_MUTED};
    margin: 4px 0 0 0;
}}

/* ── KPI card ── */
.kpi-card {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 16px 18px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    height: 100%;
}}
.kpi-label {{
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {TEXT_MUTED};
    margin: 0;
}}
.kpi-value {{
    font-size: 28px;
    font-weight: 800;
    color: {TEXT_PRIMARY};
    line-height: 1.1;
    margin: 0;
    letter-spacing: -0.02em;
}}
.kpi-delta-pos {{
    font-size: 12px;
    color: {SUCCESS};
    font-weight: 600;
    margin: 0;
}}
.kpi-delta-neg {{
    font-size: 12px;
    color: {DANGER};
    font-weight: 600;
    margin: 0;
}}
.kpi-delta-neu {{
    font-size: 12px;
    color: {TEXT_MUTED};
    font-weight: 600;
    margin: 0;
}}
.kpi-accent-bar {{
    height: 3px;
    border-radius: 2px;
    background: {ACCENT};
    margin-top: 4px;
    width: 36px;
}}

/* ── Section label ── */
.section-label {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {TEXT_MUTED};
    margin: 0 0 8px 0;
    padding-bottom: 6px;
    border-bottom: 1px solid {BORDER};
}}

/* ── Content card ── */
.content-card {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 18px 20px 10px 20px;
    margin-bottom: 16px;
}}

/* ── Progress bar item ── */
.progress-row {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}}
.progress-label {{
    font-size: 12px;
    color: {TEXT_PRIMARY};
    min-width: 120px;
    flex-shrink: 0;
}}
.progress-track {{
    flex: 1;
    background: {BORDER};
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
}}
.progress-fill {{
    height: 100%;
    border-radius: 4px;
    background: {ACCENT};
}}
.progress-val {{
    font-size: 11px;
    color: {TEXT_MUTED};
    min-width: 40px;
    text-align: right;
}}

/* ── Alert box ── */
.alert-insight {{
    background: #eff6ff;
    border-left: 3px solid #3b82f6;
    border-radius: 0 6px 6px 0;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: 13px;
    color: {TEXT_PRIMARY};
    line-height: 1.45;
}}
.alert-warning {{
    background: #fffbeb;
    border-left: 3px solid #f59e0b;
}}
.alert-danger {{
    background: #fef2f2;
    border-left: 3px solid #ef4444;
}}
.alert-success {{
    background: #f0fdf4;
    border-left: 3px solid #22c55e;
}}

/* ── Badge ── */
.badge {{
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 9999px;
    background: {ACCENT_LIGHT};
    color: {ACCENT};
}}

/* ── Table styling ── */
.stDataFrame thead th {{
    background: #f1f5f9 !important;
    color: {TEXT_MUTED} !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 2px solid {BORDER} !important;
}}
.stDataFrame tbody td {{
    font-size: 13px !important;
    color: {TEXT_PRIMARY} !important;
}}

/* ── Streamlit overrides ── */
[data-testid="metric-container"] {{ display: none; }}
div[data-testid="stHorizontalBlock"] {{ gap: 0.75rem; }}
.stSelectbox label, .stMultiSelect label {{ font-size: 12px !important; color: {TEXT_MUTED} !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.06em; }}
.stTabs [data-baseweb="tab-list"] {{ border-bottom: 2px solid {BORDER}; background: transparent; gap: 0; }}
.stTabs [data-baseweb="tab"] {{ background: transparent; color: {TEXT_MUTED}; font-size: 13px; font-weight: 600; padding: 10px 18px; border-bottom: 2px solid transparent; margin-bottom: -2px; }}
.stTabs [aria-selected="true"] {{ color: {ACCENT} !important; border-bottom-color: {ACCENT} !important; background: transparent !important; }}
.stTabs [data-baseweb="tab-panel"] {{ padding-top: 1.2rem; }}
div[data-testid="stExpander"] > details > summary {{ font-size: 13px; font-weight: 600; color: {TEXT_PRIMARY}; }}
.stDownloadButton button {{ font-size: 12px; background: {NAV_BG}; color: white; border: none; padding: 6px 16px; border-radius: 6px; }}
.stDownloadButton button:hover {{ background: {PRIMARY}; }}
footer {{ display: none; }}
#MainMenu {{ display: none; }}

/* ── Sidebar collapse ── */
section[data-testid="stSidebar"] {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

# ─── DATA LOADING ────────────────────────────────────────────────────────────
# Resolves to the raw/ folder two levels above this script's location.
# Adjust DATA_DIR if running from a different working directory.
DATA_DIR = Path(__file__).resolve().parent.parent / "raw"

@st.cache_data(show_spinner=False)
def load_data() -> tuple[pd.DataFrame, ...]:
    claims    = pd.read_csv(DATA_DIR / "claims_data.csv")
    food      = pd.read_csv(DATA_DIR / "food_listings_data.csv")
    providers = pd.read_csv(DATA_DIR / "providers_data.csv")
    receivers = pd.read_csv(DATA_DIR / "receivers_data.csv")

    claims["Timestamp"] = pd.to_datetime(claims["Timestamp"])
    claims["Date"]      = claims["Timestamp"].dt.date
    claims["Hour"]      = claims["Timestamp"].dt.hour
    claims["DayOfWeek"] = claims["Timestamp"].dt.day_name()
    food["Expiry_Date"] = pd.to_datetime(food["Expiry_Date"])

    merged = (
        claims
        .merge(food,      on="Food_ID",     how="left")
        .merge(providers, on="Provider_ID", how="left", suffixes=("", "_prov"))
        .merge(receivers, on="Receiver_ID", how="left", suffixes=("", "_recv"))
    )
    return claims, food, providers, receivers, merged

claims, food, providers, receivers, merged = load_data()

# ─── CHART HELPERS ───────────────────────────────────────────────────────────
def clean_fig(fig: go.Figure, height: int = 300, show_legend: bool = True) -> go.Figure:
    """Apply consistent light-theme styling to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="#f8fafc",
        font=dict(color=TEXT_MUTED, size=11, family="Inter, sans-serif"),
        margin=dict(l=8, r=8, t=32, b=8),
        height=height,
        showlegend=show_legend,
        legend=dict(
            bgcolor="white",
            bordercolor=BORDER,
            borderwidth=1,
            font=dict(size=10, color=TEXT_MUTED),
        ),
        xaxis=dict(
            gridcolor="#f1f5f9",
            linecolor=BORDER,
            tickfont=dict(size=10),
            title_font=dict(size=11),
        ),
        yaxis=dict(
            gridcolor="#f1f5f9",
            linecolor=BORDER,
            tickfont=dict(size=10),
            title_font=dict(size=11),
        ),
    )
    return fig


def render_chart(fig: go.Figure) -> None:
    """Render a Plotly figure with shared config."""
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ─── KPI CARD HTML HELPER ────────────────────────────────────────────────────
def kpi_card(label: str, value: str, delta: str = "", delta_type: str = "neu") -> str:
    """Return HTML for a styled KPI card (no emojis, no Streamlit metric widget)."""
    delta_cls = f"kpi-delta-{delta_type}"
    delta_html = f'<p class="{delta_cls}">{delta}</p>' if delta else ""
    return f"""
    <div class="kpi-card">
        <p class="kpi-label">{label}</p>
        <p class="kpi-value">{value}</p>
        {delta_html}
        <div class="kpi-accent-bar"></div>
    </div>
    """


def section_label(text: str) -> None:
    st.markdown(f'<p class="section-label">{text}</p>', unsafe_allow_html=True)


def insight(text: str, kind: str = "info") -> None:
    cls = {"info": "alert-insight", "warn": "alert-insight alert-warning",
           "danger": "alert-insight alert-danger", "ok": "alert-insight alert-success"}.get(kind, "alert-insight")
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)


# ─── TOP NAVIGATION BAR ──────────────────────────────────────────────────────
st.markdown("""
<div class="top-nav">
    <div class="nav-brand">Local Food <span>Wastage Management System</span></div>
</div>
""", unsafe_allow_html=True)

# Navigation tabs + global filters on the same row
nav_col, _, filter_col1, filter_col2 = st.columns([3, 0.5, 2, 2])

with nav_col:
    page = st.selectbox(
        "Section",
        ["Executive Summary", "Supply & Providers", "Demand & Receivers",
         "Food Intelligence", "Geographic Analysis", "Operations & Efficiency", "Data Explorer"],
        label_visibility="collapsed",
    )

with filter_col1:
    status_filter = st.multiselect(
        "Claim Status",
        options=claims["Status"].unique().tolist(),
        default=claims["Status"].unique().tolist(),
        placeholder="All statuses",
    )

with filter_col2:
    food_type_filter = st.multiselect(
        "Food Type",
        options=food["Food_Type"].unique().tolist(),
        default=food["Food_Type"].unique().tolist(),
        placeholder="All food types",
    )

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ─── APPLY GLOBAL FILTERS ────────────────────────────────────────────────────
f_claims  = merged[
    merged["Status"].isin(status_filter) &
    merged["Food_Type"].isin(food_type_filter)
]
f_food    = food[food["Food_Type"].isin(food_type_filter)]
f_merged  = merged[merged["Food_Type"].isin(food_type_filter)]

# ─── COMPUTED KPIs ────────────────────────────────────────────────────────────
total_qty     = int(f_food["Quantity"].sum())
total_claims  = len(f_claims)
completed_n   = int((f_claims["Status"] == "Completed").sum())
cancelled_n   = int((f_claims["Status"] == "Cancelled").sum())
pending_n     = int((f_claims["Status"] == "Pending").sum())
claimed_qty   = int(f_food[f_food["Food_ID"].isin(
    f_claims[f_claims["Status"] == "Completed"]["Food_ID"]
)]["Quantity"].sum())
success_rate  = round(completed_n / max(total_claims, 1) * 100, 1)
rescue_rate   = round(claimed_qty / max(total_qty, 1) * 100, 1)
cancel_rate   = round(cancelled_n / max(total_claims, 1) * 100, 1)
pending_rate  = round(pending_n   / max(total_claims, 1) * 100, 1)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════
if page == "Executive Summary":
    st.markdown("""
    <div class="page-header">
        <p class="page-title">Executive Summary</p>
        <p class="page-subtitle">Platform-wide performance overview · March 2025</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 1: KPI cards ──────────────────────────────────────────────────
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.markdown(kpi_card("Total Food Units", f"{total_qty:,}", "All listings"), unsafe_allow_html=True)
    k2.markdown(kpi_card("Units Rescued", f"{claimed_qty:,}", f"{rescue_rate}% of supply", "pos"), unsafe_allow_html=True)
    k3.markdown(kpi_card("Claim Success Rate", f"{success_rate}%", f"{completed_n:,} completed", "pos"), unsafe_allow_html=True)
    k4.markdown(kpi_card("Cancellation Rate", f"{cancel_rate}%", f"{cancelled_n:,} cancelled", "neg"), unsafe_allow_html=True)
    k5.markdown(kpi_card("Active Providers", f"{len(providers):,}", "Food donors"), unsafe_allow_html=True)
    k6.markdown(kpi_card("Active Receivers", f"{len(receivers):,}", "NGOs & individuals"), unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Row 2: Claim funnel + status trend + insights ─────────────────────
    col_left, col_mid, col_right = st.columns([1.1, 1.4, 1])

    with col_left:
        section_label("Claim Outcome Funnel")
        funnel = go.Figure(go.Funnel(
            y=["Total Claims", "Completed", "Pending", "Cancelled"],
            x=[total_claims, completed_n, pending_n, cancelled_n],
            marker=dict(color=[PRIMARY, ACCENT, "#b45309", DANGER]),
            textinfo="value+percent total",
            textfont=dict(size=12),
            connector=dict(line=dict(color=BORDER, width=1)),
        ))
        funnel.update_layout(
            paper_bgcolor="white", plot_bgcolor="white",
            margin=dict(l=0, r=0, t=28, b=0), height=260,
            font=dict(color=TEXT_MUTED, size=11),
        )
        render_chart(funnel)

    with col_mid:
        section_label("Daily Claim Volume by Status")
        ts = f_claims.groupby(["Date", "Status"]).size().reset_index(name="Count")
        fig = px.area(
            ts, x="Date", y="Count", color="Status",
            color_discrete_map={
                "Completed": ACCENT,
                "Cancelled": "#ef4444",
                "Pending":   "#f59e0b",
            },
            line_group="Status",
        )
        fig.update_traces(opacity=0.75)
        render_chart(clean_fig(fig, height=260))

    with col_right:
        section_label("Key Insights")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        insight(f"Only <strong>{rescue_rate}%</strong> of listed food is successfully rescued — significant room to improve.", "warn")
        insight(f"<strong>{cancel_rate}%</strong> of claims are cancelled, indicating systemic friction in the matching process.", "danger")
        insight(f"<strong>{pending_n:,}</strong> claims remain unresolved — SLA tracking could accelerate resolution.", "info")
        insight(f"Restaurants and supermarkets are top contributors. Formalising partnerships can boost supply.", "ok")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Row 3: Provider type performance + Receiver type demand ───────────
    col_a, col_b = st.columns(2)

    with col_a:
        section_label("Provider Type — Claim Status Breakdown")
        cross = f_merged.groupby(["Provider_Type", "Status"]).size().reset_index(name="Count")
        fig = px.bar(
            cross, x="Provider_Type", y="Count", color="Status", barmode="group",
            color_discrete_map={"Completed": ACCENT, "Cancelled": "#ef4444", "Pending": "#f59e0b"},
        )
        fig.update_layout(xaxis_title="", yaxis_title="Claims", legend_title="")
        render_chart(clean_fig(fig, height=270))

    with col_b:
        section_label("Rescue Rate Progress by Food Type")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        for ft in f_food["Food_Type"].unique():
            food_ids = f_food[f_food["Food_Type"] == ft]["Food_ID"]
            comp_ids = f_claims[f_claims["Status"] == "Completed"]["Food_ID"]
            qty_total = int(f_food[f_food["Food_Type"] == ft]["Quantity"].sum())
            qty_rescued = int(f_food[f_food["Food_ID"].isin(comp_ids) & (f_food["Food_Type"] == ft)]["Quantity"].sum())
            rate = round(qty_rescued / max(qty_total, 1) * 100, 1)
            st.markdown(f"""
            <div class="progress-row">
                <span class="progress-label">{ft}</span>
                <div class="progress-track">
                    <div class="progress-fill" style="width:{rate}%"></div>
                </div>
                <span class="progress-val">{rate}%</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        section_label("Meal Type Supply Distribution")
        mt = f_food.groupby("Meal_Type")["Quantity"].sum().reset_index().sort_values("Quantity")
        fig = px.bar(
            mt, x="Quantity", y="Meal_Type", orientation="h",
            color_discrete_sequence=[PRIMARY],
        )
        fig.update_layout(xaxis_title="Units", yaxis_title="")
        render_chart(clean_fig(fig, height=180, show_legend=False))


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 2 — SUPPLY & PROVIDERS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Supply & Providers":
    st.markdown("""
    <div class="page-header">
        <p class="page-title">Supply & Providers</p>
        <p class="page-subtitle">Donor analytics, contribution trends, and type breakdown</p>
    </div>
    """, unsafe_allow_html=True)

    avg_qty  = f_food.groupby("Provider_ID")["Quantity"].sum().mean()
    top_type = f_food["Provider_Type"].value_counts().idxmax()
    top_city_supply = f_food.groupby("Location")["Quantity"].sum().idxmax()

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card("Total Providers",   f"{len(providers):,}", "Active donors"), unsafe_allow_html=True)
    k2.markdown(kpi_card("Total Units Donated", f"{total_qty:,}", "Across all types"), unsafe_allow_html=True)
    k3.markdown(kpi_card("Avg Units / Provider", f"{avg_qty:.0f}", "Per donor"), unsafe_allow_html=True)
    k4.markdown(kpi_card("Top Provider Type", top_type, "By volume"), unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Contribution Analysis", "Type Breakdown", "Top Donors"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            section_label("Top 12 Providers by Donation Volume")
            top_prov = (
                f_food.groupby("Provider_ID")["Quantity"].sum()
                .reset_index().nlargest(12, "Quantity")
                .merge(providers[["Provider_ID", "Name", "Type"]], on="Provider_ID")
            )
            fig = px.bar(
                top_prov.sort_values("Quantity"),
                x="Quantity", y="Name", orientation="h",
                color="Type", color_discrete_sequence=PALETTE,
            )
            fig.update_layout(yaxis_title="", xaxis_title="Units Donated", legend_title="Type")
            render_chart(clean_fig(fig, height=360))

        with c2:
            section_label("Provider Type — Supply vs. Claim Success")
            ptype_supply = f_food.groupby("Provider_Type")["Quantity"].sum().reset_index()
            ptype_supply.columns = ["Provider_Type", "Supply"]
            ptype_comp = (
                f_merged[f_merged["Status"] == "Completed"]
                .groupby("Provider_Type").size().reset_index(name="Completed")
            )
            ptype_all = f_merged.groupby("Provider_Type").size().reset_index(name="Total")
            ptype_merged = ptype_supply.merge(ptype_comp, on="Provider_Type", how="left")
            ptype_merged = ptype_merged.merge(ptype_all, on="Provider_Type", how="left").fillna(0)
            ptype_merged["Success_Rate"] = (ptype_merged["Completed"] / ptype_merged["Total"].clip(lower=1) * 100).round(1)

            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(
                x=ptype_merged["Provider_Type"], y=ptype_merged["Supply"],
                name="Units Donated", marker_color=PRIMARY, opacity=0.85,
            ), secondary_y=False)
            fig.add_trace(go.Scatter(
                x=ptype_merged["Provider_Type"], y=ptype_merged["Success_Rate"],
                name="Success Rate %", mode="lines+markers",
                line=dict(color=ACCENT, width=2), marker=dict(size=8),
            ), secondary_y=True)
            fig.update_layout(
                paper_bgcolor="white", plot_bgcolor="#f8fafc",
                font=dict(color=TEXT_MUTED, size=11), legend_title="",
                margin=dict(l=8, r=8, t=32, b=8), height=360,
                yaxis=dict(title="Units Donated", gridcolor="#f1f5f9"),
                yaxis2=dict(title="Success Rate %", range=[0, 100]),
                xaxis=dict(title=""),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            section_label("Supply Volume by Provider Type")
            ptype = f_food.groupby("Provider_Type")["Quantity"].sum().sort_values(ascending=True).reset_index()
            fig = px.bar(
                ptype, x="Quantity", y="Provider_Type", orientation="h",
                color="Provider_Type", color_discrete_sequence=PALETTE,
            )
            fig.update_layout(showlegend=False, xaxis_title="Total Units", yaxis_title="")
            render_chart(clean_fig(fig, height=260, show_legend=False))

        with c2:
            section_label("Provider Type — Claim Status Stack")
            ps = f_merged.groupby(["Provider_Type", "Status"]).size().reset_index(name="Count")
            fig = px.bar(
                ps, x="Provider_Type", y="Count", color="Status", barmode="stack",
                color_discrete_map={"Completed": ACCENT, "Cancelled": "#ef4444", "Pending": "#f59e0b"},
            )
            fig.update_layout(xaxis_title="", yaxis_title="Claims", legend_title="")
            render_chart(clean_fig(fig, height=260))

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        section_label("Food Type Mix by Provider Type")
        hm_data = f_food.groupby(["Provider_Type", "Food_Type"])["Quantity"].sum().reset_index()
        pivot = hm_data.pivot(index="Provider_Type", columns="Food_Type", values="Quantity").fillna(0)
        fig = px.imshow(
            pivot, color_continuous_scale=[[0,"#f8fafc"],[1, ACCENT]],
            text_auto=True, aspect="auto",
        )
        fig.update_coloraxes(showscale=False)
        fig.update_layout(margin=dict(l=0,r=0,t=32,b=0))
        render_chart(clean_fig(fig, height=200, show_legend=False))

    with tab3:
        section_label("Top 20 Providers — Ranked by Donation Volume")
        tbl = (
            f_food.groupby("Provider_ID")["Quantity"].sum().reset_index()
            .merge(providers, on="Provider_ID").nlargest(20, "Quantity")
            [["Name", "Type", "City", "Quantity"]]
            .rename(columns={"Quantity": "Units Donated"})
            .reset_index(drop=True)
        )
        tbl.index = tbl.index + 1
        c1, c2 = st.columns([3, 1])
        with c1:
            st.dataframe(tbl, use_container_width=True)
        with c2:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            insight("Top providers are distributed across all four types. Establishing formal SLAs with top-10 donors could improve consistency.", "info")
        col_dl, _ = st.columns([1, 4])
        with col_dl:
            st.download_button(
                "Download Table (CSV)",
                data=tbl.to_csv(index=False),
                file_name="top_providers.csv",
                mime="text/csv",
            )


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 3 — DEMAND & RECEIVERS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Demand & Receivers":
    st.markdown("""
    <div class="page-header">
        <p class="page-title">Demand & Receivers</p>
        <p class="page-subtitle">Claim behaviour, segmentation, and success rates across receiver organisations</p>
    </div>
    """, unsafe_allow_html=True)

    top_recv_type = f_merged["Type"].value_counts().idxmax() if "Type" in f_merged.columns else "NGO"
    recv_success = (
        f_merged.groupby("Receiver_ID")
        .agg(total=("Claim_ID","count"), comp=("Status", lambda x: (x=="Completed").sum()))
        .assign(rate=lambda d: d.comp/d.total.clip(lower=1)*100)
    )
    avg_success = recv_success["rate"].mean()

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card("Total Receivers", f"{len(receivers):,}", "Registered"), unsafe_allow_html=True)
    k2.markdown(kpi_card("Total Claims", f"{total_claims:,}", "All statuses"), unsafe_allow_html=True)
    k3.markdown(kpi_card("Avg Receiver Success", f"{avg_success:.1f}%", "Completion rate"), unsafe_allow_html=True)
    k4.markdown(kpi_card("Top Receiver Segment", top_recv_type, "By claim count"), unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        section_label("Claim Volume & Success by Receiver Type")
        rt = f_merged.groupby(["Type", "Status"]).size().reset_index(name="Count")
        fig = px.bar(
            rt, x="Type", y="Count", color="Status", barmode="group",
            color_discrete_map={"Completed": ACCENT, "Cancelled": "#ef4444", "Pending": "#f59e0b"},
        )
        fig.update_layout(xaxis_title="", yaxis_title="Claims", legend_title="")
        render_chart(clean_fig(fig, height=290))

    with col2:
        section_label("Top 10 Receivers — Completed Claims")
        top_recv = (
            f_merged[f_merged["Status"] == "Completed"]
            .groupby("Receiver_ID").size().reset_index(name="Completed")
            .merge(receivers, on="Receiver_ID")
            .nlargest(10, "Completed")[["Name", "Type", "City", "Completed"]]
        )
        fig = px.bar(
            top_recv.sort_values("Completed"),
            x="Completed", y="Name", orientation="h",
            color="Type", color_discrete_sequence=PALETTE,
        )
        fig.update_layout(xaxis_title="Completed Claims", yaxis_title="", legend_title="Type")
        render_chart(clean_fig(fig, height=290))

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    section_label("Receiver Performance Table")
    recv_tbl = (
        f_merged.groupby("Receiver_ID")
        .agg(Total_Claims=("Claim_ID","count"),
             Completed=("Status", lambda x: (x=="Completed").sum()),
             Cancelled=("Status", lambda x: (x=="Cancelled").sum()))
        .reset_index()
        .merge(receivers, on="Receiver_ID")
        .assign(Success_Rate=lambda d: (d["Completed"]/d["Total_Claims"].clip(lower=1)*100).round(1))
        .nlargest(25, "Total_Claims")
        [["Name", "Type", "City", "Total_Claims", "Completed", "Cancelled", "Success_Rate"]]
        .rename(columns={"Success_Rate":"Success %", "Total_Claims":"Total"})
        .reset_index(drop=True)
    )
    recv_tbl.index = recv_tbl.index + 1
    st.dataframe(recv_tbl, use_container_width=True)
    col_dl, _ = st.columns([1.2, 5])
    with col_dl:
        st.download_button("Download Table (CSV)", recv_tbl.to_csv(index=False),
                           "receiver_performance.csv", "text/csv")


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 4 — FOOD INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Food Intelligence":
    st.markdown("""
    <div class="page-header">
        <p class="page-title">Food Intelligence</p>
        <p class="page-subtitle">Dietary composition, meal type analysis, and supply distribution</p>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card("Total Units",         f"{total_qty:,}", "Listed"), unsafe_allow_html=True)
    k2.markdown(kpi_card("Unique Food Items",   f"{f_food['Food_Name'].nunique():,}", "Distinct items"), unsafe_allow_html=True)
    k3.markdown(kpi_card("Avg Qty / Listing",   f"{f_food['Quantity'].mean():.1f}", "Units per entry"), unsafe_allow_html=True)
    k4.markdown(kpi_card("Largest Single Batch",f"{f_food['Quantity'].max():,} units","Max listing"), unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Type & Meal Analysis", "Top Items", "Quantity Distribution"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            section_label("Dietary Type — Total Supply")
            ft = f_food.groupby("Food_Type")["Quantity"].sum().sort_values(ascending=True).reset_index()
            fig = px.bar(ft, x="Quantity", y="Food_Type", orientation="h",
                         color_discrete_sequence=[PRIMARY])
            fig.update_layout(xaxis_title="Total Units", yaxis_title="")
            render_chart(clean_fig(fig, height=240, show_legend=False))

        with c2:
            section_label("Meal Type — Total Supply")
            mt = f_food.groupby("Meal_Type")["Quantity"].sum().sort_values(ascending=True).reset_index()
            fig = px.bar(mt, x="Quantity", y="Meal_Type", orientation="h",
                         color_discrete_sequence=[ACCENT])
            fig.update_layout(xaxis_title="Total Units", yaxis_title="")
            render_chart(clean_fig(fig, height=240, show_legend=False))

        section_label("Food Type x Meal Type — Quantity Heatmap")
        hm = f_food.groupby(["Food_Type","Meal_Type"])["Quantity"].sum().reset_index()
        pivot = hm.pivot(index="Food_Type", columns="Meal_Type", values="Quantity").fillna(0)
        fig = px.imshow(pivot, color_continuous_scale=[[0,"#f8fafc"],[1,ACCENT]],
                        text_auto=True, aspect="auto")
        fig.update_coloraxes(showscale=False)
        render_chart(clean_fig(fig, height=200, show_legend=False))

    with tab2:
        c1, c2 = st.columns([2, 1])
        with c1:
            section_label("Top 15 Food Items by Total Quantity")
            top_items = f_food.groupby("Food_Name")["Quantity"].sum().nlargest(15).sort_values().reset_index()
            fig = px.bar(top_items, x="Quantity", y="Food_Name", orientation="h",
                         color_discrete_sequence=[PRIMARY])
            fig.update_layout(xaxis_title="Total Units", yaxis_title="")
            render_chart(clean_fig(fig, height=380, show_legend=False))
        with c2:
            section_label("Top Items Summary")
            top5 = f_food.groupby("Food_Name")["Quantity"].sum().nlargest(5).reset_index()
            top5.columns = ["Item", "Units"]
            top5 = top5.reset_index(drop=True)
            top5.index = top5.index + 1
            st.dataframe(top5, use_container_width=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            insight("Bread, Rice, and Soup consistently appear as high-volume donations. Targeted receiver matching for these items could improve rescue rates.", "ok")

    with tab3:
        section_label("Listing Quantity Distribution")
        fig = px.histogram(f_food, x="Quantity", nbins=30,
                           color_discrete_sequence=[ACCENT])
        fig.update_traces(marker_line_color=BORDER, marker_line_width=1)
        fig.update_layout(xaxis_title="Quantity per Listing", yaxis_title="Number of Listings", bargap=0.04)
        render_chart(clean_fig(fig, height=280, show_legend=False))

        c1, c2, c3 = st.columns(3)
        for col, label, val in [
            (c1, "Median Listing Size", f"{f_food['Quantity'].median():.0f} units"),
            (c2, "75th Percentile",     f"{f_food['Quantity'].quantile(0.75):.0f} units"),
            (c3, "Standard Deviation",  f"{f_food['Quantity'].std():.1f}"),
        ]:
            col.markdown(kpi_card(label, val), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 5 — GEOGRAPHIC ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Geographic Analysis":
    st.markdown("""
    <div class="page-header">
        <p class="page-title">Geographic Analysis</p>
        <p class="page-subtitle">City-level supply surplus, demand concentration, and regional coverage</p>
    </div>
    """, unsafe_allow_html=True)

    top_supply_city  = f_food.groupby("Location")["Quantity"].sum().idxmax()
    top_demand_city  = f_merged.groupby("Location").size().idxmax()
    city_count       = f_food["Location"].nunique()

    k1, k2, k3 = st.columns(3)
    k1.markdown(kpi_card("Cities with Listings", f"{city_count:,}", "Supply footprint"), unsafe_allow_html=True)
    k2.markdown(kpi_card("Highest Supply City",  top_supply_city, "By units donated"), unsafe_allow_html=True)
    k3.markdown(kpi_card("Highest Demand City",  top_demand_city, "By claim count"), unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Supply vs Demand — side by side
    col1, col2 = st.columns(2)
    with col1:
        section_label("Top 15 Cities — Food Supply")
        cs = f_food.groupby("Location")["Quantity"].sum().nlargest(15).sort_values().reset_index()
        cs.columns = ["City","Supply"]
        fig = px.bar(cs, x="Supply", y="City", orientation="h",
                     color="Supply", color_continuous_scale=[[0,"#e0f2fe"],[1,PRIMARY]])
        fig.update_coloraxes(showscale=False)
        fig.update_layout(xaxis_title="Units", yaxis_title="")
        render_chart(clean_fig(fig, height=400, show_legend=False))

    with col2:
        section_label("Top 15 Cities — Claim Demand")
        cd = f_merged.groupby("Location").size().nlargest(15).sort_values().reset_index()
        cd.columns = ["City","Claims"]
        fig = px.bar(cd, x="Claims", y="City", orientation="h",
                     color="Claims", color_continuous_scale=[[0,ACCENT_LIGHT],[1,ACCENT]])
        fig.update_coloraxes(showscale=False)
        fig.update_layout(xaxis_title="Claims", yaxis_title="")
        render_chart(clean_fig(fig, height=400, show_legend=False))

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section_label("Supply vs. Demand — Top 20 Cities (Grouped Comparison)")

    supply_top = f_food.groupby("Location")["Quantity"].sum().nlargest(20).reset_index()
    supply_top.columns = ["City","Supply"]
    demand_all = f_merged.groupby("Location").size().reset_index()
    demand_all.columns = ["City","Demand"]
    svd = supply_top.merge(demand_all, on="City", how="left").fillna(0).sort_values("Supply", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Supply (Units)", y=svd["City"], x=svd["Supply"],
                         orientation="h", marker_color=PRIMARY, opacity=0.85))
    fig.add_trace(go.Bar(name="Demand (Claims)", y=svd["City"], x=svd["Demand"],
                         orientation="h", marker_color=ACCENT, opacity=0.85))
    fig.update_layout(barmode="group", xaxis_title="Volume", yaxis_title="", legend_title="")
    render_chart(clean_fig(fig, height=420))


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 6 — OPERATIONS & EFFICIENCY
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Operations & Efficiency":
    st.markdown("""
    <div class="page-header">
        <p class="page-title">Operations & Efficiency</p>
        <p class="page-subtitle">Claim pipeline health, cancellation patterns, and efficiency gauges</p>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card("Completed Claims",  f"{completed_n:,}", f"{success_rate}% success rate",  "pos"), unsafe_allow_html=True)
    k2.markdown(kpi_card("Pending Claims",    f"{pending_n:,}",   f"{pending_rate}% unresolved",     "neu"), unsafe_allow_html=True)
    k3.markdown(kpi_card("Cancelled Claims",  f"{cancelled_n:,}", f"{cancel_rate}% cancellation",   "neg"), unsafe_allow_html=True)
    k4.markdown(kpi_card("Food Rescue Rate",  f"{rescue_rate}%",  "Of total supply rescued",        "pos"), unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Efficiency gauges + funnel
    col_g, col_f = st.columns([1, 1])

    with col_g:
        section_label("Efficiency Gauges")
        fig = make_subplots(rows=1, cols=2, specs=[[{"type":"indicator"},{"type":"indicator"}]])
        for i, (val, title, color) in enumerate([
            (success_rate, "Claim Success Rate", ACCENT),
            (rescue_rate,  "Food Rescue Rate",   PRIMARY),
        ], 1):
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=val,
                title={"text": title, "font": {"color": TEXT_MUTED, "size": 12}},
                number={"font": {"color": TEXT_PRIMARY, "size": 28}, "suffix":"%"},
                gauge={
                    "axis": {"range": [0,100], "tickcolor": TEXT_MUTED},
                    "bar":  {"color": color},
                    "bgcolor": "#f1f5f9",
                    "bordercolor": BORDER,
                    "steps": [{"range":[0,50],"color":"#f8fafc"},{"range":[50,100],"color":"#f0fdf4"}],
                },
            ), row=1, col=i)
        fig.update_layout(paper_bgcolor="white", height=240,
                          margin=dict(l=16,r=16,t=48,b=8),
                          font=dict(color=TEXT_MUTED))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with col_f:
        section_label("Claim Status Funnel")
        fig = go.Figure(go.Funnel(
            y=["Total Claims","Completed","Pending","Cancelled"],
            x=[total_claims, completed_n, pending_n, cancelled_n],
            marker=dict(color=[PRIMARY, ACCENT, "#b45309", DANGER]),
            textinfo="value+percent total",
            textfont=dict(size=12),
            connector=dict(line=dict(color=BORDER)),
        ))
        fig.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                          margin=dict(l=0,r=0,t=32,b=0), height=240,
                          font=dict(color=TEXT_MUTED, size=11))
        render_chart(fig)

    # Time-series + cancellation breakdown
    col1, col2 = st.columns(2)
    with col1:
        section_label("Daily Claim Status — Time Series")
        ts = f_claims.groupby(["Date","Status"]).size().reset_index(name="Count")
        fig = px.line(ts, x="Date", y="Count", color="Status",
                      color_discrete_map={"Completed":ACCENT,"Cancelled":"#ef4444","Pending":"#f59e0b"})
        fig.update_traces(line_width=2)
        fig.update_layout(xaxis_title="", yaxis_title="Claims", legend_title="")
        render_chart(clean_fig(fig, height=260))

    with col2:
        section_label("Cancellations by Provider Type")
        canc = (f_merged[f_merged["Status"]=="Cancelled"]
                .groupby("Provider_Type").size().reset_index(name="Cancellations"))
        fig = px.bar(canc, x="Provider_Type", y="Cancellations",
                     color_discrete_sequence=[DANGER])
        fig.update_layout(xaxis_title="", yaxis_title="Cancellations", showlegend=False)
        render_chart(clean_fig(fig, height=260, show_legend=False))

    # Hourly heatmap
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section_label("Claim Activity by Hour of Day")
    hourly = f_claims.groupby("Hour").size().reset_index(name="Count")
    fig = px.bar(hourly, x="Hour", y="Count", color_discrete_sequence=[PRIMARY])
    fig.update_layout(xaxis_title="Hour of Day (0–23)", yaxis_title="Claim Count",
                      xaxis=dict(tickmode="linear", dtick=1))
    render_chart(clean_fig(fig, height=220, show_legend=False))


# ═══════════════════════════════════════════════════════════════════════════
# PAGE 7 — DATA EXPLORER
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Data Explorer":
    st.markdown("""
    <div class="page-header">
        <p class="page-title">Data Explorer</p>
        <p class="page-subtitle">Searchable, filterable view of all claim records with download capability</p>
    </div>
    """, unsafe_allow_html=True)

    # Additional drill-down filters
    fa, fb, fc = st.columns(3)
    with fa:
        ptype_filter = st.multiselect("Provider Type",
            options=sorted(f_merged["Provider_Type"].dropna().unique()),
            default=sorted(f_merged["Provider_Type"].dropna().unique()),
            placeholder="All provider types")
    with fb:
        rtype_filter = st.multiselect("Receiver Type",
            options=sorted(f_merged["Type"].dropna().unique()),
            default=sorted(f_merged["Type"].dropna().unique()),
            placeholder="All receiver types")
    with fc:
        city_opts = sorted(f_merged["Location"].dropna().unique())
        city_filter = st.multiselect("City", options=city_opts,
                                     default=city_opts, placeholder="All cities")

    display_cols = ["Claim_ID","Status","Food_Name","Quantity","Food_Type",
                    "Meal_Type","Provider_Type","Location","Type","Timestamp"]
    avail = [c for c in display_cols if c in f_merged.columns]

    explorer_df = f_merged[
        f_merged["Provider_Type"].isin(ptype_filter) &
        f_merged["Type"].isin(rtype_filter) &
        f_merged["Location"].isin(city_filter)
    ][avail].rename(columns={"Type":"Receiver_Type"}).reset_index(drop=True)

    st.markdown(f"<p style='font-size:12px;color:{TEXT_MUTED};margin-bottom:8px'>"
                f"Showing <strong>{len(explorer_df):,}</strong> records</p>",
                unsafe_allow_html=True)

    st.dataframe(explorer_df, use_container_width=True, hide_index=True)

    col_dl, col_s, _ = st.columns([1.2, 1.2, 4])
    with col_dl:
        st.download_button(
            "Download Filtered Data (CSV)",
            data=explorer_df.to_csv(index=False),
            file_name="food_rescue_export.csv",
            mime="text/csv",
        )
    with col_s:
        st.markdown(f"<p style='font-size:12px;color:{TEXT_MUTED};padding-top:8px'>"
                    f"Total: {len(explorer_df):,} rows</p>", unsafe_allow_html=True)

    # Summary stats for filtered set
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    with st.expander("Filtered Dataset — Summary Statistics"):
        num_cols = explorer_df.select_dtypes("number").columns.tolist()
        if num_cols:
            st.dataframe(explorer_df[num_cols].describe().round(2), use_container_width=True)
        else:
            st.info("No numeric columns in current selection.")


# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid {BORDER};
    display: flex;
    justify-content: space-between;
    align-items: center;
">
    <span style="font-size:12px;color:{TEXT_MUTED};">
        Local Food Wastage Management System &middot; Shubham Diwakar Portfolio Project
    </span>
    <span style="font-size:12px;color:{TEXT_MUTED};">
        Built with Streamlit &amp; Plotly &middot; Date: June 2026
    </span>
</div>
""", unsafe_allow_html=True)
