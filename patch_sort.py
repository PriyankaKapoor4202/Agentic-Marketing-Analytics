with open('app.py', 'r') as f:
    content = f.read()

old = "        ch = txn_df.groupby('channel')['transaction_amount'].sum().reset_index().sort_values('transaction_amount', ascending=False)"
new = "        ch = txn_df.groupby('channel')['transaction_amount'].sum().reset_index().sort_values('transaction_amount', ascending=True)"

content = content.replace(old, new)

with open('app.py', 'w') as f:
    f.write(content)

print("OK" if "ascending=True" in open('app.py').read() else "FAILED")
