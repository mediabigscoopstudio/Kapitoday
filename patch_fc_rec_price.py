import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/partials/fc_cart_items.html'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("₹{{ rec.price }}", "₹{{ rec.product_variant.first.price|default:'---' }}")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched recommended product price.")
