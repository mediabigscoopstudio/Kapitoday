import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """    recommended = Product.objects.prefetch_related('product_variant').exclude(id__in=cart_product_ids).order_by('?')[:3]
    
    # Render the cart items HTML so we don't have to build it in JS"""

new_code = """    recommended = Product.objects.prefetch_related('product_variant').exclude(id__in=cart_product_ids).order_by('?')[:3]
    for r in recommended:
        v = r.product_variant.first()
        r.computed_price = v.price if v else None
        r.computed_variant_id = v.id if v else ''
    
    # Render the cart items HTML so we don't have to build it in JS"""

content = content.replace(old_code, new_code)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched computed price in views.py.")
