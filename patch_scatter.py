with open('app.py', 'r') as f:
    content = f.read()

old = "                marker=dict(size=row['count']/120, color=col,"
new = "                marker=dict(size=28, color=col,"

content = content.replace(old, new)

with open('app.py', 'w') as f:
    f.write(content)

print("OK" if "size=28" in open('app.py').read() else "FAILED")
