import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/partials/fc_cart_items.html'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("rec.computed_price|default:'---'", "rec.computed_price")

with open(filepath, 'w') as f:
    f.write(content)
print("Removed default filter.")
