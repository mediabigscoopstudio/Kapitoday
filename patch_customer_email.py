filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("customer.email or request.user.email", "request.user.email")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched customer.email error.")
