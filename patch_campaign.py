with open('app.py', 'r') as f:
    content = f.read()

# Fix ROAS bar chart - light to dark blue ascending
old_fig4 = """        fig4 = px.bar(cs, x='avg_roas', y='campaign', orientation='h',
                      color='avg_roas', color_continuous_scale=[[0,'#e0e7ff'],[1,'#4f46e5']])
        fig4.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=0,r=0,t=8,b=0), height=300,
            showlegend=False, coloraxis_showscale=False,
            font=dict(size=10, color='#0f172a'),
            xaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='ROAS',font=dict(color='#94a3b8'))),
            yaxis=dict(tickfont=dict(color='#0f172a',size=10), title=None)
        )
        fig4.update_traces(marker_line_width=0)
        st.plotly_chart(fig4, use_container_width=True)"""

new_fig4 = """        cs_sorted = cs.sort_values('avg_roas', ascending=True).reset_index(drop=True)
        n = len(cs_sorted)
        bar_colors = ['#dbeafe','#93c5fd','#60a5fa','#3b82f6','#2563eb','#1e3a8a'][:n]
        fig4 = go.Figure()
        for i, row in cs_sorted.iterrows():
            fig4.add_trace(go.Bar(
                x=[row['avg_roas']], y=[row['campaign']],
                orientation='h',
                marker_color=bar_colors[i % len(bar_colors)],
                marker_line_width=0,
                text=f"{row['avg_roas']:.0f}x",
                textposition='outside',
                textfont=dict(size=10, color='#334155', family='Inter'),
                name=row['campaign']
            ))
        fig4.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=40,t=20,b=10), height=300,
            showlegend=False,
            font=dict(size=10, color='#0f172a', family='Inter'),
            bargap=0.3,
            xaxis=dict(
                showgrid=True, gridcolor='#f1f5f9', zeroline=False,
                tickfont=dict(color='#94a3b8', size=10),
                title=dict(text='Return on Ad Spend (ROAS)', font=dict(color='#64748b', size=10)),
                showline=True, linecolor='#e2e8f0'
            ),
            yaxis=dict(
                tickfont=dict(color='#0f172a', size=10, family='Inter'),
                title=None, showgrid=False
            )
        )
        st.plotly_chart(fig4, use_container_width=True)"""

# Fix conversion scatter - monochrome blue by revenue rank
old_fig5 = """        fig5 = px.scatter(cs, x='avg_conv', y='total_rev', size='total_sent',
                          color='campaign', text='campaign',
                          color_discrete_sequence=['#6366f1','#22c55e','#f59e0b','#ef4444','#0ea5e9','#8b5cf6'])
        fig5.update_traces(textposition='top center', textfont=dict(size=8, color='#0f172a'))
        fig5.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=0,r=0,t=8,b=0), height=300,
            showlegend=False,
            font=dict(size=10, color='#0f172a'),
            xaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='Avg Conversion Rate (%)',font=dict(color='#94a3b8',size=10))),
            yaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='Total Revenue ($)',font=dict(color='#94a3b8',size=10)))
        )
        st.plotly_chart(fig5, use_container_width=True)"""

new_fig5 = """        cs_rev = cs.sort_values('total_rev', ascending=True).reset_index(drop=True)
        scatter_colors = ['#dbeafe','#93c5fd','#60a5fa','#3b82f6','#2563eb','#1e3a8a']
        fig5 = go.Figure()
        for i, row in cs_rev.iterrows():
            fig5.add_trace(go.Scatter(
                x=[row['avg_conv']], y=[row['total_rev']],
                mode='markers+text',
                marker=dict(size=22, color=scatter_colors[i % len(scatter_colors)],
                            line=dict(width=2, color='white'), opacity=0.92),
                text=[row['campaign']],
                textposition='top center',
                textfont=dict(size=9, color='#0f172a', family='Inter'),
                hovertemplate=f"<b>{row['campaign']}</b><br>Conversion: {row['avg_conv']:.1f}%<br>Revenue: ${row['total_rev']:,.0f}<br>Reach: {row['total_sent']:,}<extra></extra>",
                name=row['campaign']
            ))
        fig5.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=20,b=10), height=300,
            showlegend=False,
            font=dict(size=10, color='#0f172a', family='Inter'),
            xaxis=dict(
                showgrid=True, gridcolor='#f1f5f9', zeroline=False,
                tickfont=dict(color='#64748b', size=10),
                title=dict(text='Avg Conversion Rate (%)', font=dict(color='#64748b', size=10)),
                showline=True, linecolor='#e2e8f0'
            ),
            yaxis=dict(
                showgrid=True, gridcolor='#f1f5f9', zeroline=False,
                tickfont=dict(color='#64748b', size=10),
                title=dict(text='Total Revenue (USD)', font=dict(color='#64748b', size=10)),
                tickformat='$,.0f', showline=True, linecolor='#e2e8f0'
            ),
            hovermode='closest'
        )
        st.plotly_chart(fig5, use_container_width=True)"""

content = content.replace(old_fig4, new_fig4)
content = content.replace(old_fig5, new_fig5)

with open('app.py', 'w') as f:
    f.write(content)

c = open('app.py').read()
print("ROAS chart:", "OK" if 'cs_sorted' in c else "FAILED")
print("Scatter chart:", "OK" if 'cs_rev' in c else "FAILED")
