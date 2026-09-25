filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/partials/fc_cart_items.html'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    """<button onclick="updateCartItem('{{ item.id }}', 'remove')" style="background:none;border:none;color:#d32f2f;font-size:0.75rem;cursor:pointer;padding:0;">Remove</button>""",
    """<button onclick="updateCartItem('{{ item.id }}', 'remove')" style="background:none;border:none;color:#999;font-size:1.1rem;cursor:pointer;padding:0; transition: color 0.2s;" onmouseover="this.style.color='#d32f2f'" onmouseout="this.style.color='#999'" title="Remove Item"><i class="bi bi-trash3"></i></button>"""
)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched remove button.")
