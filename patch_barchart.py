with open('app.py', 'r') as f:
    content = f.read()

old = """        colors = ['#4f46e5','#6366f1','#818cf8','#a5b4fc','#c7d2fe']
        fig1 = go.Figure()
        for i, row in ch.iterrows():
            fig1.add_trace(go.Bar(
                x=[row['channel']], y=[row['transaction_amount']],
                marker_color=colors[i % len(colors)],
                marker_line_width=0,
                name=row['channel'],
                text=f"${row['transaction_amount']/1e6:.2f}M ({row['pct']}%)",
                textposition='outside',
                textfont=dict(size=10, color='#334155', family='Inter'),
            ))"""

new = """        colors = ['#dbeafe','#93c5fd','#60a5fa','#2563eb','#1e3a8a']
        fig1 = go.Figure()
        for idx, (_, row) in enumerate(ch.iterrows()):
            fig1.add_trace(go.Bar(
                x=[row['channel']], y=[row['transaction_amount']],
                marker_color=colors[idx % len(colors)],
                marker_line_width=0,
                name=row['channel'],
                text=f"${row['transaction_amount']/1e6:.2f}M ({row['pct']}%)",
                textposition='outside',
                textfont=dict(size=10, color='#334155', family='Inter'),
            ))"""

old_xaxis = """            xaxis=dict(
                showgrid=False, zeroline=False,
                tickfont=dict(color='#334155', size=11, family='Inter'),
                title=None,
                showline=True, linecolor='#e2e8f0'
            ),"""

new_xaxis = """            xaxis=dict(
                showgrid=False, zeroline=False,
                tickfont=dict(color='#334155', size=11, family='Inter'),
                tickangle=0,
                title=None,
                showline=True, linecolor='#e2e8f0'
            ),"""

content = content.replace(old, new)
content = content.replace(old_xaxis, new_xaxis)

with open('app.py', 'w') as f:
    f.write(content)

print("OK" if '#1e3a8a' in open('app.py').read() else "FAILED")
