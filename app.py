import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from groq import Groq
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

st.set_page_config(
    page_title="NexPay Analytics | Payments Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.stApp { background: #ffffff; }

.top-nav {
    background: #ffffff;
    border-bottom: 2px solid #f1f5f9;
    padding: 0 48px;
    height: 68px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: -1rem -1rem 0 -1rem;
    box-shadow: 0 1px 0 #f1f5f9;
}
.nav-brand { display: flex; align-items: center; gap: 14px; }
.nav-logo-wrap {
    display: flex; align-items: center; gap: 10px;
}
.nav-logo {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 14px rgba(99,102,241,0.35);
}
.nav-logo svg { width: 22px; height: 22px; }
.nav-name {
    font-size: 1.15rem; font-weight: 800; color: #0f172a;
    letter-spacing: -0.4px;
}
.nav-tagline { font-size: 0.7rem; color: #94a3b8; font-weight: 400; margin-top: 1px; }
.nav-right { display: flex; align-items: center; gap: 14px; }
.nav-live {
    display: flex; align-items: center; gap: 6px;
    background: #f0fdf4; border: 1px solid #bbf7d0;
    border-radius: 20px; padding: 5px 14px;
    font-size: 0.72rem; color: #15803d; font-weight: 600;
}
.live-dot { width: 7px; height: 7px; background: #22c55e; border-radius: 50%; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }
.nav-date { font-size: 0.72rem; color: #94a3b8; }

.hero {
    padding: 48px 0 36px 0;
    border-bottom: 1px solid #f8fafc;
    margin-bottom: 36px;
}
.hero-label {
    display: inline-flex; align-items: center; gap: 6px;
    background: #eff6ff; border: 1px solid #dbeafe;
    border-radius: 20px; padding: 5px 14px;
    font-size: 0.72rem; font-weight: 600; color: #2563eb;
    margin-bottom: 16px;
}
.hero-title {
    font-size: 2.4rem; font-weight: 900; color: #0f172a;
    letter-spacing: -1px; line-height: 1.1; margin-bottom: 14px;
}
.hero-title span { color: #6366f1; }
.hero-desc { font-size: 0.95rem; color: #64748b; line-height: 1.7; max-width: 560px; margin-bottom: 28px; }
.hero-pills { display: flex; gap: 10px; flex-wrap: wrap; }
.hero-pill {
    background: #f8fafc; border: 1.5px solid #e2e8f0;
    border-radius: 20px; padding: 6px 16px;
    font-size: 0.75rem; color: #475569; font-weight: 500;
}

.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 18px; margin-bottom: 32px; }
.kpi-card {
    background: white; border-radius: 18px;
    padding: 24px; border: 1.5px solid #f1f5f9;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    position: relative; overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #6366f1, #818cf8);
    border-radius: 18px 18px 0 0;
}
.kpi-card.g::before { background: linear-gradient(90deg, #22c55e, #4ade80); }
.kpi-card.p::before { background: linear-gradient(90deg, #a855f7, #c084fc); }
.kpi-card.o::before { background: linear-gradient(90deg, #f97316, #fb923c); }
.kpi-icon-box {
    width: 42px; height: 42px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 16px;
}
.kpi-icon-box.blue { background: #eff6ff; }
.kpi-icon-box.green { background: #f0fdf4; }
.kpi-icon-box.purple { background: #faf5ff; }
.kpi-icon-box.orange { background: #fff7ed; }
.kpi-label { font-size: 0.7rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.7px; margin-bottom: 6px; }
.kpi-value { font-size: 1.85rem; font-weight: 800; color: #0f172a; letter-spacing: -0.6px; line-height: 1; }
.kpi-meta { font-size: 0.72rem; color: #64748b; margin-top: 8px; font-weight: 500; }

.card {
    background: white; border-radius: 16px;
    border: 1.5px solid #f1f5f9;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    overflow: hidden; margin-bottom: 20px;
}
.card-head {
    padding: 16px 22px; background: #fafbfc;
    border-bottom: 1px solid #f1f5f9;
    display: flex; justify-content: space-between; align-items: center;
}
.card-head-title { font-size: 0.85rem; font-weight: 700; color: #0f172a; }
.card-head-sub { font-size: 0.72rem; color: #94a3b8; margin-top: 2px; }
.card-tag {
    background: white; border: 1px solid #e2e8f0;
    border-radius: 8px; padding: 4px 10px;
    font-size: 0.68rem; color: #64748b;
}

.tbl { width: 100%; border-collapse: collapse; }
.tbl th {
    font-size: 0.68rem; font-weight: 600; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.5px;
    padding: 10px 16px; border-bottom: 1px solid #f1f5f9;
    text-align: left; background: #fafbfc;
}
.tbl td { padding: 11px 16px; border-bottom: 1px solid #f8fafc; font-size: 0.82rem; color: #0f172a; }
.tbl tr:last-child td { border-bottom: none; }
.tbl tr:hover td { background: #fafbfc; }
.tag { padding: 3px 10px; border-radius: 20px; font-size: 0.65rem; font-weight: 600; }
.tag-g { background: #f0fdf4; color: #15803d; }
.tag-b { background: #eff6ff; color: #1d4ed8; }
.tag-p { background: #faf5ff; color: #7e22ce; }

.chat-wrap {
    background: white; border-radius: 20px;
    border: 1.5px solid #f1f5f9;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    overflow: hidden;
}
.chat-head {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
    padding: 20px 28px;
    display: flex; align-items: center; gap: 16px;
}
.chat-head-avatar {
    width: 48px; height: 48px;
    background: rgba(255,255,255,0.15);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    backdrop-filter: blur(10px);
}
.chat-head-name { font-size: 1rem; font-weight: 700; color: white; }
.chat-head-status {
    font-size: 0.72rem; color: rgba(255,255,255,0.75);
    margin-top: 3px; display: flex; align-items: center; gap: 5px;
}
.chat-head-dot { width: 6px; height: 6px; background: #4ade80; border-radius: 50%; display: inline-block; }

.chat-body {
    padding: 28px 28px 20px 28px;
    min-height: 300px;
    background: #f8fafc;
    display: flex; flex-direction: column; gap: 20px;
}
.msg-u { display: flex; justify-content: flex-end; }
.msg-a { display: flex; align-items: flex-start; gap: 12px; }
.msg-avatar {
    width: 34px; height: 34px; border-radius: 10px;
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 13px; font-weight: 700;
    flex-shrink: 0; margin-top: 2px;
}
.bub-u {
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    color: white; padding: 14px 20px;
    border-radius: 22px 22px 6px 22px;
    font-size: 0.87rem; line-height: 1.6; max-width: 65%;
    box-shadow: 0 4px 18px rgba(79,70,229,0.28);
    letter-spacing: -0.1px;
}
.bub-a {
    background: white; border: 1.5px solid #e8ecf2;
    color: #1e293b; padding: 14px 20px;
    border-radius: 6px 22px 22px 22px;
    font-size: 0.87rem; line-height: 1.75; max-width: 72%;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    letter-spacing: -0.1px;
}

.chips-row {
    padding: 14px 28px; background: white;
    border-top: 1px solid #f1f5f9;
    display: flex; flex-wrap: wrap; gap: 8px;
}
.chip-btn {
    background: #f8fafc; border: 1.5px solid #e2e8f0;
    border-radius: 20px; padding: 7px 16px;
    font-size: 0.75rem; color: #475569; font-weight: 500;
    cursor: pointer; white-space: nowrap;
    transition: all 0.15s;
}

.footer-bar {
    background: #0f172a; border-radius: 16px;
    padding: 20px 32px; margin-top: 40px;
    display: flex; align-items: center; justify-content: space-between;
}
.footer-left { font-size: 0.75rem; color: #475569; line-height: 1.8; }
.footer-left strong { color: #94a3b8; }
.footer-links { display: flex; gap: 8px; }
.footer-link {
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px; padding: 6px 14px;
    font-size: 0.72rem; color: #94a3b8; text-decoration: none;
    font-weight: 500;
}

[data-testid="stSidebar"] { display: none; }
.stTabs [data-baseweb="tab-list"] {
    background: #f8fafc !important;
    border-radius: 14px !important;
    padding: 5px !important;
    gap: 3px !important;
    border: 1.5px solid #f1f5f9 !important;
    margin-bottom: 8px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    color: #64748b !important;
    padding: 9px 22px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    txn = pd.read_csv('transaction_data.csv')
    camp = pd.read_csv('campaign_data.csv')
    cust = pd.read_csv('customer_data.csv')
    txn['date'] = pd.to_datetime(txn['date'])
    camp['date'] = pd.to_datetime(camp['date'])
    return txn, camp, cust

txn_df, camp_df, cust_df = load_data()

def get_key():
    try: return st.secrets["GROQ_API_KEY"]
    except: return os.getenv("GROQ_API_KEY")

def analyze(q):
    try:
        ch = txn_df.groupby('channel')['net_revenue'].sum().round(0).to_dict()
        top5 = txn_df.groupby('merchant')['transaction_amount'].sum().sort_values(ascending=False).head(5).round(0).to_dict()
        churn = cust_df.groupby('segment')['churn_risk'].mean().round(3).to_dict()
        roas = camp_df.groupby('campaign')['roas'].mean().round(1).to_dict()
        ctx = f"""You are NexPay AI, a razor-sharp payments intelligence agent built for C-suite executives.

STRICT RULES — never break these:
1. Answer in EXACTLY 2-3 short sentences. Never more.
2. Lead with the direct answer and the most important number immediately.
3. No greetings, no preamble, no "based on the data", no "I'd like to present".
4. End every response with one bold action: "ACTION: [what to do now]"
5. Use $ and % formatting. Be blunt. Sound like a McKinsey partner, not a chatbot.

LIVE DATA SNAPSHOT:
- Total Volume: ${txn_df['transaction_amount'].sum():,.0f} | Net Revenue: ${txn_df['net_revenue'].sum():,.0f}
- Approval Rate: {txn_df['is_approved'].mean():.1%} | Customers: {len(cust_df):,}
- Channel Revenue: {ch}
- Top Merchants: {top5}
- Churn by Segment: {churn}
- ROAS by Campaign: {roas}"""
        client = Groq(api_key=get_key())
        r = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"system","content":ctx},{"role":"user","content":q}],
            max_tokens=120, temperature=0.1
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)[:80]}"

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role":"assistant","content":"Hello. I am NexPay AI, your payments intelligence assistant. I have analyzed 100,000 transactions across all channels and customer segments. What would you like to know?"}
    ]
if 'chip_clicked' not in st.session_state:
    st.session_state.chip_clicked = None

now = datetime.now()

st.markdown(f"""
<div class="top-nav">
    <div class="nav-brand">
        <div class="nav-logo-wrap">
            <div class="nav-logo">
                <svg viewBox="0 0 24 24" fill="none">
                    <rect x="3" y="3" width="8" height="8" rx="2" fill="white" opacity="0.9"/>
                    <rect x="13" y="3" width="8" height="8" rx="2" fill="white" opacity="0.6"/>
                    <rect x="3" y="13" width="8" height="8" rx="2" fill="white" opacity="0.6"/>
                    <rect x="13" y="13" width="8" height="8" rx="2" fill="white" opacity="0.9"/>
                </svg>
            </div>
            <div>
                <div class="nav-name">NexPay Analytics</div>
                <div class="nav-tagline">Next-Generation Payments Intelligence</div>
            </div>
        </div>
    </div>
    <div class="nav-right">
        <div class="nav-live"><span class="live-dot"></span>Live Data</div>
        <div class="nav-date">{now.strftime('%b %d, %Y  %H:%M')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-label">
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <circle cx="6" cy="6" r="5" fill="#2563eb" opacity="0.2"/>
            <circle cx="6" cy="6" r="3" fill="#2563eb"/>
        </svg>
        Payments Intelligence Platform
    </div>
    <div class="hero-title">Turn payment data into<br><span>strategic decisions</span></div>
    <div class="hero-desc">Real-time analytics across 100,000 transactions, 50,000 customers, and 6 campaign types. Ask the AI agent anything in plain English.</div>
    <div class="hero-pills">
        <span class="hero-pill">100,000 Transactions</span>
        <span class="hero-pill">50,000 Customers</span>
        <span class="hero-pill">6 Campaign Types</span>
        <span class="hero-pill">AI-Powered Insights</span>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Dashboard",
    "AI Analytics Agent",
    "Transaction Explorer",
    "Campaign Intelligence"
])

with tab1:
    tv = txn_df['transaction_amount'].sum()
    nr = txn_df['net_revenue'].sum()
    ar = txn_df['is_approved'].mean()
    at = txn_df['transaction_amount'].mean()

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon-box blue">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2">
                    <rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/>
                </svg>
            </div>
            <div class="kpi-label">Total Payment Volume</div>
            <div class="kpi-value">${tv/1e6:.1f}M</div>
            <div class="kpi-meta">100,000 transactions processed</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card g">
            <div class="kpi-icon-box green">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2">
                    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>
                </svg>
            </div>
            <div class="kpi-label">Net Revenue</div>
            <div class="kpi-value">${nr/1e6:.2f}M</div>
            <div class="kpi-meta">After cashback deductions</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card p">
            <div class="kpi-icon-box purple">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                    <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
            </div>
            <div class="kpi-label">Approval Rate</div>
            <div class="kpi-value">{ar:.1%}</div>
            <div class="kpi-meta">{txn_df['is_approved'].sum():,} transactions approved</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card o">
            <div class="kpi-icon-box orange">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2">
                    <line x1="12" y1="1" x2="12" y2="23"/>
                    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                </svg>
            </div>
            <div class="kpi-label">Avg Transaction</div>
            <div class="kpi-value">${at:,.0f}</div>
            <div class="kpi-meta">Across all payment channels</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1,1], gap="large")

    with col1:
        st.markdown("""<div class="card"><div class="card-head">
            <div><div class="card-head-title">Volume by Payment Channel</div>
            <div class="card-head-sub">Transaction amount breakdown</div></div>
            <span class="card-tag">100K records</span>
        </div></div>""", unsafe_allow_html=True)
        ch = txn_df.groupby('channel')['transaction_amount'].sum().reset_index().sort_values('transaction_amount', ascending=True)
        ch['pct'] = (ch['transaction_amount'] / ch['transaction_amount'].sum() * 100).round(1)
        colors = ['#4f46e5','#6366f1','#818cf8','#a5b4fc','#c7d2fe']
        fig1 = go.Figure()
        for i, row in ch.iterrows():
            fig1.add_trace(go.Bar(
                x=[row['channel']], y=[row['transaction_amount']],
                marker_color=colors[i % len(colors)],
                marker_line_width=0,
                name=row['channel'],
                text=f"${row['transaction_amount']/1e6:.2f}M ({row['pct']}%)",
                textposition='outside',
                textfont=dict(size=10, color='#334155', family='Inter'),
            ))
        fig1.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=40,b=10), height=300,
            showlegend=False,
            font=dict(size=11, color='#0f172a', family='Inter'),
            bargap=0.35,
            xaxis=dict(
                showgrid=False, zeroline=False,
                tickfont=dict(color='#334155', size=11, family='Inter'),
                title=None,
                showline=True, linecolor='#e2e8f0'
            ),
            yaxis=dict(
                showgrid=True, gridcolor='#f1f5f9', gridwidth=1,
                tickfont=dict(color='#94a3b8', size=10),
                title=dict(text='Transaction Volume (USD)', font=dict(color='#64748b', size=10)),
                tickformat='$,.0f', zeroline=False,
                showline=False
            ),
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("""<div class="card"><div class="card-head">
            <div><div class="card-head-title">Monthly Revenue Trend</div>
            <div class="card-head-sub">Transaction volume over time</div></div>
        </div></div>""", unsafe_allow_html=True)
        monthly = txn_df.copy()
        monthly['month'] = monthly['date'].dt.to_period('M').astype(str)
        md = monthly.groupby('month')['transaction_amount'].sum().reset_index()
        avg_vol = md['transaction_amount'][:-1].mean()
        if len(md) > 2 and md['transaction_amount'].iloc[-1] < avg_vol * 0.8:
            md = md.iloc[:-1]
        max_idx = md['transaction_amount'].idxmax()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=md['month'], y=md['transaction_amount'],
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(99,102,241,0.08)',
            line=dict(width=2.5, color='#4f46e5', shape='spline'),
            marker=dict(size=5, color='#4f46e5', line=dict(width=2, color='white')),
            hovertemplate='<b>%{x}</b><br>Volume: $%{y:,.0f}<extra></extra>',
        ))
        fig2.add_annotation(
            x=md.loc[max_idx,'month'], y=md.loc[max_idx,'transaction_amount'],
            text=f"Peak: \${md.loc[max_idx,'transaction_amount']/1e6:.2f}M",
            showarrow=True, arrowhead=2, arrowcolor='#4f46e5',
            font=dict(size=9, color='#4f46e5', family='Inter'),
            bgcolor='#eff6ff', bordercolor='#c7d2fe', borderwidth=1, borderpad=4, ay=-36
        )
        fig2.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=30,b=10), height=260,
            font=dict(size=10, color='#0f172a', family='Inter'),
            xaxis=dict(
                showgrid=False, zeroline=False,
                tickfont=dict(color='#64748b', size=9),
                tickangle=30, title=None,
                showline=True, linecolor='#e2e8f0', nticks=8
            ),
            yaxis=dict(
                showgrid=True, gridcolor='#f1f5f9', gridwidth=1,
                tickfont=dict(color='#94a3b8', size=9),
                title=dict(text='Volume (USD)', font=dict(color='#64748b', size=9)),
                tickformat='\$,.0f', zeroline=False
            ),
            hovermode='x unified', showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown("""<div class="card"><div class="card-head">
            <div><div class="card-head-title">Customer Segment Risk Matrix</div>
            <div class="card-head-sub">Average spend vs churn risk</div></div>
        </div></div>""", unsafe_allow_html=True)
        seg = cust_df.groupby('segment').agg(count=('customer_id','count'), avg_spend=('total_spend','mean'), churn=('churn_risk','mean')).reset_index()
        # Color by churn risk rank: light blue=lowest, darkest navy=highest
        seg_sorted = seg.sort_values('churn')
        risk_colors = ['#bfdbfe','#60a5fa','#2563eb','#1d4ed8','#1e3a8a']
        palette = {row['segment']: risk_colors[i] for i, (_, row) in enumerate(seg_sorted.iterrows())}
        fig3 = go.Figure()
        mid_spend = seg['avg_spend'].mean()
        mid_churn = seg['churn'].mean()
        fig3.add_shape(type='rect', x0=seg['avg_spend'].min()*0.85, x1=mid_spend,
            y0=mid_churn, y1=seg['churn'].max()*1.005,
            fillcolor='rgba(239,68,68,0.05)', line_width=0)
        fig3.add_shape(type='rect', x0=mid_spend, x1=seg['avg_spend'].max()*1.15,
            y0=mid_churn, y1=seg['churn'].max()*1.005,
            fillcolor='rgba(249,115,22,0.05)', line_width=0)
        fig3.add_shape(type='rect', x0=seg['avg_spend'].min()*0.85, x1=mid_spend,
            y0=seg['churn'].min()*0.995, y1=mid_churn,
            fillcolor='rgba(99,102,241,0.05)', line_width=0)
        fig3.add_shape(type='rect', x0=mid_spend, x1=seg['avg_spend'].max()*1.15,
            y0=seg['churn'].min()*0.995, y1=mid_churn,
            fillcolor='rgba(34,197,94,0.05)', line_width=0)
        fig3.add_annotation(x=seg['avg_spend'].min()*1.1, y=seg['churn'].max()*1.004,
            text='High Risk / Low Spend', font=dict(size=8, color='#ef4444'), showarrow=False, xanchor='left')
        fig3.add_annotation(x=seg['avg_spend'].max()*1.1, y=seg['churn'].max()*1.004,
            text='High Risk / High Spend', font=dict(size=8, color='#f97316'), showarrow=False, xanchor='right')
        fig3.add_annotation(x=seg['avg_spend'].min()*1.1, y=seg['churn'].min()*0.996,
            text='Low Risk / Low Spend', font=dict(size=8, color='#6366f1'), showarrow=False, xanchor='left')
        fig3.add_annotation(x=seg['avg_spend'].max()*1.1, y=seg['churn'].min()*0.996,
            text='Low Risk / High Spend', font=dict(size=8, color='#16a34a'), showarrow=False, xanchor='right')
        for _, row in seg.iterrows():
            col = palette.get(row['segment'], '#6366f1')
            fig3.add_trace(go.Scatter(
                x=[row['avg_spend']], y=[row['churn']],
                mode='markers+text',
                marker=dict(size=28, color=col,
                            line=dict(width=2.5, color='white'), opacity=0.92),
                text=[f"<b>{row['segment']}</b>"],
                textposition='top center',
                textfont=dict(size=10, color='#0f172a', family='Inter'),
                hovertemplate=f"<b>{row['segment']}</b><br>Avg Spend: \${row['avg_spend']:,.0f}<br>Churn Risk: {row['churn']:.4f}<br>Customers: {row['count']:,}<extra></extra>",
                name=row['segment']
            ))
        fig3.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=30,b=10), height=280,
            showlegend=False,
            font=dict(size=10, color='#0f172a', family='Inter'),
            xaxis=dict(
                showgrid=True, gridcolor='#f1f5f9', zeroline=False,
                tickfont=dict(color='#64748b', size=10),
                title=dict(text='Average Customer Spend (USD)', font=dict(color='#64748b', size=10)),
                tickformat='\$,.0f', showline=True, linecolor='#e2e8f0'
            ),
            yaxis=dict(
                showgrid=True, gridcolor='#f1f5f9', zeroline=False,
                tickfont=dict(color='#64748b', size=10),
                title=dict(text='Churn Risk Score', font=dict(color='#64748b', size=10)),
                tickformat='.3f', showline=True, linecolor='#e2e8f0'
            ),
            hovermode='closest'
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("""<div class="card"><div class="card-head">
            <div><div class="card-head-title">Top Merchants by Volume</div>
            <div class="card-head-sub">Ranked by transaction amount</div></div>
        </div></div>""", unsafe_allow_html=True)
        top_m = txn_df.groupby('merchant').agg(
            volume=('transaction_amount','sum'),
            count=('transaction_id','count'),
            approval=('is_approved','mean')
        ).sort_values('volume', ascending=False).head(8).reset_index()
        tbl = '<table class="tbl"><tr><th>Merchant</th><th>Volume</th><th>Transactions</th><th>Approval</th></tr>'
        for _,r in top_m.iterrows():
            tc = 'tag-g' if r['approval']>0.7 else 'tag-b'
            tbl += f'<tr><td><strong>{r["merchant"]}</strong></td><td>${r["volume"]/1000:.0f}K</td><td>{r["count"]:,}</td><td><span class="tag {tc}">{r["approval"]:.0%}</span></td></tr>'
        tbl += '</table>'
        st.markdown(tbl, unsafe_allow_html=True)

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    _, center, _ = st.columns([1,5,1])
    with center:
        st.markdown("""
        <div style="text-align:center;margin-bottom:28px">
            <div style="font-size:0.72rem;font-weight:600;color:#6366f1;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px">AI Analytics Agent</div>
            <div style="font-size:1.7rem;font-weight:900;color:#0f172a;letter-spacing:-0.5px;line-height:1.2">Ask anything about your payments</div>
            <div style="font-size:0.88rem;color:#94a3b8;margin-top:10px">Powered by Groq LLaMA3, analyzing 100,000 transactions in real time</div>
        </div>
        """, unsafe_allow_html=True)

        msgs_html = ""
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                msgs_html += f'<div class="msg-u"><div class="bub-u">{msg["content"]}</div></div>'
            else:
                msgs_html += f'<div class="msg-a"><div class="msg-avatar">N</div><div class="bub-a">{msg["content"]}</div></div>'

        st.markdown(f"""
        <div class="chat-wrap">
            <div class="chat-head">
                <div class="chat-head-avatar">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
                        <rect x="3" y="3" width="7" height="7" rx="1.5" fill="white" opacity="0.8"/>
                        <rect x="14" y="3" width="7" height="7" rx="1.5" fill="white" opacity="0.5"/>
                        <rect x="3" y="14" width="7" height="7" rx="1.5" fill="white" opacity="0.5"/>
                        <rect x="14" y="14" width="7" height="7" rx="1.5" fill="white" opacity="0.8"/>
                    </svg>
                </div>
                <div>
                    <div class="chat-head-name">NexPay AI Agent</div>
                    <div class="chat-head-status">
                        <span class="chat-head-dot"></span>
                        Online, analyzing 100K transactions
                    </div>
                </div>
            </div>
            <div class="chat-body">
                {msgs_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

        chips = ["Which channel has the best ROAS?", "Who is at highest churn risk?", "What is our top campaign?", "Where should we increase budget?", "What is our approval rate by region?"]
        st.markdown('<div class="chips-row">', unsafe_allow_html=True)
        chip_cols = st.columns(len(chips))
        for i, (col, chip) in enumerate(zip(chip_cols, chips)):
            with col:
                if st.button(chip, key=f"chip_{i}", use_container_width=True):
                    st.session_state.messages.append({"role":"user","content":chip})
                    with st.spinner("Analyzing..."):
                        resp = analyze(chip)
                    st.session_state.messages.append({"role":"assistant","content":resp})
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            ci, cb = st.columns([6,1])
            with ci:
                user_input = st.text_input("q", placeholder="Ask about transactions, campaigns, customers...", label_visibility="collapsed")
            with cb:
                submit = st.form_submit_button("Send", use_container_width=True)

        if submit and user_input:
            st.session_state.messages.append({"role":"user","content":user_input})
            with st.spinner("Analyzing..."):
                resp = analyze(user_input)
            st.session_state.messages.append({"role":"assistant","content":resp})
            st.rerun()

with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    with f1:
        sel_ch = st.selectbox("Channel", ['All'] + list(txn_df['channel'].unique()))
    with f2:
        sel_me = st.selectbox("Merchant", ['All'] + list(txn_df['merchant'].unique()))
    with f3:
        sel_st = st.selectbox("Status", ['All','Approved','Declined','Pending'])

    filt = txn_df.copy()
    if sel_ch != 'All': filt = filt[filt['channel']==sel_ch]
    if sel_me != 'All': filt = filt[filt['merchant']==sel_me]
    if sel_st != 'All': filt = filt[filt['status']==sel_st]

    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Transactions", f"{len(filt):,}")
    m2.metric("Total Volume", f"${filt['transaction_amount'].sum():,.0f}")
    m3.metric("Avg Amount", f"${filt['transaction_amount'].mean():,.2f}")
    m4.metric("Approval Rate", f"{filt['is_approved'].mean():.1%}")
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(filt[['transaction_id','date','merchant','channel','customer_segment','transaction_amount','status','cashback_earned','net_revenue']].head(200), use_container_width=True, height=420)

with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    cs = camp_df.groupby('campaign').agg(
        total_sent=('sent','sum'), total_rev=('revenue','sum'),
        total_cost=('cost','sum'), avg_conv=('conversion_rate','mean'),
        avg_roas=('roas','mean')
    ).reset_index().sort_values('avg_roas', ascending=False)

    cc1, cc2 = st.columns(2, gap="large")
    with cc1:
        st.markdown("""<div class="card"><div class="card-head">
            <div><div class="card-head-title">Campaign ROAS Ranking</div>
            <div class="card-head-sub">Return on ad spend by campaign</div></div>
        </div></div>""", unsafe_allow_html=True)
        fig4 = px.bar(cs, x='avg_roas', y='campaign', orientation='h',
                      color='avg_roas', color_continuous_scale=[[0,'#e0e7ff'],[1,'#4f46e5']])
        fig4.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=0,r=0,t=8,b=0), height=300,
            showlegend=False, coloraxis_showscale=False,
            font=dict(size=10, color='#0f172a'),
            xaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='ROAS',font=dict(color='#94a3b8'))),
            yaxis=dict(tickfont=dict(color='#0f172a',size=10), title=None)
        )
        fig4.update_traces(marker_line_width=0)
        st.plotly_chart(fig4, use_container_width=True)

    with cc2:
        st.markdown("""<div class="card"><div class="card-head">
            <div><div class="card-head-title">Conversion vs Revenue</div>
            <div class="card-head-sub">Bubble size indicates total reach</div></div>
        </div></div>""", unsafe_allow_html=True)
        fig5 = px.scatter(cs, x='avg_conv', y='total_rev', size='total_sent',
                          color='campaign', text='campaign',
                          color_discrete_sequence=['#6366f1','#22c55e','#f59e0b','#ef4444','#0ea5e9','#8b5cf6'])
        fig5.update_traces(textposition='top center', textfont=dict(size=8, color='#0f172a'))
        fig5.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=0,r=0,t=8,b=0), height=300,
            showlegend=False,
            font=dict(size=10, color='#0f172a'),
            xaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='Avg Conversion Rate (%)',font=dict(color='#94a3b8',size=10))),
            yaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='Total Revenue ($)',font=dict(color='#94a3b8',size=10)))
        )
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cd = cs.copy()
    cd['total_rev'] = cd['total_rev'].apply(lambda x: f"${x/1e6:.1f}M")
    cd['avg_conv'] = cd['avg_conv'].apply(lambda x: f"{x:.1f}%")
    cd['avg_roas'] = cd['avg_roas'].apply(lambda x: f"{x:.0f}x")
    cd['total_sent'] = cd['total_sent'].apply(lambda x: f"{x:,}")
    cd.columns = ['Campaign','Total Sent','Revenue','Cost','Avg Conversion','ROAS']
    st.dataframe(cd[['Campaign','Total Sent','Revenue','Avg Conversion','ROAS']], use_container_width=True)

st.markdown("""
<div class="footer-bar">
    <div class="footer-left">
        <strong>NexPay Analytics</strong> by <strong>Priyanka Kapoor</strong><br>
        MS Business Analytics, Montclair State University 2026 &nbsp;|&nbsp; Powered by Groq LLaMA3 &nbsp;|&nbsp; 100,000 transactions analyzed
    </div>
    <div class="footer-links">
        <a href="https://github.com/PriyankaKapoor4202" class="footer-link">GitHub</a>
        <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6669899" class="footer-link">Research</a>
        <a href="https://breast-cancer-detection-ai-wnn9lf9wtmywjaeuhckuv9.streamlit.app" class="footer-link">MedScan AI</a>
    </div>
</div>
""", unsafe_allow_html=True)
