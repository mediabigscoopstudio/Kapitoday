filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/partials/fc_cart_items.html'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    """<button onclick="fcAddRecommended('{{ rec.id }}')\"""",
    """<button onclick="fcAddRecommended('{{ rec.id }}', '{{ rec.product_variant.first.id|default:\"\" }}')\""""
)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched fcAddRecommended HTML args.")
