import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """    recommended = Product.objects.prefetch_related('product_variant').filter(product_variant__isnull=False).distinct().exclude(id__in=cart_product_ids).order_by('?')[:3]
    for r in recommended:
        variants = list(r.product_variant.all())"""

new_code = """    recommended_qs = Product.objects.prefetch_related('product_variant').filter(product_variant__isnull=False).distinct().exclude(id__in=cart_product_ids).order_by('?')[:3]
    recommended = list(recommended_qs)
    for r in recommended:
        variants = list(r.product_variant.all())"""

content = content.replace(old_code, new_code)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched recommended to be a list.")
