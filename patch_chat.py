import re

with open('app.py', 'r') as f:
    content = f.read()

# 1. Replace chat CSS
old_css = '''.chat-body {
    padding: 24px 28px;
    min-height: 320px;
    background: #fafbfc;
    display: flex; flex-direction: column; gap: 16px;
}
.msg-u { display: flex; justify-content: flex-end; }
.msg-a { display: flex; align-items: flex-start; gap: 10px; }
.msg-avatar {
    width: 32px; height: 32px; border-radius: 10px;
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 13px; font-weight: 700;
    flex-shrink: 0;
}
.bub-u {
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    color: white; padding: 12px 18px;
    border-radius: 20px 20px 6px 20px;
    font-size: 0.85rem; line-height: 1.55; max-width: 68%;
    box-shadow: 0 4px 14px rgba(79,70,229,0.25);
}
.bub-a {
    background: white; border: 1.5px solid #e2e8f0;
    color: #0f172a; padding: 12px 18px;
    border-radius: 20px 20px 20px 6px;
    font-size: 0.85rem; line-height: 1.65; max-width: 72%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}'''

new_css = '''.chat-body {
    padding: 28px 28px 20px 28px;
    min-height: 300px;
    background: #f8fafc;
    display: flex; flex-direction: column; gap: 20px;
}
.msg-u { display: flex; justify-content: flex-end; }
.msg-a { display: flex; align-items: flex-start; gap: 12px; }
.msg-avatar {
    width: 34px; height: 34px; border-radius: 10px;
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 13px; font-weight: 700;
    flex-shrink: 0; margin-top: 2px;
}
.bub-u {
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    color: white; padding: 14px 20px;
    border-radius: 22px 22px 6px 22px;
    font-size: 0.87rem; line-height: 1.6; max-width: 65%;
    box-shadow: 0 4px 18px rgba(79,70,229,0.28);
    letter-spacing: -0.1px;
}
.bub-a {
    background: white; border: 1.5px solid #e8ecf2;
    color: #1e293b; padding: 14px 20px;
    border-radius: 6px 22px 22px 22px;
    font-size: 0.87rem; line-height: 1.75; max-width: 72%;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    letter-spacing: -0.1px;
}'''

content = content.replace(old_css, new_css)

# 2. Replace the tab2 chat rendering section
old_tab2_render = '''        st.markdown("""
        <div class="chat-wrap">
            <div class="chat-head">
                <div class="chat-head-avatar">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
                        <rect x="3" y="3" width="7" height="7" rx="1.5" fill="white" opacity="0.8"/>
                        <rect x="14" y="3" width="7" height="7" rx="1.5" fill="white" opacity="0.5"/>
                        <rect x="3" y="14" width="7" height="7" rx="1.5" fill="white" opacity="0.5"/>
                        <rect x="14" y="14" width="7" height="7" rx="1.5" fill="white" opacity="0.8"/>
                    </svg>
                </div>
                <div>
                    <div class="chat-head-name">NexPay AI Agent</div>
                    <div class="chat-head-status">
                        <span class="chat-head-dot"></span>
                        Online, analyzing 100K transactions
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(\'<div class="chat-body">\', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg[\'role\'] == \'user\':
                st.markdown(f\'<div class="msg-u"><div class="bub-u">{msg["content"]}</div></div>\', unsafe_allow_html=True)
            else:
                st.markdown(f\'<div class="msg-a"><div class="msg-avatar">N</div><div class="bub-a">{msg["content"]}</div></div>\', unsafe_allow_html=True)
        st.markdown(\'</div>\', unsafe_allow_html=True)'''

new_tab2_render = '''        msgs_html = ""
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                msgs_html += f\'<div class="msg-u"><div class="bub-u">{msg["content"]}</div></div>\'
            else:
                msgs_html += f\'<div class="msg-a"><div class="msg-avatar">N</div><div class="bub-a">{msg["content"]}</div></div>\'

        st.markdown(f"""
        <div class="chat-wrap">
            <div class="chat-head">
                <div class="chat-head-avatar">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
                        <rect x="3" y="3" width="7" height="7" rx="1.5" fill="white" opacity="0.8"/>
                        <rect x="14" y="3" width="7" height="7" rx="1.5" fill="white" opacity="0.5"/>
                        <rect x="3" y="14" width="7" height="7" rx="1.5" fill="white" opacity="0.5"/>
                        <rect x="14" y="14" width="7" height="7" rx="1.5" fill="white" opacity="0.8"/>
                    </svg>
                </div>
                <div>
                    <div class="chat-head-name">NexPay AI Agent</div>
                    <div class="chat-head-status">
                        <span class="chat-head-dot"></span>
                        Online, analyzing 100K transactions
                    </div>
                </div>
            </div>
            <div class="chat-body">
                {msgs_html}
            </div>
        </div>
        """, unsafe_allow_html=True)'''

content = content.replace(old_tab2_render, new_tab2_render)

with open('app.py', 'w') as f:
    f.write(content)

print("Done! Check if both replacements worked.")
