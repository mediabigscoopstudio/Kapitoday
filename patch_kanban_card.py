import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/dash/partials/kanban_card.html'
with open(filepath, 'r') as f:
    content = f.read()

# Replace \'order_detail\' with "order_detail"
content = content.replace(r"\'order_detail\'", '"order_detail"')

with open(filepath, 'w') as f:
    f.write(content)
print("Patched kanban_card.html")
