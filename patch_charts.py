with open('app.py', 'r') as f:
    content = f.read()

# ── CHART 1: Volume by Payment Channel ────────────────────────────────────────
old_chart1 = """        ch = txn_df.groupby('channel')['transaction_amount'].sum().reset_index().sort_values('transaction_amount', ascending=False)
        fig1 = px.bar(ch, x='channel', y='transaction_amount',
                      color_discrete_sequence=['#6366f1','#818cf8','#a5b4fc','#c7d2fe','#e0e7ff'])
        fig1.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=0,r=0,t=8,b=0), height=260,
            showlegend=False,
            font=dict(size=11, color='#0f172a'),
            xaxis=dict(showgrid=False, tickfont=dict(color='#475569',size=11), title=None),
            yaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='Volume ($)',font=dict(color='#94a3b8',size=10)))
        )
        fig1.update_traces(marker_line_width=0)
        st.plotly_chart(fig1, use_container_width=True)"""

new_chart1 = """        ch = txn_df.groupby('channel')['transaction_amount'].sum().reset_index().sort_values('transaction_amount', ascending=False)
        ch['pct'] = (ch['transaction_amount'] / ch['transaction_amount'].sum() * 100).round(1)
        colors = ['#4f46e5','#6366f1','#818cf8','#a5b4fc','#c7d2fe']
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
            ))
        fig1.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=40,b=10), height=300,
            showlegend=False,
            font=dict(size=11, color='#0f172a', family='Inter'),
            bargap=0.35,
            xaxis=dict(
                showgrid=False, zeroline=False,
                tickfont=dict(color='#334155', size=11, family='Inter'),
                title=None,
                showline=True, linecolor='#e2e8f0'
            ),
            yaxis=dict(
                showgrid=True, gridcolor='#f1f5f9', gridwidth=1,
                tickfont=dict(color='#94a3b8', size=10),
                title=dict(text='Transaction Volume (USD)', font=dict(color='#64748b', size=10)),
                tickformat='$,.0f', zeroline=False,
                showline=False
            ),
        )
        st.plotly_chart(fig1, use_container_width=True)"""

# ── CHART 2: Monthly Revenue Trend ────────────────────────────────────────────
old_chart2 = """        st.markdown(\"\"\"<div class="card"><div class="card-head">
            <div><div class="card-head-title">Monthly Revenue Trend</div>
            <div class="card-head-sub">Transaction volume over time</div></div>
        </div></div>\"\"\", unsafe_allow_html=True)
        monthly = txn_df.copy()
        monthly['month'] = monthly['date'].dt.to_period('M').astype(str)
        md = monthly.groupby('month')['transaction_amount'].sum().reset_index()
        fig2 = px.area(md, x='month', y='transaction_amount', color_discrete_sequence=['#6366f1'])
        fig2.update_traces(fill='tozeroy', fillcolor='rgba(99,102,241,0.07)', line=dict(width=2.5, color='#6366f1'))
        fig2.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=0,r=0,t=8,b=0), height=240,
            font=dict(size=10, color='#0f172a'),
            xaxis=dict(showgrid=False, tickfont=dict(color='#94a3b8',size=9), tickangle=45, title=None),
            yaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=9), title=None)
        )
        st.plotly_chart(fig2, use_container_width=True)"""

new_chart2 = """        st.markdown(\"\"\"<div class="card"><div class="card-head">
            <div><div class="card-head-title">Monthly Revenue Trend</div>
            <div class="card-head-sub">Transaction volume over time</div></div>
        </div></div>\"\"\", unsafe_allow_html=True)
        monthly = txn_df.copy()
        monthly['month'] = monthly['date'].dt.to_period('M').astype(str)
        md = monthly.groupby('month')['transaction_amount'].sum().reset_index()
        avg_vol = md['transaction_amount'][:-1].mean()
        if len(md) > 2 and md['transaction_amount'].iloc[-1] < avg_vol * 0.8:
            md = md.iloc[:-1]
        max_idx = md['transaction_amount'].idxmax()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=md['month'], y=md['transaction_amount'],
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(99,102,241,0.08)',
            line=dict(width=2.5, color='#4f46e5', shape='spline'),
            marker=dict(size=5, color='#4f46e5', line=dict(width=2, color='white')),
            hovertemplate='<b>%{x}</b><br>Volume: $%{y:,.0f}<extra></extra>',
        ))
        fig2.add_annotation(
            x=md.loc[max_idx,'month'], y=md.loc[max_idx,'transaction_amount'],
            text=f"Peak: \${md.loc[max_idx,'transaction_amount']/1e6:.2f}M",
            showarrow=True, arrowhead=2, arrowcolor='#4f46e5',
            font=dict(size=9, color='#4f46e5', family='Inter'),
            bgcolor='#eff6ff', bordercolor='#c7d2fe', borderwidth=1, borderpad=4, ay=-36
        )
        fig2.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=30,b=10), height=260,
            font=dict(size=10, color='#0f172a', family='Inter'),
            xaxis=dict(
                showgrid=False, zeroline=False,
                tickfont=dict(color='#64748b', size=9),
                tickangle=30, title=None,
                showline=True, linecolor='#e2e8f0', nticks=8
            ),
            yaxis=dict(
                showgrid=True, gridcolor='#f1f5f9', gridwidth=1,
                tickfont=dict(color='#94a3b8', size=9),
                title=dict(text='Volume (USD)', font=dict(color='#64748b', size=9)),
                tickformat='\$,.0f', zeroline=False
            ),
            hovermode='x unified', showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)"""

