import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("item.variant.title", "item.variant.name")

with open(filepath, 'w') as f:
    f.write(content)

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/partials/fc_cart_items.html'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("item.variant.title", "item.variant.name")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched variant title to name.")
