import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """                for item in cart.cart_items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        variant=item.variant,
                        product_name=item.product.name,
                        variant_name=item.variant.name if item.variant else ''
                    )"""

new_block = """                for item in cart.cart_items.all():
                    v = item.variant or item.product.product_variant.first()
                    price = v.price if v else 0
                    gst = v.gst if v else 0
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        variant=item.variant,
                        product_name=item.product.name,
                        variant_name=item.variant.name if item.variant else '',
                        price=price,
                        gst=gst,
                        quantity=item.quantity,
                        total=price * item.quantity
                    )"""

content = content.replace(old_block, new_block)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched OrderItem creation in fc_verify_payment.")
