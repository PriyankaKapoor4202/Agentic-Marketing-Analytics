with open('app.py', 'r') as f:
    content = f.read()

old = "        palette = {'Student':'#6366f1','Standard':'#ef4444','Business':'#f59e0b','Premium':'#f97316','Enterprise':'#22c55e'}"
new = """        # Color by churn risk rank: green=safest, red=riskiest
        seg_sorted = seg.sort_values('churn')
        risk_colors = ['#16a34a','#65a30d','#ca8a04','#ea580c','#dc2626']
        palette = {row['segment']: risk_colors[i] for i, (_, row) in enumerate(seg_sorted.iterrows())}"""

content = content.replace(old, new)

with open('app.py', 'w') as f:
    f.write(content)

print("OK" if 'risk_colors' in open('app.py').read() else "FAILED")
