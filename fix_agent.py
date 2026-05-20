import re

with open('app.py', 'r') as f:
    content = f.read()

old_func = '''def analyze_with_agent(question, campaigns_df, customers_df):
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
        max_tokens=300,
        temperature=0.3
    )
    
    return response.choices[0].message.content'''

new_func = '''def analyze_with_agent(question, campaigns_df, customers_df):
    ch = campaigns_df.groupby('channel').agg({'revenue':'sum','cost':'sum','conversions':'sum'}).round(0)
    top5 = campaigns_df.groupby('campaign')['revenue'].sum().sort_values(ascending=False).head(3)
    seg = customers_df.groupby('segment')['churn_risk'].mean().round(2)
    total_rev = campaigns_df['revenue'].sum()
    total_cost = campaigns_df['cost'].sum()
    roas = total_rev/total_cost

    context = f"""You are MarketIQ, a marketing analytics AI. Answer concisely with numbers.

KEY METRICS:
Total Revenue: ${total_rev:,.0f} | Ad Spend: ${total_cost:,.0f} | ROAS: {roas:.1f}x
Customers: {len(customers_df)} | Avg Churn Risk: {customers_df['churn_risk'].mean():.1%}

CHANNEL PERFORMANCE:
{ch.to_string()}

TOP 3 CAMPAIGNS BY REVENUE:
{top5.to_string()}

CHURN RISK BY SEGMENT:
{seg.to_string()}

Answer the question with specific numbers. Be concise. End with one recommendation."""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ],
        max_tokens=250,
        temperature=0.3
    )
    
    return response.choices[0].message.content'''

content = content.replace(old_func, new_func)

with open('app.py', 'w') as f:
    f.write(content)

print("Fixed")
