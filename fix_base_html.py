import os
import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

# I want to remove the duplicate block 'body' and footer things.
# Let's find all occurrences of block 'body'
blocks = list(re.finditer(r'{% block \'body\' %}.*?{% endblock \'body\' %}', content, flags=re.DOTALL))
print(f"Found {len(blocks)} block 'body' elements.")

if len(blocks) > 1:
    # Remove the FIRST occurrence, which is likely the old messed up one
    content = content[:blocks[0].start()] + content[blocks[0].end():]
    print("Removed duplicate block 'body'.")

# I should also ensure there are no duplicated footers or weird leftover markup.
# Let's just output the current base.html structure to analyze it first.
