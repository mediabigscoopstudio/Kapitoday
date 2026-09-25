filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/partials/fc_cart_items.html'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("rec.product_variant.all.0.price", "rec.computed_price")
content = content.replace("rec.product_variant.all.0.id", "rec.computed_variant_id")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched computed price in HTML.")
