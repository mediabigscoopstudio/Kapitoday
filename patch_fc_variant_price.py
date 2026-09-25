import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/partials/fc_cart_items.html'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("rec.product_variant.first.price", "rec.product_variant.all.0.price")
content = content.replace("rec.product_variant.first.id", "rec.product_variant.all.0.id")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched template variant access.")
