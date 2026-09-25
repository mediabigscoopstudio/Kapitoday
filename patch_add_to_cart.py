import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

old_add_to_cart = re.search(r"def add_to_cart\(request\):.*?(?=@csrf_exempt\ndef google_login)", content, re.DOTALL)

if old_add_to_cart:
    new_add_to_cart = """def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        variant_id = request.POST.get('variant_id')
        quantity = int(request.POST.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id)
        variant = get_object_or_404(Variant, id=variant_id) if variant_id else None
        
        cart = _get_or_create_cart(request)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': 0}
        )
        cart_item.quantity += quantity
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
            
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
            return fc_get_state(request)
            
        return redirect(request.META.get('HTTP_REFERER', '/shop/'))
    return redirect('/shop/')

"""
    content = content.replace(old_add_to_cart.group(0), new_add_to_cart)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched add_to_cart")
else:
    print("Could not find add_to_cart")
