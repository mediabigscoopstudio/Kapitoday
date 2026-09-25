filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/partials/fc_cart_items.html'
with open(filepath, 'r') as f:
    content = f.read()

addition = """
{% if recommended %}
<div style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
    <h6 style="font-weight:700; color:#3A2A1D; margin-bottom:15px; font-family:serif;">You might also like</h6>
    {% for rec in recommended %}
    <div style="display:flex; gap:15px; align-items:center; margin-bottom:15px; background:#fff; padding:10px; border-radius:8px; border:1px solid #eee;">
        <img src="{% if rec.thumbnail %}{{ rec.thumbnail.url }}{% else %}{% static 'main/logos/LogoMain.webp' %}{% endif %}" style="width:60px; height:60px; object-fit:cover; border-radius:6px;" alt="{{ rec.name }}">
        <div style="flex:1;">
            <div style="font-weight:600; font-size:0.9rem; color:#3A2A1D;">{{ rec.name }}</div>
            <div style="font-weight:700; color:#2a8b41; font-size:0.85rem;">₹{{ rec.price }}</div>
        </div>
        <button onclick="fcAddRecommended('{{ rec.id }}')" style="background:#a67c52; color:#fff; border:none; width:30px; height:30px; border-radius:50%; font-weight:bold; cursor:pointer;">+</button>
    </div>
    {% endfor %}
</div>
{% endif %}
"""

with open(filepath, 'w') as f:
    f.write(content + addition)
print("Added recommended products HTML.")
