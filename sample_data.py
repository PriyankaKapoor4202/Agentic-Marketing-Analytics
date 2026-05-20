import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

def generate_fintech_data():
    merchants = ['Amazon', 'Walmart', 'Target', 'Shopify Store', 'Netflix', 
                 'Uber', 'DoorDash', 'Apple Store', 'Google Play', 'Airbnb',
                 'Delta Airlines', 'Marriott Hotels', 'Best Buy', 'Home Depot',
                 'Starbucks', 'McDonald\'s', 'CVS Pharmacy', 'Walgreens']
    
    channels = ['Credit Card', 'Debit Card', 'Digital Wallet', 'Buy Now Pay Later', 'ACH Transfer']
    regions = ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West Coast', 'International']
    segments = ['Premium', 'Standard', 'Business', 'Enterprise', 'Student']
    campaign_types = ['Cashback Offer', 'Points Multiplier', 'Zero APR Promo', 
                      'Sign-up Bonus', 'Referral Program', 'Merchant Partnership']
    statuses = ['Approved', 'Approved', 'Approved', 'Approved', 'Declined', 'Pending']
    
    rows = []
    base_date = datetime(2025, 1, 1)
    
    for i in range(100000):
        merchant = random.choice(merchants)
        channel = random.choice(channels)
        region = random.choice(regions)
        segment = random.choice(segments)
        campaign = random.choice(campaign_types)
        date = base_date + timedelta(days=random.randint(0, 365))
        amount = round(np.random.lognormal(4, 1.2), 2)
        status = random.choice(statuses)
        is_approved = 1 if status == 'Approved' else 0
        cashback = round(amount * random.uniform(0.01, 0.05), 2) if is_approved else 0
        processing_fee = round(amount * 0.029 + 0.30, 2)
        
        rows.append({
            'transaction_id': f'TXN{i:08d}',
            'date': date.strftime('%Y-%m-%d'),
            'merchant': merchant,
            'channel': channel,
            'region': region,
            'customer_segment': segment,
            'campaign_type': campaign,
            'transaction_amount': amount,
            'status': status,
            'is_approved': is_approved,
            'cashback_earned': cashback,
            'processing_fee': processing_fee,
            'net_revenue': round(processing_fee - cashback * 0.5, 2)
        })
    
    return pd.DataFrame(rows)

def generate_campaign_performance():
    campaigns = ['Cashback Offer', 'Points Multiplier', 'Zero APR Promo',
                 'Sign-up Bonus', 'Referral Program', 'Merchant Partnership']
    rows = []
    base_date = datetime(2025, 1, 1)
    
    for campaign in campaigns:
        for month in range(12):
            date = base_date + timedelta(days=month*30)
            sent = random.randint(50000, 500000)
            open_rate = random.uniform(0.18, 0.42)
            click_rate = random.uniform(0.03, 0.18)
            conversion_rate = random.uniform(0.01, 0.09)
            opens = int(sent * open_rate)
            clicks = int(sent * click_rate)
            conversions = int(sent * conversion_rate)
            revenue = conversions * random.uniform(150, 800)
            cost = sent * random.uniform(0.002, 0.008)
            
            rows.append({
                'date': date.strftime('%Y-%m-%d'),
                'campaign': campaign,
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
    segments = ['Premium', 'Standard', 'Business', 'Enterprise', 'Student']
    rows = []
    
    for i in range(50000):
        segment = random.choice(segments)
        spend_multiplier = {'Premium': 5, 'Enterprise': 8, 'Business': 4, 'Standard': 2, 'Student': 1}[segment]
        rows.append({
            'customer_id': f'CUS{i:06d}',
            'segment': segment,
            'total_spend': round(random.uniform(500, 50000) * spend_multiplier * 0.1, 2),
            'total_transactions': random.randint(5, 500),
            'avg_transaction': round(random.uniform(25, 2000), 2),
            'months_active': random.randint(1, 48),
            'churn_risk': round(random.uniform(0, 1), 2),
            'credit_score': random.randint(580, 850),
            'cashback_earned': round(random.uniform(10, 2000), 2),
            'preferred_channel': random.choice(['Credit Card', 'Debit Card', 'Digital Wallet', 'BNPL'])
        })
    
    return pd.DataFrame(rows)

if __name__ == '__main__':
    print("Generating 100,000 transaction records...")
    df1 = generate_fintech_data()
    df1.to_csv('transaction_data.csv', index=False)
    print(f"Transactions: {len(df1):,} records")
    
    print("Generating campaign performance data...")
    df2 = generate_campaign_performance()
    df2.to_csv('campaign_data.csv', index=False)
    print(f"Campaigns: {len(df2):,} records")
    
    print("Generating 50,000 customer records...")
    df3 = generate_customer_data()
    df3.to_csv('customer_data.csv', index=False)
    print(f"Customers: {len(df3):,} records")
    
    print("All data generated successfully!")
