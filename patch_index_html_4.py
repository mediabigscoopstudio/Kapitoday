import os

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/index.html'
with open(filepath, 'r') as f:
    content = f.read()

body_addition = """
    {% include 'main/components/testimonials.html' %}
    {% include 'main/components/community.html' %}
    {% include 'main/components/newsletter.html' %}
"""
content = content.replace("<!-- Stage 9-11 components will go here -->", body_addition)

with open(filepath, 'w') as f:
    f.write(content)

print("index.html patched with Stages 9-11.")
