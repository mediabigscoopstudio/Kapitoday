import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

target = """    # Render the cart items HTML so we don't have to build it in JS
    cart_html = render_to_string('main/partials/fc_cart_items.html', {'cart_items': cart_items}, request=request)"""

addition = """    # Get up to 3 recommended products (random or latest)
    from dash.models import Product
    cart_product_ids = [item.product.id for item in cart_items]
    recommended = Product.objects.filter(status='Enabled').exclude(id__in=cart_product_ids).order_by('?')[:3]
    
    # Render the cart items HTML so we don't have to build it in JS
    cart_html = render_to_string('main/partials/fc_cart_items.html', {
        'cart_items': cart_items,
        'recommended': recommended
    }, request=request)"""

content = content.replace(target, addition)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched fc_get_state with recommended products.")
