from django.conf import settings
from dash.models import Cart, CartItem, Customers

def cart_processor(request):
    cart_items = []
    cart_total = 0
    cart_count = 0
    
    if not request.session.session_key:
        request.session.create()
    
    cart = None
    if request.user.is_authenticated:
        try:
            customer = Customers.objects.get(user=request.user)
            cart, _ = Cart.objects.get_or_create(customer=customer)
        except Customers.DoesNotExist:
            pass
            
    if not cart:
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)

    if cart:
        cart_items = cart.cart_items.all().select_related('product', 'variant')
        cart_total = sum((item.variant.price if item.variant else 0) * item.quantity for item in cart_items)
        cart_count = sum(item.quantity for item in cart_items)
        
    return {
        'global_cart_items': cart_items,
        'global_cart_total': cart_total,
        'global_cart_count': cart_count,
    }

def google_client_id(request):
    return {
        'GOOGLE_CLIENT_ID': getattr(settings, 'GOOGLE_CLIENT_ID', '')
    }

from dash.models import Category, Product
def nav_categories_processor(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    
    # Exclude Accessories to get coffee categories only
    coffee_products = Product.objects.exclude(category__title__icontains='Accessories').order_by('-id')[:4]
    
    # Get Accessories
    accessories = Product.objects.filter(category__title__icontains='Accessories')[:4]
    
    # Get Featured Product
    featured_product = Product.objects.filter(name__icontains='Chikmagalur Medium Roast').first()
    
    return {
        'nav_categories': categories,
        'nav_coffee_products': coffee_products,
        'nav_accessories': accessories,
        'nav_featured_product': featured_product,
    }
