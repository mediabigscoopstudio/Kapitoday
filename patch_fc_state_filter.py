import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    "recommended = Product.objects.prefetch_related('product_variant').exclude(id__in=cart_product_ids).order_by('?')[:3]",
    "recommended = Product.objects.prefetch_related('product_variant').filter(product_variant__isnull=False).distinct().exclude(id__in=cart_product_ids).order_by('?')[:3]"
)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched recommended query to require variants.")
