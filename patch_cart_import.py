import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

old_func = """def _get_or_create_cart(request):
    cart = None
    if request.user.is_authenticated:
        from dash.models import Customers, Cart
        customer, _ = Customers.objects.get_or_create(user=request.user)
        cart, _ = Cart.objects.get_or_create(customer=customer)
    
    if not cart:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    
    return cart"""

new_func = """def _get_or_create_cart(request):
    from dash.models import Customers, Cart
    cart = None
    if request.user.is_authenticated:
        customer, _ = Customers.objects.get_or_create(user=request.user)
        cart, _ = Cart.objects.get_or_create(customer=customer)
    
    if not cart:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    
    return cart"""

content = content.replace(old_func, new_func)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched _get_or_create_cart imports.")
