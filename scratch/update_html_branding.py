with open('static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace user-facing title and branding
html = html.replace('<title>Swiggy Support Desk AI — Grounded Knowledge Assistant</title>', '<title>Siddarth Swiggy Support Desk AI — Grounded Knowledge Assistant</title>')
html = html.replace('<span class="font-extrabold text-xl tracking-tight text-slate-900">SWIGGY</span>', '<span class="font-extrabold text-xl tracking-tight text-slate-900">SIDDARTH SWIGGY</span>')
html = html.replace('Welcome to Swiggy Support Desk AI 👋', 'Welcome to Siddarth Swiggy Support Desk AI 👋')
html = html.replace('Swiggy Support Desk AI Knowledge Assistant • Synthetic Academic Scenario', 'Siddarth Swiggy Support Desk AI Knowledge Assistant • Synthetic Academic Scenario')
html = html.replace('Swiggy Support Desk AI Server', 'Siddarth Swiggy Support Desk AI Server')

with open('static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("static/index.html updated successfully!")
