import os
filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/checkout.html'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("{% block content %}", "{% block 'body' %}")
content = content.replace("{% endblock %}", "{% endblock 'body' %}")
content = content.replace("{% endblock content %}", "{% endblock 'body' %}")

with open(filepath, 'w') as f:
    f.write(content)
print("Fixed block names in checkout.html")
