import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """    for r in recommended:
        v = r.product_variant.first()
        r.computed_price = v.price if v else None
        r.computed_variant_id = v.id if v else ''"""

new_code = """    for r in recommended:
        variants = list(r.product_variant.all())
        v = variants[0] if variants else None
        r.computed_price = v.price if v else None
        r.computed_variant_id = v.id if v else ''"""

content = content.replace(old_code, new_code)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched computed price evaluating list.")
