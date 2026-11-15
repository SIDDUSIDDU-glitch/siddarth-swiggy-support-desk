with open('README.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('# 🛡️ Swiggy Support Desk AI Knowledge Assistant', '# 🛡️ Siddarth Swiggy Support Desk AI Knowledge Assistant')
text = text.replace('swiggy-support-desk-ai', 'siddarth-swiggy-support-desk-ai')
text = text.replace('Swiggy Support Desk AI Server Running', 'Siddarth Swiggy Support Desk AI Server Running')
text = text.replace('Swiggy Support Desk AI Knowledge Assistant', 'Siddarth Swiggy Support Desk AI Knowledge Assistant')
text = text.replace('Swiggy brand styling', 'Siddarth Swiggy brand styling')
text = text.replace('Swiggy Support Desk AI', 'Siddarth Swiggy Support Desk AI')

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("README.md updated with Siddarth Swiggy branding!")
