import re
filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/partials/fc_cart_items.html'
with open(filepath, 'r') as f:
    content = f.read()

# Remove the old recommended block
old_block = re.search(r"{% if recommended %}.*?{% endif %}", content, re.DOTALL)
if old_block:
    content = content.replace(old_block.group(0), "")

# Add the new squarish block
new_block = """
{% if recommended %}
<div style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
    <h6 style="font-weight:700; color:#3A2A1D; margin-bottom:15px; font-family:serif;">You might also like</h6>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        {% for rec in recommended %}
        <div style="background:#fff; border:1px solid #eee; border-radius:10px; overflow:hidden; position:relative; display:flex; flex-direction:column;">
            <div style="aspect-ratio: 1; width: 100%; background: #f9f9f9;">
                <img src="{% if rec.thumbnail %}{{ rec.thumbnail.url }}{% else %}{% static 'main/logos/LogoMain.webp' %}{% endif %}" style="width:100%; height:100%; object-fit:cover;" alt="{{ rec.name }}">
            </div>
            <div style="padding: 10px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="font-weight:600; font-size:0.85rem; color:#3A2A1D; line-height: 1.2; margin-bottom: 5px;">{{ rec.name|truncatechars:35 }}</div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
                    <div style="font-weight:700; color:#2a8b41; font-size:0.85rem;">₹{{ rec.product_variant.first.price|default:'---' }}</div>
                    <button onclick="fcAddRecommended('{{ rec.id }}')" style="background:#a67c52; color:#fff; border:none; width:28px; height:28px; border-radius:50%; font-weight:bold; cursor:pointer; display:flex; align-items:center; justify-content:center; transition: background 0.2s;" onmouseover="this.style.background='#8e6843'" onmouseout="this.style.background='#a67c52'">
                        <i class="bi bi-plus-lg" style="font-size:14px;"></i>
                    </button>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endif %}
"""

with open(filepath, 'w') as f:
    f.write(content + new_block)
print("Patched recommended grid.")
