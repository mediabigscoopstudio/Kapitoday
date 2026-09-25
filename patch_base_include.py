import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    "{% include 'main/partials/fc_cart_items.html' %}",
    "{% include 'main/partials/fc_cart_items.html' with cart_items=global_cart_items %}"
)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched base.html include.")
