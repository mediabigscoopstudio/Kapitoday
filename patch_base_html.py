import os
import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

# The old base.html has the ticker bar, utility bar, and navbar.
# I will use regex to replace everything between <div class="page-wrapper"> and {% block 'body' %}

pattern = r'<div class="page-wrapper">.*?(?={% block \'body\' %})'
replacement = """<div class="page-wrapper">

    {% include 'main/components/announcement.html' %}
    {% include 'main/components/header.html' %}
    
"""

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(new_content)

print("base.html patched.")
