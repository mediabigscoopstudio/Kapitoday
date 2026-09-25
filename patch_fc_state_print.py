import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """        r.computed_variant_id = v.id if v else ''"""

new_code = """        r.computed_variant_id = v.id if v else ''
        print(f"Product: {r.name}, Variant: {v}, Price: {r.computed_price}")"""

content = content.replace(old_code, new_code)

with open(filepath, 'w') as f:
    f.write(content)
