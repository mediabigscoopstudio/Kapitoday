import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """        print(f"Product: {r.name}, Variant: {v}, Price: {r.computed_price}")"""

new_code = """        with open('/tmp/kapi_debug.txt', 'a') as debug_f:
            debug_f.write(f"Product: {r.name}, Variant: {v}, Price: {r.computed_price}\\n")"""

content = content.replace(old_code, new_code)

with open(filepath, 'w') as f:
    f.write(content)