# ── CHART 3: Customer Segment Risk Matrix ─────────────────────────────────────
old_chart3 = """        seg = cust_df.groupby('segment').agg(count=('customer_id','count'), avg_spend=('total_spend','mean'), churn=('churn_risk','mean')).reset_index()
        fig3 = px.scatter(seg, x='avg_spend', y='churn', size='count', color='segment', text='segment',
                          color_discrete_sequence=['#6366f1','#22c55e','#f59e0b','#ef4444','#0ea5e9'])
        fig3.update_traces(textposition='top center', textfont=dict(size=10, color='#0f172a'))
        fig3.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=0,r=0,t=8,b=0), height=260,
            showlegend=False,
            font=dict(size=10, color='#0f172a'),
            xaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='Avg Spend ($)',font=dict(color='#94a3b8',size=10))),
            yaxis=dict(showgrid=True, gridcolor='#f8fafc', tickfont=dict(color='#94a3b8',size=10), title=dict(text='Churn Risk',font=dict(color='#94a3b8',size=10)))
        )
        st.plotly_chart(fig3, use_container_width=True)"""

new_chart3 = """        seg = cust_df.groupby('segment').agg(count=('customer_id','count'), avg_spend=('total_spend','mean'), churn=('churn_risk','mean')).reset_index()
        palette = {'Student':'#6366f1','Standard':'#ef4444','Business':'#f59e0b','Premium':'#f97316','Enterprise':'#22c55e'}
        fig3 = go.Figure()
        mid_spend = seg['avg_spend'].mean()
        mid_churn = seg['churn'].mean()
        fig3.add_shape(type='rect', x0=seg['avg_spend'].min()*0.85, x1=mid_spend,
            y0=mid_churn, y1=seg['churn'].max()*1.005,
            fillcolor='rgba(239,68,68,0.05)', line_width=0)
        fig3.add_shape(type='rect', x0=mid_spend, x1=seg['avg_spend'].max()*1.15,
            y0=mid_churn, y1=seg['churn'].max()*1.005,
            fillcolor='rgba(249,115,22,0.05)', line_width=0)
        fig3.add_shape(type='rect', x0=seg['avg_spend'].min()*0.85, x1=mid_spend,
            y0=seg['churn'].min()*0.995, y1=mid_churn,
            fillcolor='rgba(99,102,241,0.05)', line_width=0)
        fig3.add_shape(type='rect', x0=mid_spend, x1=seg['avg_spend'].max()*1.15,
            y0=seg['churn'].min()*0.995, y1=mid_churn,
            fillcolor='rgba(34,197,94,0.05)', line_width=0)
        fig3.add_annotation(x=seg['avg_spend'].min()*1.1, y=seg['churn'].max()*1.004,
            text='High Risk / Low Spend', font=dict(size=8, color='#ef4444'), showarrow=False, xanchor='left')
        fig3.add_annotation(x=seg['avg_spend'].max()*1.1, y=seg['churn'].max()*1.004,
            text='High Risk / High Spend', font=dict(size=8, color='#f97316'), showarrow=False, xanchor='right')
        fig3.add_annotation(x=seg['avg_spend'].min()*1.1, y=seg['churn'].min()*0.996,
            text='Low Risk / Low Spend', font=dict(size=8, color='#6366f1'), showarrow=False, xanchor='left')
        fig3.add_annotation(x=seg['avg_spend'].max()*1.1, y=seg['churn'].min()*0.996,
            text='Low Risk / High Spend', font=dict(size=8, color='#16a34a'), showarrow=False, xanchor='right')
        for _, row in seg.iterrows():
            col = palette.get(row['segment'], '#6366f1')
            fig3.add_trace(go.Scatter(
                x=[row['avg_spend']], y=[row['churn']],
                mode='markers+text',
                marker=dict(size=row['count']/120, color=col,
                            line=dict(width=2.5, color='white'), opacity=0.92),
                text=[f"<b>{row['segment']}</b>"],
                textposition='top center',
                textfont=dict(size=10, color='#0f172a', family='Inter'),
                hovertemplate=f"<b>{row['segment']}</b><br>Avg Spend: \${row['avg_spend']:,.0f}<br>Churn Risk: {row['churn']:.4f}<br>Customers: {row['count']:,}<extra></extra>",
                name=row['segment']
            ))
        fig3.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(l=10,r=10,t=30,b=10), height=280,
            showlegend=False,
            font=dict(size=10, color='#0f172a', family='Inter'),
            xaxis=dict(
                showgrid=True, gridcolor='#f1f5f9', zeroline=False,
                tickfont=dict(color='#64748b', size=10),
                title=dict(text='Average Customer Spend (USD)', font=dict(color='#64748b', size=10)),
                tickformat='\$,.0f', showline=True, linecolor='#e2e8f0'
            ),
            yaxis=dict(
                showgrid=True, gridcolor='#f1f5f9', zeroline=False,
                tickfont=dict(color='#64748b', size=10),
                title=dict(text='Churn Risk Score', font=dict(color='#64748b', size=10)),
                tickformat='.3f', showline=True, linecolor='#e2e8f0'
            ),
            hovermode='closest'
        )
        st.plotly_chart(fig3, use_container_width=True)"""

content = content.replace(old_chart1, new_chart1)
content = content.replace(old_chart2, new_chart2)
content = content.replace(old_chart3, new_chart3)

with open('app.py', 'w') as f:
    f.write(content)

c = open('app.py').read()
print("Chart 1:", "OK" if '$,.0f' in c and 'Transaction Volume (USD)' in c else "FAILED")
print("Chart 2:", "OK" if 'avg_vol' in c else "FAILED")
print("Chart 3:", "OK" if 'High Risk / Low Spend' in c else "FAILED")
