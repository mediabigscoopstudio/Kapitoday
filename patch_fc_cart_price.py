filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/partials/fc_cart_items.html'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    "₹{% widthratio item.variant.price|default:item.product.price|default:0 1 item.quantity %}",
    "₹{% widthratio item.variant.price|default:item.product.product_variant.first.price|default:0 1 item.quantity %}"
)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched cart item price.")
