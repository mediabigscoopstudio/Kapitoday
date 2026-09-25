import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

old_line = "recommended = Product.objects.filter(status='Enabled').exclude(id__in=cart_product_ids).order_by('?')[:3]"
new_line = "recommended = Product.objects.exclude(id__in=cart_product_ids).order_by('?')[:3]"

content = content.replace(old_line, new_line)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched Product query.")
