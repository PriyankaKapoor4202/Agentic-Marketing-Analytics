import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_campaign_data():
    campaigns = ['Summer Sale Email', 'Back to School Push', 'Flash Sale SMS', 
                 'Holiday Preview', 'New User Welcome', 'Re-engagement Flow',
                 'Product Launch', 'Weekly Newsletter']
    channels = ['Email', 'SMS', 'Push Notification', 'Social Media', 'Paid Search']
    rows = []
    base_date = datetime(2026, 1, 1)
    for i in range(200):
        campaign = random.choice(campaigns)
        channel = random.choice(channels)
        date = base_date + timedelta(days=random.randint(0, 140))
        sent = random.randint(5000, 50000)
        open_rate = random.uniform(0.15, 0.45)
        click_rate = random.uniform(0.02, 0.15)
        conversion_rate = random.uniform(0.01, 0.08)
        opens = int(sent * open_rate)
        clicks = int(sent * click_rate)
        conversions = int(sent * conversion_rate)
        revenue = conversions * random.uniform(25, 150)
        cost = sent * random.uniform(0.001, 0.005)
        rows.append({
            'date': date.strftime('%Y-%m-%d'),
            'campaign': campaign,
            'channel': channel,
            'sent': sent,
            'opens': opens,
            'clicks': clicks,
            'conversions': conversions,
            'revenue': round(revenue, 2),
            'cost': round(cost, 2),
            'open_rate': round(open_rate * 100, 2),
            'click_rate': round(click_rate * 100, 2),
            'conversion_rate': round(conversion_rate * 100, 2),
            'roas': round(revenue / cost, 2)
        })
    return pd.DataFrame(rows)

def generate_customer_data():
    segments = ['High Value', 'At Risk', 'New Customer', 'Loyal', 'Dormant']
    rows = []
    for i in range(500):
        segment = random.choice(segments)
        rows.append({
            'customer_id': f'CUS{i:04d}',
            'segment': segment,
            'total_spend': round(random.uniform(50, 5000), 2),
            'orders': random.randint(1, 50),
            'last_purchase_days': random.randint(1, 365),
            'email_engagement': random.choice(['High', 'Medium', 'Low']),
            'churn_risk': round(random.uniform(0, 1), 2)
        })
    return pd.DataFrame(rows)

if __name__ == '__main__':
    df1 = generate_campaign_data()
    df1.to_csv('campaign_data.csv', index=False)
    df2 = generate_customer_data()
    df2.to_csv('customer_data.csv', index=False)
    print('Data generated successfully')
