filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    '<h5 style="margin: 0; font-family: serif; font-size: 1.2rem;">Kapi Today Checkout</h5>',
    '<h5 style="margin: 0; font-family: serif; font-size: 1.2rem; color: #fdfaf4;">Kapi Today Checkout</h5>'
)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched checkout title color.")
