import os

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

# I need to replace everything after {% block 'body' %}{% endblock 'body' %} up to the closing </div> page wrapper or </body>
# wait, the simplest is to just inject {% include 'main/components/footer.html' %} right after {% endblock 'body' %}

# Find: {% block 'body' %}{% endblock 'body' %}
# and insert footer.
if "{% endblock 'body' %}" in content:
    content = content.replace("{% endblock 'body' %}", "{% endblock 'body' %}\n    {% include 'main/components/footer.html' %}")

with open(filepath, 'w') as f:
    f.write(content)

print("base.html footer patched.")
