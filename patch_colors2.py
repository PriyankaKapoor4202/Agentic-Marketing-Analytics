with open('app.py', 'r') as f:
    content = f.read()

old = """        # Color by churn risk rank: green=safest, red=riskiest
        seg_sorted = seg.sort_values('churn')
        risk_colors = ['#16a34a','#65a30d','#ca8a04','#ea580c','#dc2626']
        palette = {row['segment']: risk_colors[i] for i, (_, row) in enumerate(seg_sorted.iterrows())}"""
new = """        # Color by churn risk rank: light blue=lowest, darkest navy=highest
        seg_sorted = seg.sort_values('churn')
        risk_colors = ['#bfdbfe','#60a5fa','#2563eb','#1d4ed8','#1e3a8a']
        palette = {row['segment']: risk_colors[i] for i, (_, row) in enumerate(seg_sorted.iterrows())}"""

content = content.replace(old, new)

with open('app.py', 'w') as f:
    f.write(content)

print("OK" if '#1e3a8a' in open('app.py').read() else "FAILED")
