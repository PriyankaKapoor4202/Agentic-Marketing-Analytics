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
    page_title="MarketIQ Enterprise | Payments Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.stApp { background: #f0f2f5; }

.top-nav {
    background: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    padding: 0 32px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    margin: -1rem -1rem 0 -1rem;
}
.nav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}
.nav-logo {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #1a56db, #0e3fa8);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 16px; font-weight: 800;
}
.nav-title { font-size: 1rem; font-weight: 700; color: #0f172a; }
.nav-sub { font-size: 0.68rem; color: #64748b; }
.nav-right { display: flex; align-items: center; gap: 16px; }
.nav-status {
    display: flex; align-items: center; gap: 6px;
    background: #f0fdf4; border: 1px solid #bbf7d0;
    border-radius: 20px; padding: 5px 12px;
    font-size: 0.72rem; color: #166534; font-weight: 600;
}
.status-dot { width: 7px; height: 7px; background: #22c55e; border-radius: 50%; }
.nav-time { font-size: 0.72rem; color: #94a3b8; }

.page-header {
    padding: 24px 0 16px 0;
}
.page-title { font-size: 1.4rem; font-weight: 700; color: #0f172a; letter-spacing: -0.3px; }
.page-sub { font-size: 0.82rem; color: #64748b; margin-top: 4px; }
.breadcrumb { font-size: 0.7rem; color: #94a3b8; margin-bottom: 8px; }
.breadcrumb-link { color: #1a56db; }

.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 20px 22px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 3px;
    background: linear-gradient(90deg, #1a56db, #3b82f6);
}
.kpi-card.green::after { background: linear-gradient(90deg, #16a34a, #22c55e); }
.kpi-card.purple::after { background: linear-gradient(90deg, #7c3aed, #a78bfa); }
.kpi-card.orange::after { background: linear-gradient(90deg, #ea580c, #fb923c); }
.kpi-label { font-size: 0.7rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 8px; }
.kpi-value { font-size: 1.9rem; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; line-height: 1; }
.kpi-change { font-size: 0.72rem; font-weight: 600; margin-top: 8px; }
.kpi-change.up { color: #16a34a; }
.kpi-change.down { color: #dc2626; }

.card {
    background: white;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    overflow: hidden;
    margin-bottom: 16px;
}
.card-header {
    padding: 14px 20px;
    border-bottom: 1px solid #f1f5f9;
    display: flex; align-items: center; justify-content: space-between;
    background: #fafbfc;
}
.card-title { font-size: 0.8rem; font-weight: 700; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px; }
.card-sub { font-size: 0.68rem; color: #94a3b8; }
.card-body { padding: 20px; }

.chat-bubble {
    position: fixed;
    bottom: 24px; right: 24px;
    z-index: 1000;
}
.chat-btn {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #1a56db, #0e3fa8);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(26,86,219,0.4);
    font-size: 24px;
    border: none;
    color: white;
}
.chat-panel {
    position: fixed;
    bottom: 90px; right: 24px;
    width: 380px;
    background: white;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    z-index: 1000;
    overflow: hidden;
}
.chat-panel-header {
    background: linear-gradient(135deg, #1a56db, #0e3fa8);
    padding: 16px 20px;
    display: flex; align-items: center; justify-content: space-between;
}
.chat-panel-title { color: white; font-size: 0.9rem; font-weight: 700; }
.chat-panel-sub { color: rgba(255,255,255,0.7); font-size: 0.7rem; margin-top: 2px; }
.chat-messages { padding: 16px; max-height: 320px; overflow-y: auto; }
.msg-user {
    background: #1a56db; color: white;
    padding: 10px 14px; border-radius: 12px 12px 4px 12px;
    font-size: 0.82rem; margin: 8px 0 8px 32px; line-height: 1.5;
}
.msg-agent {
    background: #f8fafc; border: 1px solid #e2e8f0;
    padding: 10px 14px; border-radius: 12px 12px 12px 4px;
    font-size: 0.82rem; margin: 8px 32px 8px 0; line-height: 1.6; color: #0f172a;
}
.msg-label { font-size: 0.62rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 3px; }
.msg-label.user { color: #94a3b8; text-align: right; }
.msg-label.agent { color: #1a56db; }
.quick-chips { padding: 0 16px 12px; display: flex; flex-wrap: wrap; gap: 6px; }
.chip {
    background: #eff6ff; color: #1a56db;
    border: 1px solid #bfdbfe; border-radius: 16px;
    padding: 5px 12px; font-size: 0.72rem; font-weight: 500;
    cursor: pointer;
}

.metric-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
.metric-table th {
    background: #f8fafc; color: #64748b;
    font-size: 0.68rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.5px; padding: 10px 14px;
    border-bottom: 1px solid #e2e8f0; text-align: left;
}
.metric-table td { padding: 10px 14px; border-bottom: 1px solid #f1f5f9; color: #0f172a; }
.metric-table tr:last-child td { border-bottom: none; }
.badge {
    padding: 3px 8px; border-radius: 12px;
    font-size: 0.65rem; font-weight: 600;
}
.badge-green { background: #f0fdf4; color: #166534; }
.badge-blue { background: #eff6ff; color: #1e40af; }
.badge-red { background: #fef2f2; color: #991b1b; }

[data-testid="stSidebar"] { display: none; }
div[data-testid="stMetricValue"] { font-size: 1.4rem !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    txn = pd.read_csv('transaction_data.csv')
    campaigns = pd.read_csv('campaign_data.csv')
    customers = pd.read_csv('customer_data.csv')
    txn['date'] = pd.to_datetime(txn['date'])
    campaigns['date'] = pd.to_datetime(campaigns['date'])
    return txn, campaigns, customers

txn_df, camp_df, cust_df = load_data()

def get_groq_client():
    key = st.secrets.get("GROQ_API_KEY") if hasattr(st, 'secrets') and "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY")
    return Groq(api_key=key)

def analyze(question):
    try:
        approved = txn_df[txn_df['is_approved']==1]
        channel_rev = txn_df.groupby('channel')['net_revenue'].sum().round(0).to_dict()
        top_merchants = txn_df.groupby('merchant')['transaction_amount'].sum().sort_values(ascending=False).head(5).round(0).to_dict()
        seg_churn = cust_df.groupby('segment')['churn_risk'].mean().round(3).to_dict()
        camp_roas = camp_df.groupby('campaign')['roas'].mean().round(1).to_dict()
        
        context = f"""You are MarketIQ, an elite payments analytics AI for a fintech company similar to Visa.
Answer as a senior payments analyst presenting to the CEO. Be specific, use numbers, be concise.

PAYMENT METRICS:
Total Transactions: {len(txn_df):,}
Total Volume: ${txn_df['transaction_amount'].sum():,.0f}
Approved Transactions: {txn_df['is_approved'].sum():,} ({txn_df['is_approved'].mean():.1%} approval rate)
Net Revenue: ${txn_df['net_revenue'].sum():,.0f}
Total Customers: {len(cust_df):,}
Avg Transaction: ${txn_df['transaction_amount'].mean():,.2f}

REVENUE BY CHANNEL: {channel_rev}
TOP MERCHANTS: {top_merchants}
CHURN RISK BY SEGMENT: {seg_churn}
CAMPAIGN ROAS: {camp_roas}

Answer concisely in 3-4 sentences max. Use $ and % signs. End with one strategic recommendation."""

        client = get_groq_client()
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": question}
            ],
            max_tokens=200,
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Agent error: {str(e)[:100]}"

if 'chat_open' not in st.session_state:
    st.session_state.chat_open = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'pending_question' not in st.session_state:
    st.session_state.pending_question = None

now = datetime.now()

st.markdown(f"""
<div class="top-nav">
    <div class="nav-brand">
        <div class="nav-logo">M</div>
        <div>
            <div class="nav-title">MarketIQ Enterprise</div>
            <div class="nav-sub">Payments Intelligence Platform</div>
        </div>
    </div>
    <div class="nav-right">
        <div class="nav-status"><span class="status-dot"></span>Live Data</div>
        <div class="nav-time">{now.strftime('%b %d, %Y  %H:%M')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <div class="breadcrumb"><span class="breadcrumb-link">Analytics</span> / Executive Dashboard</div>
    <div class="page-title">Payments Executive Dashboard</div>
    <div class="page-sub">Real-time transaction intelligence and campaign performance for 100,000+ payment records</div>
</div>
""", unsafe_allow_html=True)

approved_df = txn_df[txn_df['is_approved']==1]
total_volume = txn_df['transaction_amount'].sum()
total_revenue = txn_df['net_revenue'].sum()
approval_rate = txn_df['is_approved'].mean()
avg_txn = txn_df['transaction_amount'].mean()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Payment Volume</div>
        <div class="kpi-value">${total_volume/1e6:.1f}M</div>
        <div class="kpi-change up">100,000 transactions</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-label">Net Revenue</div>
        <div class="kpi-value">${total_revenue/1e6:.2f}M</div>
        <div class="kpi-change up">Processing fees minus cashback</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="kpi-card purple">
        <div class="kpi-label">Approval Rate</div>
        <div class="kpi-value">{approval_rate:.1%}</div>
        <div class="kpi-change up">{txn_df['is_approved'].sum():,} approved</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="kpi-card orange">
        <div class="kpi-label">Avg Transaction</div>
        <div class="kpi-value">${avg_txn:,.0f}</div>
        <div class="kpi-change up">Across all channels</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""<div class="card"><div class="card-header">
        <div class="card-title">Transaction Volume by Channel</div>
        <div class="card-sub">Net revenue breakdown</div>
    </div></div>""", unsafe_allow_html=True)
    
    ch_data = txn_df.groupby('channel').agg(
        volume=('transaction_amount', 'sum'),
        revenue=('net_revenue', 'sum'),
        count=('transaction_id', 'count')
    ).reset_index().sort_values('volume', ascending=False)
    
    fig1 = px.bar(ch_data, x='channel', y='volume',
                  color='revenue',
                  color_continuous_scale=['#bfdbfe', '#1a56db'],
                  labels={'volume': 'Volume ($)', 'channel': ''})
    fig1.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0, r=0, t=10, b=0), height=240,
        showlegend=False, coloraxis_showscale=False,
        font=dict(size=10, color='#0f172a')
    )
    fig1.update_traces(marker_line_width=0)
    fig1.update_xaxes(showgrid=False, tickfont=dict(size=9))
    fig1.update_yaxes(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(size=9))
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""<div class="card"><div class="card-header">
        <div class="card-title">Monthly Transaction Trend</div>
        <div class="card-sub">Volume over time</div>
    </div></div>""", unsafe_allow_html=True)
    
    monthly = txn_df.copy()
    monthly['month'] = monthly['date'].dt.to_period('M').astype(str)
    monthly_data = monthly.groupby('month')['transaction_amount'].sum().reset_index()
    
    fig2 = px.area(monthly_data, x='month', y='transaction_amount',
                   color_discrete_sequence=['#1a56db'])
    fig2.update_traces(fill='tozeroy', fillcolor='rgba(26,86,219,0.08)', line=dict(width=2))
    fig2.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0, r=0, t=10, b=0), height=220,
        font=dict(size=10, color='#0f172a')
    )
    fig2.update_xaxes(showgrid=False, tickfont=dict(size=8), tickangle=45)
    fig2.update_yaxes(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(size=9))
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("""<div class="card"><div class="card-header">
        <div class="card-title">Customer Segment Analysis</div>
        <div class="card-sub">Churn risk and spend</div>
    </div></div>""", unsafe_allow_html=True)
    
    seg_data = cust_df.groupby('segment').agg(
        count=('customer_id', 'count'),
        avg_spend=('total_spend', 'mean'),
        churn_risk=('churn_risk', 'mean')
    ).reset_index()
    
    fig3 = px.scatter(seg_data, x='avg_spend', y='churn_risk',
                      size='count', color='segment', text='segment',
                      color_discrete_sequence=['#1a56db','#22c55e','#7c3aed','#ea580c','#0891b2'])
    fig3.update_traces(textposition='top center', textfont=dict(size=9))
    fig3.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0, r=0, t=10, b=0), height=240,
        showlegend=False, font=dict(size=10)
    )
    fig3.update_xaxes(showgrid=True, gridcolor='#f1f5f9', title='Avg Spend ($)', tickfont=dict(size=9))
    fig3.update_yaxes(showgrid=True, gridcolor='#f1f5f9', title='Churn Risk', tickfont=dict(size=9))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""<div class="card"><div class="card-header">
        <div class="card-title">Top Merchants by Volume</div>
        <div class="card-sub">Transaction amount ranking</div>
    </div></div>""", unsafe_allow_html=True)
    
    top_merch = txn_df.groupby('merchant').agg(
        volume=('transaction_amount', 'sum'),
        count=('transaction_id', 'count'),
        approval=('is_approved', 'mean')
    ).sort_values('volume', ascending=False).head(8).reset_index()
    
    table_html = """<table class="metric-table">
    <tr><th>Merchant</th><th>Volume</th><th>Txns</th><th>Approval</th></tr>"""
    for _, row in top_merch.iterrows():
        badge_class = 'badge-green' if row['approval'] > 0.8 else 'badge-blue'
        table_html += f"""<tr>
            <td><strong>{row['merchant']}</strong></td>
            <td>${row['volume']/1000:.0f}K</td>
            <td>{row['count']:,}</td>
            <td><span class="badge {badge_class}">{row['approval']:.0%}</span></td>
        </tr>"""
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""<div class="card"><div class="card-header">
    <div class="card-title">Campaign Performance Overview</div>
    <div class="card-sub">ROAS and conversion across all campaigns</div>
</div></div>""", unsafe_allow_html=True)

camp_summary = camp_df.groupby('campaign').agg(
    total_sent=('sent', 'sum'),
    total_revenue=('revenue', 'sum'),
    total_cost=('cost', 'sum'),
    avg_conversion=('conversion_rate', 'mean'),
    avg_roas=('roas', 'mean')
).reset_index().sort_values('avg_roas', ascending=False)

c1, c2 = st.columns(2)
with c1:
    fig4 = px.bar(camp_summary, x='avg_roas', y='campaign', orientation='h',
                  color='avg_roas', color_continuous_scale=['#bfdbfe', '#1a56db'],
                  labels={'avg_roas': 'ROAS', 'campaign': ''})
    fig4.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0, r=0, t=10, b=0), height=220,
        showlegend=False, coloraxis_showscale=False, font=dict(size=10)
    )
    fig4.update_traces(marker_line_width=0)
    fig4.update_xaxes(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(size=9))
    fig4.update_yaxes(tickfont=dict(size=9))
    st.plotly_chart(fig4, use_container_width=True)

with c2:
    fig5 = px.scatter(camp_summary, x='avg_conversion', y='total_revenue',
                      size='total_sent', color='campaign', text='campaign',
                      color_discrete_sequence=px.colors.qualitative.Set2)
    fig5.update_traces(textposition='top center', textfont=dict(size=8))
    fig5.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0, r=0, t=10, b=0), height=220,
        showlegend=False, font=dict(size=10)
    )
    fig5.update_xaxes(showgrid=True, gridcolor='#f1f5f9', title='Conversion Rate (%)', tickfont=dict(size=9))
    fig5.update_yaxes(showgrid=True, gridcolor='#f1f5f9', title='Total Revenue ($)', tickfont=dict(size=9))
    st.plotly_chart(fig5, use_container_width=True)

st.markdown(f"""
<div style="background:#0f172a;color:#64748b;text-align:center;padding:16px;border-radius:12px;margin-top:16px;font-size:0.72rem;line-height:1.8">
    <strong style="color:#94a3b8">MarketIQ Enterprise</strong> &nbsp;|&nbsp;
    Payments Intelligence Platform &nbsp;|&nbsp;
    Built by <strong style="color:#94a3b8">Priyanka Kapoor</strong> &nbsp;|&nbsp;
    MS Business Analytics, Montclair State University 2026 &nbsp;|&nbsp;
    <a href="https://github.com/PriyankaKapoor4202" style="color:#3b82f6">GitHub</a> &nbsp;|&nbsp;
    Powered by Groq LLaMA3 &nbsp;|&nbsp; {len(txn_df):,} transactions analyzed
</div>
""", unsafe_allow_html=True)

if st.session_state.chat_open:
    st.markdown("""
    <div class="chat-panel">
        <div class="chat-panel-header">
            <div>
                <div class="chat-panel-title">MarketIQ AI Agent</div>
                <div class="chat-panel-sub">Ask anything about payments and campaigns</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div style="position:fixed;bottom:90px;right:24px;width:380px;background:white;
        border-radius:0 0 16px 16px;border:1px solid #e2e8f0;border-top:none;
        box-shadow:0 20px 60px rgba(0,0,0,0.15);z-index:1000;padding:12px 16px;">
        """, unsafe_allow_html=True)
        
        for msg in st.session_state.messages[-6:]:
            if msg['role'] == 'user':
                st.markdown(f"""
                <div class="msg-label user">You</div>
                <div class="msg-user">{msg['content']}</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-label agent">MarketIQ Agent</div>
                <div class="msg-agent">{msg['content']}</div>
                """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="quick-chips">
            <span class="chip">Best performing channel?</span>
            <span class="chip">Churn risk insights?</span>
            <span class="chip">Top campaign ROAS?</span>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("chat_form", clear_on_submit=True):
            col_input, col_btn = st.columns([4, 1])
            with col_input:
                user_input = st.text_input("Ask", placeholder="Ask about your payments data...", label_visibility="collapsed")
            with col_btn:
                submit = st.form_submit_button("Send")
        
        if submit and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Analyzing..."):
                response = analyze(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

col_bubble = st.columns([6,1])[1]
with col_bubble:
    if st.button("💬" if not st.session_state.chat_open else "✕", key="chat_toggle"):
        st.session_state.chat_open = not st.session_state.chat_open
        st.rerun()
