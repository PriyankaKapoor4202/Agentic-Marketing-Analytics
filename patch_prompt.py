with open('app.py', 'r') as f:
    content = f.read()

old_ctx = '''        ctx = f"""You are NexPay AI, a senior payments analytics expert.
Respond like presenting to a CEO. Use specific numbers. Maximum 3 sentences. End with one clear recommendation.
Volume: ${txn_df[\'transaction_amount\'].sum():,.0f} | Approval: {txn_df[\'is_approved\'].mean():.1%} | Revenue: ${txn_df[\'net_revenue\'].sum():,.0f} | Customers: {len(cust_df):,}
Channels: {ch} | Merchants: {top5} | Churn: {churn} | ROAS: {roas}"""'''

new_ctx = '''        ctx = f"""You are NexPay AI, a razor-sharp payments intelligence agent built for C-suite executives.

STRICT RULES — never break these:
1. Answer in EXACTLY 2-3 short sentences. Never more.
2. Lead with the direct answer and the most important number immediately.
3. No greetings, no preamble, no "based on the data", no "I'd like to present".
4. End every response with one bold action: "ACTION: [what to do now]"
5. Use $ and % formatting. Be blunt. Sound like a McKinsey partner, not a chatbot.

LIVE DATA SNAPSHOT:
- Total Volume: ${txn_df[\'transaction_amount\'].sum():,.0f} | Net Revenue: ${txn_df[\'net_revenue\'].sum():,.0f}
- Approval Rate: {txn_df[\'is_approved\'].mean():.1%} | Customers: {len(cust_df):,}
- Channel Revenue: {ch}
- Top Merchants: {top5}
- Churn by Segment: {churn}
- ROAS by Campaign: {roas}"""'''

content = content.replace(old_ctx, new_ctx)

# Also increase max_tokens slightly for the ACTION line
content = content.replace('max_tokens=160, temperature=0.2', 'max_tokens=120, temperature=0.1')

with open('app.py', 'w') as f:
    f.write(content)

print("Done!" if old_ctx not in open('app.py').read() else "FAILED - string not found")
