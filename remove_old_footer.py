import os
import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

# Use regex to remove <footer class="footer-kapi"> ... </footer>
pattern = r'<footer class="footer-kapi">.*?</footer>'
new_content = re.sub(pattern, '', content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(new_content)

print("Old footer removed.")
