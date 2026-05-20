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
    padding: 0 40px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: -1rem -1rem 0 -1rem;
}
.nav-brand { display: flex; align-items: center; gap: 12px; }
.nav-logo {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 16px; font-weight: 900;
    box-shadow: 0 4px 12px rgba(99,102,241,0.3);
}
.nav-title { font-size: 1.05rem; font-weight: 800; color: #0f172a; letter-spacing: -0.3px; }
.nav-sub { font-size: 0.68rem; color: #94a3b8; font-weight: 400; }
.nav-tabs { display: flex; align-items: center; gap: 4px; }
.nav-tab {
    padding: 8px 16px; border-radius: 8px;
    font-size: 0.82rem; font-weight: 500; color: #64748b;
    cursor: pointer; border: none; background: transparent;
}
.nav-tab-active {
    background: #f1f5f9; color: #0f172a; font-weight: 600;
}
.nav-right { display: flex; align-items: center; gap: 12px; }
.nav-badge {
    background: #f0fdf4; border: 1px solid #bbf7d0;
    border-radius: 20px; padding: 5px 12px;
    font-size: 0.72rem; color: #166534; font-weight: 600;
    display: flex; align-items: center; gap: 5px;
}
.nav-dot { width: 6px; height: 6px; background: #22c55e; border-radius: 50%; display: inline-block; }

.hero-section {
    padding: 40px 0 32px 0;
    border-bottom: 1px solid #f1f5f9;
    margin-bottom: 32px;
}
.hero-eyebrow {
    font-size: 0.72rem; font-weight: 600; color: #6366f1;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;
}
.hero-title {
    font-size: 2.2rem; font-weight: 900; color: #0f172a;
    letter-spacing: -0.8px; line-height: 1.1; margin-bottom: 12px;
}
.hero-title span { color: #6366f1; }
.hero-sub { font-size: 0.92rem; color: #64748b; line-height: 1.6; max-width: 600px; }
.hero-stats { display: flex; gap: 32px; margin-top: 24px; }
.hero-stat-value { font-size: 1.4rem; font-weight: 800; color: #0f172a; }
.hero-stat-label { font-size: 0.72rem; color: #94a3b8; font-weight: 500; margin-top: 2px; }

.kpi-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 28px; }
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 22px 24px;
    border: 1.5px solid #f1f5f9;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.03);
    transition: box-shadow 0.2s;
}
.kpi-card:hover { box-shadow: 0 4px 24px rgba(99,102,241,0.12); border-color: #e0e7ff; }
.kpi-icon {
    width: 40px; height: 40px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; margin-bottom: 14px;
}
.kpi-icon.blue { background: #eff6ff; }
.kpi-icon.green { background: #f0fdf4; }
.kpi-icon.purple { background: #faf5ff; }
.kpi-icon.orange { background: #fff7ed; }
.kpi-label { font-size: 0.72rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 6px; }
.kpi-value { font-size: 1.8rem; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; line-height: 1; }
.kpi-sub { font-size: 0.72rem; color: #22c55e; font-weight: 600; margin-top: 8px; display: flex; align-items: center; gap: 4px; }

.section-header { margin-bottom: 16px; }
.section-title { font-size: 1rem; font-weight: 700; color: #0f172a; }
.section-sub { font-size: 0.78rem; color: #94a3b8; margin-top: 2px; }

.chart-card {
    background: white;
    border-radius: 16px;
    border: 1.5px solid #f1f5f9;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    padding: 20px;
    margin-bottom: 20px;
}
.chart-card-header { margin-bottom: 16px; display: flex; justify-content: space-between; align-items: flex-start; }
.chart-card-title { font-size: 0.85rem; font-weight: 700; color: #0f172a; }
.chart-card-sub { font-size: 0.72rem; color: #94a3b8; margin-top: 3px; }
.chart-badge {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 8px; padding: 4px 10px;
    font-size: 0.68rem; color: #64748b; font-weight: 500;
}

.data-table { width: 100%; border-collapse: collapse; }
.data-table th {
    font-size: 0.68rem; font-weight: 600; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.5px;
    padding: 8px 12px; border-bottom: 1.5px solid #f1f5f9;
    text-align: left; background: #fafbfc;
}
.data-table td { padding: 10px 12px; border-bottom: 1px solid #f8fafc; font-size: 0.82rem; color: #0f172a; }
.data-table tr:hover td { background: #fafbfc; }
.data-table tr:last-child td { border-bottom: none; }
.pill { padding: 3px 10px; border-radius: 20px; font-size: 0.65rem; font-weight: 600; }
.pill-green { background: #f0fdf4; color: #16a34a; }
.pill-blue { background: #eff6ff; color: #2563eb; }
.pill-purple { background: #faf5ff; color: #7c3aed; }

.chat-container {
    background: #fafbfc;
    border-radius: 20px;
    border: 1.5px solid #f1f5f9;
    overflow: hidden;
    height: 580px;
    display: flex;
    flex-direction: column;
}
.chat-top-bar {
    background: white;
    border-bottom: 1.5px solid #f1f5f9;
    padding: 16px 24px;
    display: flex; align-items: center; gap: 14px;
}
.chat-ai-avatar {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 12px rgba(99,102,241,0.3);
}
.chat-ai-avatar svg { width: 24px; height: 24px; }
.chat-ai-name { font-size: 0.92rem; font-weight: 700; color: #0f172a; }
.chat-ai-status { font-size: 0.7rem; color: #22c55e; font-weight: 500; margin-top: 2px; display: flex; align-items: center; gap: 4px; }
.chat-ai-dot { width: 6px; height: 6px; background: #22c55e; border-radius: 50%; display: inline-block; }

.chat-messages-area {
    flex: 1; padding: 20px 24px;
    overflow-y: auto; display: flex; flex-direction: column; gap: 16px;
}
.msg-row-user { display: flex; justify-content: flex-end; }
.msg-row-agent { display: flex; justify-content: flex-start; align-items: flex-start; gap: 10px; }
.msg-avatar-small {
    width: 30px; height: 30px; border-radius: 10px;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 2px;
    font-size: 14px; color: white; font-weight: 700;
}
.bubble-user {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white; padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    font-size: 0.85rem; line-height: 1.5;
    max-width: 70%; box-shadow: 0 4px 12px rgba(99,102,241,0.2);
}
.bubble-agent {
    background: white; border: 1.5px solid #f1f5f9;
    color: #0f172a; padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    font-size: 0.85rem; line-height: 1.6;
    max-width: 75%; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.chat-suggestions {
    padding: 12px 24px;
    background: white;
    border-top: 1px solid #f1f5f9;
    display: flex; flex-wrap: wrap; gap: 8px;
}
.suggestion-btn {
    background: #f8fafc; border: 1.5px solid #e2e8f0;
    border-radius: 20px; padding: 6px 14px;
    font-size: 0.75rem; color: #475569; font-weight: 500;
    cursor: pointer; white-space: nowrap;
}
.suggestion-btn:hover { background: #eff6ff; border-color: #c7d2fe; color: #4f46e5; }

.chat-input-bar {
    padding: 16px 24px; background: white;
    border-top: 1.5px solid #f1f5f9;
    display: flex; gap: 10px; align-items: center;
}

.built-by-card {
    background: linear-gradient(135deg, #faf5ff, #eff6ff);
    border: 1.5px solid #e0e7ff;
    border-radius: 20px;
    padding: 28px 32px;
    margin-top: 32px;
    display: flex; align-items: center; justify-content: space-between;
}
.built-by-left { display: flex; align-items: center; gap: 16px; }
.built-by-avatar {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; font-weight: 900; color: white;
    box-shadow: 0 4px 16px rgba(99,102,241,0.3);
}
.built-by-name { font-size: 1rem; font-weight: 800; color: #0f172a; }
.built-by-title { font-size: 0.78rem; color: #6366f1; font-weight: 600; margin-top: 2px; }
.built-by-sub { font-size: 0.72rem; color: #94a3b8; margin-top: 2px; }
.built-by-links { display: flex; gap: 10px; }
.built-by-link {
    background: white; border: 1.5px solid #e0e7ff;
    border-radius: 10px; padding: 8px 16px;
    font-size: 0.75rem; font-weight: 600; color: #4f46e5;
    text-decoration: none;
}

[data-testid="stSidebar"] { display: none; }
.stTabs [data-baseweb="tab-list"] {
    background: #f8fafc !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1.5px solid #f1f5f9 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #64748b !important;
    padding: 8px 18px !important;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
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
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        return os.getenv("GROQ_API_KEY")

def analyze(question):
    try:
        ch = txn_df.groupby('channel')['net_revenue'].sum().round(0).to_dict()
        top5 = txn_df.groupby('merchant')['transaction_amount'].sum().sort_values(ascending=False).head(5).round(0).to_dict()
        churn = cust_df.groupby('segment')['churn_risk'].mean().round(3).to_dict()
        roas = camp_df.groupby('campaign')['roas'].mean().round(1).to_dict()
        context = f"""You are NexPay AI, an elite payments analytics assistant.
Answer like a senior analyst to a CEO. Specific numbers. Max 3-4 sentences. End with one recommendation.
Total Volume: ${txn_df['transaction_amount'].sum():,.0f} | Approval: {txn_df['is_approved'].mean():.1%}
Revenue: ${txn_df['net_revenue'].sum():,.0f} | Customers: {len(cust_df):,}
Channels: {ch} | Top Merchants: {top5} | Churn: {churn} | ROAS: {roas}"""
        client = Groq(api_key=get_key())
        r = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"system","content":context},{"role":"user","content":question}],
            max_tokens=180, temperature=0.2
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)[:100]}"

if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role":"assistant","content":"Hi! I'm NexPay AI. I have full access to your payments data — 100,000 transactions, 50,000 customers, and 6 campaign types. What would you like to know?"}
    ]

now = datetime.now()

st.markdown(f"""
<div class="top-nav">
    <div class="nav-brand">
        <div class="nav-logo">N</div>
        <div>
            <div class="nav-title">NexPay Analytics</div>
            <div class="nav-sub">Next-Generation Payments Intelligence</div>
        </div>
    </div>
    <div class="nav-right">
        <div class="nav-badge"><span class="nav-dot"></span> Live — {len(txn_df):,} transactions</div>
        <div style="font-size:0.72rem;color:#94a3b8">{now.strftime('%b %d, %Y')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-section">
    <div class="hero-eyebrow">Payments Intelligence Platform</div>
    <div class="hero-title">Turn payment data into<br><span>strategic decisions</span></div>
    <div class="hero-sub">Real-time analytics across transactions, campaigns, and customer segments — powered by AI that speaks business, not SQL.</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Dashboard",
    "AI Analytics Agent",
    "Transaction Explorer",
    "Campaign Intelligence"
])

with tab1:
    total_volume = txn_df['transaction_amount'].sum()
    total_revenue = txn_df['net_revenue'].sum()
    approval_rate = txn_df['is_approved'].mean()
    avg_txn = txn_df['transaction_amount'].mean()

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon blue">💳</div>
            <div class="kpi-label">Total Volume</div>
            <div class="kpi-value">${total_volume/1e6:.1f}M</div>
            <div class="kpi-sub">100,000 transactions</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon green">📈</div>
            <div class="kpi-label">Net Revenue</div>
            <div class="kpi-value">${total_revenue/1e6:.2f}M</div>
            <div class="kpi-sub">After cashback costs</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon purple">✅</div>
            <div class="kpi-label">Approval Rate</div>
            <div class="kpi-value">{approval_rate:.1%}</div>
            <div class="kpi-sub">{txn_df['is_approved'].sum():,} approved</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon orange">💰</div>
            <div class="kpi-label">Avg Transaction</div>
            <div class="kpi-value">${avg_txn:,.0f}</div>
            <div class="kpi-sub">All channels</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1,1], gap="large")

    with col1:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-card-header">
                <div>
                    <div class="chart-card-title">Volume by Channel</div>
                    <div class="chart-card-sub">Transaction amount breakdown</div>
                </div>
                <span class="chart-badge">100K records</span>
            </div>
        </div>""", unsafe_allow_html=True)
        ch = txn_df.groupby('channel')['transaction_amount'].sum().reset_index().sort_values('transaction_amount', ascending=False)
        fig1 = px.bar(ch, x='channel', y='transaction_amount',
                      color_discrete_sequence=['#6366f1','#818cf8','#a5b4fc','#c7d2fe','#e0e7ff'])
        fig1.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=0,r=0,t=0,b=0), height=250,
            showlegend=False,
            font=dict(size=11, color='#0f172a'),
            xaxis=dict(showgrid=False, tickfont=dict(color='#475569',size=11), title=None),
            yaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='Volume ($)',font=dict(color='#94a3b8',size=10)))
        )
        fig1.update_traces(marker_line_width=0, marker_cornerradius=4)
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("""
        <div class="chart-card">
            <div class="chart-card-header">
                <div>
                    <div class="chart-card-title">Monthly Revenue Trend</div>
                    <div class="chart-card-sub">Transaction volume over time</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        monthly = txn_df.copy()
        monthly['month'] = monthly['date'].dt.to_period('M').astype(str)
        md = monthly.groupby('month')['transaction_amount'].sum().reset_index()
        fig2 = px.area(md, x='month', y='transaction_amount', color_discrete_sequence=['#6366f1'])
        fig2.update_traces(fill='tozeroy', fillcolor='rgba(99,102,241,0.08)', line=dict(width=2.5, color='#6366f1'))
        fig2.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=0,r=0,t=0,b=0), height=230,
            font=dict(size=10, color='#0f172a'),
            xaxis=dict(showgrid=False, tickfont=dict(color='#94a3b8',size=9), tickangle=45, title=None),
            yaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=9), title=None)
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown("""
        <div class="chart-card">
            <div class="chart-card-header">
                <div>
                    <div class="chart-card-title">Customer Segment Risk Matrix</div>
                    <div class="chart-card-sub">Spend vs churn risk by segment</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        seg = cust_df.groupby('segment').agg(count=('customer_id','count'), avg_spend=('total_spend','mean'), churn=('churn_risk','mean')).reset_index()
        fig3 = px.scatter(seg, x='avg_spend', y='churn', size='count', color='segment', text='segment',
                          color_discrete_sequence=['#6366f1','#22c55e','#f59e0b','#ef4444','#0ea5e9'])
        fig3.update_traces(textposition='top center', textfont=dict(size=10, color='#0f172a'))
        fig3.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=0,r=0,t=0,b=0), height=250,
            showlegend=False,
            font=dict(size=10, color='#0f172a'),
            xaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='Avg Spend ($)',font=dict(color='#94a3b8',size=10))),
            yaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='Churn Risk',font=dict(color='#94a3b8',size=10)))
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("""
        <div class="chart-card">
            <div class="chart-card-header">
                <div>
                    <div class="chart-card-title">Top Merchants</div>
                    <div class="chart-card-sub">By transaction volume</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        top_m = txn_df.groupby('merchant').agg(volume=('transaction_amount','sum'), count=('transaction_id','count'), approval=('is_approved','mean')).sort_values('volume',ascending=False).head(8).reset_index()
        tbl = '<table class="data-table"><tr><th>Merchant</th><th>Volume</th><th>Txns</th><th>Approval</th></tr>'
        for _,r in top_m.iterrows():
            pc = 'pill-green' if r['approval']>0.7 else 'pill-blue'
            tbl += f'<tr><td><strong>{r["merchant"]}</strong></td><td>${r["volume"]/1000:.0f}K</td><td>{r["count"]:,}</td><td><span class="pill {pc}">{r["approval"]:.0%}</span></td></tr>'
        tbl += '</table>'
        st.markdown(tbl, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div style="max-width:760px;margin:24px auto 0 auto">
        <div style="text-align:center;margin-bottom:28px">
            <div style="font-size:0.72rem;font-weight:600;color:#6366f1;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">AI Analytics Agent</div>
            <div style="font-size:1.6rem;font-weight:800;color:#0f172a;letter-spacing:-0.4px">Ask anything about your payments</div>
            <div style="font-size:0.85rem;color:#94a3b8;margin-top:8px">Powered by Groq LLaMA3 — analyzing 100,000 transactions in real time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    chat_col = st.columns([1,6,1])[1]
    with chat_col:
        st.markdown("""
        <div class="chat-container">
            <div class="chat-top-bar">
                <div class="chat-ai-avatar">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="12" cy="9" r="3" fill="white" opacity="0.9"/>
                        <path d="M5 19c0-3.866 3.134-7 7-7s7 3.134 7 7" stroke="white" stroke-width="1.8" stroke-linecap="round" opacity="0.9"/>
                        <circle cx="7" cy="7" r="1" fill="white" opacity="0.5"/>
                        <circle cx="17" cy="7" r="1" fill="white" opacity="0.5"/>
                        <circle cx="5" cy="12" r="0.8" fill="white" opacity="0.4"/>
                        <circle cx="19" cy="12" r="0.8" fill="white" opacity="0.4"/>
                        <path d="M3 9h1M20 9h1M12 3v1" stroke="white" stroke-width="1.2" stroke-linecap="round" opacity="0.5"/>
                    </svg>
                </div>
                <div>
                    <div class="chat-ai-name">NexPay AI Agent</div>
                    <div class="chat-ai-status"><span class="chat-ai-dot"></span>Online — 100K transactions analyzed</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                st.markdown(f"""
                <div class="msg-row-user">
                    <div class="bubble-user">{msg['content']}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-row-agent">
                    <div class="msg-avatar-small">N</div>
                    <div class="bubble-agent">{msg['content']}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="chat-suggestions">
            <span class="suggestion-btn">Which channel has the best ROAS?</span>
            <span class="suggestion-btn">Who is at highest churn risk?</span>
            <span class="suggestion-btn">What is our top campaign?</span>
            <span class="suggestion-btn">Where should we increase budget?</span>
            <span class="suggestion-btn">Approval rate by region?</span>
        </div>
        """, unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            col_i, col_b = st.columns([6,1])
            with col_i:
                user_input = st.text_input("q", placeholder="Ask about transactions, campaigns, customers...", label_visibility="collapsed")
            with col_b:
                submit = st.form_submit_button("Send", use_container_width=True)

        if submit and user_input:
            st.session_state.messages.append({"role":"user","content":user_input})
            with st.spinner("Analyzing..."):
                response = analyze(user_input)
            st.session_state.messages.append({"role":"assistant","content":response})
            st.rerun()

with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        channels = ['All'] + list(txn_df['channel'].unique())
        sel_channel = st.selectbox("Channel", channels)
    with col_f2:
        merchants = ['All'] + list(txn_df['merchant'].unique())
        sel_merchant = st.selectbox("Merchant", merchants)
    with col_f3:
        statuses = ['All', 'Approved', 'Declined', 'Pending']
        sel_status = st.selectbox("Status", statuses)

    filtered = txn_df.copy()
    if sel_channel != 'All': filtered = filtered[filtered['channel']==sel_channel]
    if sel_merchant != 'All': filtered = filtered[filtered['merchant']==sel_merchant]
    if sel_status != 'All': filtered = filtered[filtered['status']==sel_status]

    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Transactions", f"{len(filtered):,}")
    m2.metric("Total Volume", f"${filtered['transaction_amount'].sum():,.0f}")
    m3.metric("Avg Amount", f"${filtered['transaction_amount'].mean():,.2f}")
    m4.metric("Approval Rate", f"{filtered['is_approved'].mean():.1%}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(
        filtered[['transaction_id','date','merchant','channel','customer_segment','transaction_amount','status','cashback_earned','net_revenue']].head(200),
        use_container_width=True, height=400
    )

with tab4:
    st.markdown("<br>", unsafe_allow_html=True)
    camp_sum = camp_df.groupby('campaign').agg(
        total_sent=('sent','sum'), total_rev=('revenue','sum'),
        total_cost=('cost','sum'), avg_conv=('conversion_rate','mean'),
        avg_roas=('roas','mean')
    ).reset_index().sort_values('avg_roas', ascending=False)

    cc1, cc2 = st.columns(2, gap="large")
    with cc1:
        st.markdown("""<div class="chart-card"><div class="chart-card-header">
            <div><div class="chart-card-title">Campaign ROAS Ranking</div>
            <div class="chart-card-sub">Return on ad spend by campaign</div></div>
        </div></div>""", unsafe_allow_html=True)
        fig4 = px.bar(camp_sum, x='avg_roas', y='campaign', orientation='h',
                      color='avg_roas', color_continuous_scale=[[0,'#e0e7ff'],[1,'#4f46e5']])
        fig4.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=0,r=0,t=0,b=0), height=280,
            showlegend=False, coloraxis_showscale=False,
            font=dict(size=10, color='#0f172a'),
            xaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='ROAS',font=dict(color='#94a3b8'))),
            yaxis=dict(tickfont=dict(color='#0f172a',size=10), title=None)
        )
        fig4.update_traces(marker_line_width=0)
        st.plotly_chart(fig4, use_container_width=True)

    with cc2:
        st.markdown("""<div class="chart-card"><div class="chart-card-header">
            <div><div class="chart-card-title">Conversion vs Revenue</div>
            <div class="chart-card-sub">Bubble size = total sent</div></div>
        </div></div>""", unsafe_allow_html=True)
        fig5 = px.scatter(camp_sum, x='avg_conv', y='total_rev', size='total_sent',
                          color='campaign', text='campaign',
                          color_discrete_sequence=['#6366f1','#22c55e','#f59e0b','#ef4444','#0ea5e9','#8b5cf6'])
        fig5.update_traces(textposition='top center', textfont=dict(size=8, color='#0f172a'))
        fig5.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=0,r=0,t=0,b=0), height=280,
            showlegend=False,
            font=dict(size=10, color='#0f172a'),
            xaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='Avg Conversion Rate (%)',font=dict(color='#94a3b8',size=10))),
            yaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='Total Revenue ($)',font=dict(color='#94a3b8',size=10)))
        )
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="chart-card"><div class="chart-card-header">
        <div><div class="chart-card-title">Campaign Performance Summary</div>
        <div class="chart-card-sub">All campaigns ranked by ROAS</div></div>
    </div></div>""", unsafe_allow_html=True)
    camp_display = camp_sum.copy()
    camp_display['total_rev'] = camp_display['total_rev'].apply(lambda x: f"${x/1e6:.1f}M")
    camp_display['avg_conv'] = camp_display['avg_conv'].apply(lambda x: f"{x:.1f}%")
    camp_display['avg_roas'] = camp_display['avg_roas'].apply(lambda x: f"{x:.0f}x")
    camp_display['total_sent'] = camp_display['total_sent'].apply(lambda x: f"{x:,}")
    camp_display.columns = ['Campaign','Total Sent','Revenue','Cost','Avg Conversion','ROAS']
    st.dataframe(camp_display[['Campaign','Total Sent','Revenue','Avg Conversion','ROAS']], use_container_width=True)

st.markdown("""
<div class="built-by-card">
    <div class="built-by-left">
        <div class="built-by-avatar">P</div>
        <div>
            <div class="built-by-name">Priyanka Kapoor</div>
            <div class="built-by-title">MS Business Analytics — Montclair State University 2026</div>
            <div class="built-by-sub">Built NexPay Analytics · MedScan AI · Published AI researcher · Open to work</div>
        </div>
    </div>
    <div class="built-by-links">
        <a href="https://github.com/PriyankaKapoor4202" class="built-by-link">GitHub</a>
        <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6669899" class="built-by-link">Research</a>
        <a href="https://breast-cancer-detection-ai-wnn9lf9wtmywjaeuhckuv9.streamlit.app" class="built-by-link">MedScan AI</a>
    </div>
</div>
""", unsafe_allow_html=True)
