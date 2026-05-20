import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()

st.set_page_config(
    page_title="MarketIQ | Agentic Marketing Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.stApp { background-color: #f0f3f7; }

.top-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 20px 32px;
    border-radius: 12px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.header-title { color: white; font-size: 1.4rem; font-weight: 700; }
.header-sub { color: #a8bdd4; font-size: 0.8rem; margin-top: 2px; }
.header-badge {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 6px 16px;
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
}

.kpi-card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    border: 1px solid #dde3ed;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: #0f3460;
}
.kpi-card.green::before { background: #2e7d32; }
.kpi-card.teal::before { background: #00838f; }
.kpi-card.purple::before { background: #6a1b9a; }
.kpi-value { font-size: 1.8rem; font-weight: 800; color: #1a2b45; line-height: 1; }
.kpi-label { font-size: 0.7rem; color: #8a9ab0; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 6px; font-weight: 600; }
.kpi-trend { font-size: 0.72rem; color: #2e7d32; font-weight: 600; margin-top: 6px; }

.chat-container {
    background: white;
    border-radius: 12px;
    border: 1px solid #dde3ed;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.chat-header {
    background: #1a1a2e;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.chat-header-title { color: white; font-size: 0.85rem; font-weight: 600; }
.chat-header-sub { color: #a8bdd4; font-size: 0.7rem; }
.agent-dot { width: 8px; height: 8px; background: #4caf50; border-radius: 50%; }

.message-user {
    background: #0f3460;
    color: white;
    padding: 12px 16px;
    border-radius: 12px 12px 4px 12px;
    margin: 8px 0 8px 40px;
    font-size: 0.85rem;
    line-height: 1.5;
}
.message-agent {
    background: #f7f9fc;
    border: 1px solid #edf1f7;
    color: #1a2b45;
    padding: 14px 16px;
    border-radius: 12px 12px 12px 4px;
    margin: 8px 40px 8px 0;
    font-size: 0.85rem;
    line-height: 1.6;
}
.message-label {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}
.message-label.user { color: #a8bdd4; }
.message-label.agent { color: #0f3460; }

.panel {
    background: white;
    border-radius: 10px;
    border: 1px solid #dde3ed;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    overflow: hidden;
    margin-bottom: 16px;
}
.panel-header {
    padding: 12px 18px;
    border-bottom: 1px solid #edf1f7;
    background: #fafbfc;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.panel-title { font-size: 0.78rem; font-weight: 700; color: #1a2b45; text-transform: uppercase; letter-spacing: 0.6px; }
.panel-body { padding: 18px; }

.suggestion-chip {
    display: inline-block;
    background: #e8f0fb;
    color: #0f3460;
    border: 1px solid #c5d8f5;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 4px 4px;
    cursor: pointer;
}

[data-testid="stSidebar"] { background: white !important; border-right: 1px solid #dde3ed !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    campaigns = pd.read_csv('campaign_data.csv')
    customers = pd.read_csv('customer_data.csv')
    return campaigns, customers

campaigns_df, customers_df = load_data()

client = Groq(api_key=st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY"))

def analyze_with_agent(question, campaigns_df, customers_df):
    campaign_summary = campaigns_df.groupby('channel').agg({
        'sent': 'sum',
        'opens': 'sum', 
        'clicks': 'sum',
        'conversions': 'sum',
        'revenue': 'sum',
        'cost': 'sum',
        'roas': 'mean'
    }).round(2).to_string()
    
    top_campaigns = campaigns_df.groupby('campaign')['revenue'].sum().sort_values(ascending=False).head(5).to_string()
    
    customer_segments = customers_df.groupby('segment').agg({
        'total_spend': 'mean',
        'orders': 'mean',
        'churn_risk': 'mean'
    }).round(2).to_string()
    
    monthly = campaigns_df.copy()
    monthly['date'] = pd.to_datetime(monthly['date'])
    monthly['month'] = monthly['date'].dt.strftime('%Y-%m')
    monthly_rev = monthly.groupby('month')['revenue'].sum().to_string()
    
    context = f"""
You are MarketIQ, an expert marketing analytics AI agent. You have access to real campaign and customer data.

CAMPAIGN PERFORMANCE BY CHANNEL:
{campaign_summary}

TOP 5 CAMPAIGNS BY REVENUE:
{top_campaigns}

CUSTOMER SEGMENTS:
{customer_segments}

MONTHLY REVENUE TREND:
{monthly_rev}

TOTAL METRICS:
- Total Campaigns Analyzed: {len(campaigns_df)}
- Total Revenue: ${campaigns_df['revenue'].sum():,.0f}
- Total Ad Spend: ${campaigns_df['cost'].sum():,.0f}
- Overall ROAS: {(campaigns_df['revenue'].sum() / campaigns_df['cost'].sum()):.2f}x
- Total Customers: {len(customers_df)}
- Average Churn Risk: {customers_df['churn_risk'].mean():.2%}

Answer the user's question with specific numbers from the data. Be concise, insightful, and actionable.
Format your response clearly with key metrics highlighted. End with one specific recommendation.
"""
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ],
        max_tokens=500,
        temperature=0.3
    )
    
    return response.choices[0].message.content

if 'messages' in st.session_state and not isinstance(st.session_state.messages, list):
    st.session_state.messages = []
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.markdown("""
<div class="top-header">
    <div>
        <div class="header-title">MarketIQ — Agentic Marketing Analytics</div>
        <div class="header-sub">AI-powered campaign intelligence and customer insights platform</div>
    </div>
    <div class="header-badge">Agent Online</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="background:#1a1a2e;padding:16px;border-radius:10px;margin-bottom:16px">
        <div style="color:white;font-weight:700;font-size:0.9rem">MarketIQ Agent</div>
        <div style="color:#a8bdd4;font-size:0.72rem;margin-top:4px">Powered by Groq LLaMA3</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**Data Sources**")
    st.success("Campaign Data: 200 records")
    st.success("Customer Data: 500 records")
    
    st.markdown("---")
    st.markdown("**Filter Data**")
    channels = ['All'] + list(campaigns_df['channel'].unique())
    selected_channel = st.selectbox("Channel", channels)
    
    st.markdown("---")
    st.markdown("**Agent Settings**")
    st.info("Model: LLaMA3-8B via Groq\nResponse: Real-time\nData: Live CSV")

if selected_channel != 'All':
    filtered_df = campaigns_df[campaigns_df['channel'] == selected_channel]
else:
    filtered_df = campaigns_df

total_revenue = filtered_df['revenue'].sum()
total_cost = filtered_df['cost'].sum()
total_conversions = filtered_df['conversions'].sum()
overall_roas = total_revenue / total_cost if total_cost > 0 else 0
avg_open_rate = filtered_df['open_rate'].mean()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value">${total_revenue:,.0f}</div>
        <div class="kpi-trend">All Campaigns</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-label">Overall ROAS</div>
        <div class="kpi-value">{overall_roas:.1f}x</div>
        <div class="kpi-trend">Return on Ad Spend</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="kpi-card teal">
        <div class="kpi-label">Total Conversions</div>
        <div class="kpi-value">{total_conversions:,}</div>
        <div class="kpi-trend">Across All Channels</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="kpi-card purple">
        <div class="kpi-label">Avg Open Rate</div>
        <div class="kpi-value">{avg_open_rate:.1f}%</div>
        <div class="kpi-trend">Campaign Average</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.markdown("""
    <div class="chat-container">
        <div class="chat-header">
            <div class="agent-dot"></div>
            <div>
                <div class="chat-header-title">MarketIQ Analytics Agent</div>
                <div class="chat-header-sub">Ask anything about your campaigns and customers</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin:12px 0 8px 0">
        <div style="font-size:0.72rem;color:#8a9ab0;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Suggested Questions</div>
        <span class="suggestion-chip">Which channel has the best ROAS?</span>
        <span class="suggestion-chip">What is our top performing campaign?</span>
        <span class="suggestion-chip">Which customer segment is at highest churn risk?</span>
        <span class="suggestion-chip">How is monthly revenue trending?</span>
        <span class="suggestion-chip">Where should we increase budget?</span>
    </div>
    """, unsafe_allow_html=True)
    
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="message-label user">You</div>
                <div class="message-user">{message["content"]}</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message-label agent">MarketIQ Agent</div>
                <div class="message-agent">{message["content"]}</div>
                """, unsafe_allow_html=True)
    
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                "Ask the agent",
                placeholder="e.g. Which campaign generated the most revenue?",
                label_visibility="collapsed"
            )
        with col2:
            submitted = st.form_submit_button("Ask", use_container_width=True)
    
    if submitted and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Agent analyzing..."):
            response = analyze_with_agent(user_input, campaigns_df, customers_df)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with right:
    st.markdown("""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-title">Revenue by Channel</div>
        </div>
    </div>""", unsafe_allow_html=True)
    
    channel_rev = filtered_df.groupby('channel')['revenue'].sum().reset_index()
    fig1 = px.bar(channel_rev, x='channel', y='revenue',
                  color='revenue',
                  color_continuous_scale=['#c5d8f5', '#0f3460'],
                  labels={'revenue': 'Revenue ($)', 'channel': 'Channel'})
    fig1.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=10, r=10, t=10, b=10),
        height=220,
        showlegend=False,
        coloraxis_showscale=False,
        font=dict(size=10)
    )
    fig1.update_traces(marker_line_width=0)
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-title">Customer Segments</div>
        </div>
    </div>""", unsafe_allow_html=True)
    
    seg_data = customers_df.groupby('segment').size().reset_index(name='count')
    fig2 = px.pie(seg_data, values='count', names='segment',
                  color_discrete_sequence=['#0f3460', '#1a4a8a', '#2d6cbe', '#5a9fd4', '#a8c4e0'])
    fig2.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=10, r=10, t=10, b=10),
        height=220,
        font=dict(size=10),
        legend=dict(font=dict(size=9))
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label', textfont_size=9)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-title">Top Campaigns by ROAS</div>
        </div>
    </div>""", unsafe_allow_html=True)
    
    top_roas = filtered_df.groupby('campaign')['roas'].mean().sort_values(ascending=False).head(5).reset_index()
    fig3 = px.bar(top_roas, x='roas', y='campaign', orientation='h',
                  color='roas',
                  color_continuous_scale=['#c5d8f5', '#0f3460'],
                  labels={'roas': 'ROAS', 'campaign': ''})
    fig3.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=10, r=10, t=10, b=10),
        height=220,
        showlegend=False,
        coloraxis_showscale=False,
        font=dict(size=9)
    )
    fig3.update_traces(marker_line_width=0)
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
<div style="background:#1a1a2e;color:#6b8caa;text-align:center;padding:14px;border-radius:10px;margin-top:20px;font-size:0.72rem">
    <strong style="color:#a8bdd4">MarketIQ</strong> | Agentic Marketing Analytics Platform | 
    Built by <strong style="color:#a8bdd4">Priyanka Kapoor</strong> | 
    MS Business Analytics, Montclair State University 2026 | 
    Powered by Groq LLaMA3 | 
    <a href="https://github.com/PriyankaKapoor4202" style="color:#6aadde">GitHub</a>
</div>
""", unsafe_allow_html=True)
