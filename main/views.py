
import json
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Prefetch, F

# Import the CMS models from the dash app
from dash.models import ArticleCategory, Author, Article, ArticleFAQ, ArticleHowTo, Product, Variant, Cart, CartItem, Customers, Offer, Order, OrderItem, Category, SubCategory


def index(request):
    from dash.models import Product
    bestseller_names = [
        'Kapi Today Araku Valley Medium Roast',
        'Kapi Today Chikmagalur Medium Roast',
        'Kapi Today South Indian Coffee Filter',
        'Kapi Today Wayanad Dark Roast'
    ]
    bestseller_products = []
    for name in bestseller_names:
        prod = Product.objects.filter(name__icontains=name.replace('Kapi Today ', '')).first()
        if prod:
            bestseller_products.append(prod)
    
    return render(request, 'main/index.html', {'bestseller_products': bestseller_products})

def about(request):
    return render(request, 'main/about.html')

def learn(request):
    return render(request, 'main/learn.html')

def content(request, category_slug=None):
    """
    Content listing page. Optionally filtered by category_slug.
    """
    categories = ArticleCategory.objects.filter(status='Enabled').order_by('display_order', 'title')
    articles_qs = Article.objects.filter(status='Enabled').select_related('author', 'category').order_by('-created_at')
    
    current_category = None
    if category_slug:
        current_category = get_object_or_404(ArticleCategory, slug=category_slug, status='Enabled')
        articles_qs = articles_qs.filter(category=current_category)

    # Get featured article (if not filtered by category, pick the latest one)
    featured_article = None
    if not current_category and articles_qs.exists():
        featured_article = articles_qs.first()
        # Exclude the featured article from the main list
        articles_qs = articles_qs.exclude(id=featured_article.id)

    # Pagination
    paginator = Paginator(articles_qs, 9) # 9 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Popular articles for sidebar (simple simulation by views)
    popular_articles = Article.objects.filter(status='Enabled').select_related('category').order_by('-views')[:4]

    context = {
        'categories': categories,
        'current_category': current_category,
        'page_obj': page_obj,
        'featured_article': featured_article,
        'popular_articles': popular_articles,
    }
    return render(request, 'main/content.html', context)

def article_detail(request, category_slug, article_slug):
    """
    Article detail page. Resolves by category slug and article slug.
    """
    # Ensure both category and article exist, and the article belongs to the category.
    # We prefetch faqs and howto_steps to avoid N+1 queries.
    article = get_object_or_404(
        Article.objects.select_related('author', 'category').prefetch_related('faqs', 'howto_steps'),
        slug=article_slug,
        category__slug=category_slug,
        status='Enabled'
    )
    
    # Increment views
    Article.objects.filter(id=article.id).update(views=F('views') + 1)
    
    # Related articles (same category, excluding current)
    related_articles = Article.objects.filter(
        category=article.category, 
        status='Enabled'
    ).exclude(id=article.id).select_related('author', 'category').order_by('-created_at')[:3]

    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'main/article_detail.html', context)

# ==========================================
# SHOP & E-COMMERCE VIEWS
# ==========================================
from django.http import JsonResponse
from dash.models import Product, Variant, Cart, CartItem, Customers

def _get_or_create_cart(request):
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
    
    return cart

def shop(request, category_slug=None):
    if category_slug:
        products = Product.objects.filter(category__slug=category_slug).prefetch_related('product_variant').order_by('-created_at')
    else:
        products = Product.objects.all().prefetch_related('product_variant').order_by('-created_at')
    
    # Let's also attach the cart context so the drawer works
    cart = _get_or_create_cart(request)
    cart_items = cart.cart_items.all().select_related('product', 'variant')
    cart_total = sum((item.variant.price if item.variant else 0) * item.quantity for item in cart_items)
    
    active_category = None
    if category_slug:
        from dash.models import Category
        active_category = Category.objects.filter(slug=category_slug).first()

    context = {
        'products': products,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': sum(item.quantity for item in cart_items),
        'active_category': active_category
    }
    return render(request, 'main/shop.html', context)

def product_detail(request, category_slug, subcategory_slug, product_slug):
    qs = Product.objects.prefetch_related('product_images', 'product_variant', 'product_highlight', 'product_content')
    if subcategory_slug == 'all':
        product = get_object_or_404(qs, slug=product_slug, category__slug=category_slug, sub_category__isnull=True)
    else:
        product = get_object_or_404(qs, slug=product_slug, category__slug=category_slug, sub_category__slug=subcategory_slug)
    
    cart = _get_or_create_cart(request)
    cart_items = cart.cart_items.all().select_related('product', 'variant')
    cart_total = sum((item.variant.price if item.variant else 0) * item.quantity for item in cart_items)
    
    context = {
        'product': product,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': sum(item.quantity for item in cart_items)
    }
    return render(request, 'main/product_detail.html', context)

def add_to_cart(request):
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

@csrf_exempt
def google_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('credential')
            
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                settings.GOOGLE_CLIENT_ID
            )
            
            # Extract user info
            email = idinfo.get('email')
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            
            if not email:
                return JsonResponse({'success': False, 'error': 'No email provided by Google.'})
            
            # Create or get user
            user, created = User.objects.get_or_create(username=email, defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            })
            
            # Ensure Customer object exists
            from dash.models import Customers, Cart, CartItem
            customer, _ = Customers.objects.get_or_create(user=user)
            
            # Transfer session cart if exists
            session_key = request.session.session_key
            if session_key:
                session_cart = Cart.objects.filter(session_key=session_key).first()
                if session_cart:
                    customer_cart = Cart.objects.filter(customer=customer).first()
                    if customer_cart and customer_cart != session_cart:
                        # Merge session cart items into customer cart
                        for item in session_cart.cart_items.all():
                            existing_item = customer_cart.cart_items.filter(product=item.product, variant=item.variant).first()
                            if existing_item:
                                existing_item.quantity += item.quantity
                                existing_item.save()
                            else:
                                item.cart = customer_cart
                                item.save()
                        session_cart.delete()
                    else:
                        session_cart.customer = customer
                        session_cart.save()
            
            # Send welcome email if created
            if created:
                try:
                    from django.core.mail import EmailMultiAlternatives
                    from django.template.loader import render_to_string
                    
                    base_url = request.build_absolute_uri('/')[:-1]
                    html_content = render_to_string('emails/welcome.html', {
                        'first_name': first_name,
                        'base_url': base_url
                    })
                    text_content = f'Hi {first_name},\n\nThank you for joining Kapi Today. Explore our premium South Indian filter coffees and estate single origins!\n\nCheers,\nThe Kapi Today Team'
                    
                    msg = EmailMultiAlternatives(
                        'Welcome to Kapi Today!',
                        text_content,
                        settings.DEFAULT_FROM_EMAIL,
                        [email]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send(fail_silently=False)
                except Exception as e:
                    print("Could not send email:", e)
            
            # Log the user in
            login(request, user)
            
            return JsonResponse({'success': True, 'first_name': first_name, 'created': created})
            
        except ValueError:
            # Invalid token
            return JsonResponse({'success': False, 'error': 'Invalid token'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request'})

from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

def custom_logout(request):
    auth_logout(request)
    return redirect('/')


from django.views.decorators.http import require_POST
from dash.models import Subscriber
import json

@require_POST
def subscribe_newsletter(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        if not email:
            return JsonResponse({'success': False, 'error': 'Email is required'})
            
        sub, created = Subscriber.objects.get_or_create(email=email)
        
        if created:
            try:
                from django.core.mail import EmailMultiAlternatives
                from django.template.loader import render_to_string
                base_url = request.build_absolute_uri('/')[:-1]
                html_content = render_to_string('emails/newsletter.html', {'base_url': base_url})
                text_content = "Thank you for subscribing to our newsletter! You're now officially part of the Kapi Culture.\n\nGet ready for early access to our exclusive product releases, seasonal estate blends, expert brewing tips, and stories straight from the coffee hills of South India."
                
                msg = EmailMultiAlternatives(
                    'Welcome to the Kapi Culture!',
                    text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=False)
            except Exception as e:
                print("Newsletter email failed:", e)
                
        return JsonResponse({'success': True, 'message': 'Successfully subscribed!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import razorpay

def get_razorpay_client():
    if not getattr(settings, 'RAZORPAY_API_KEY', None) or not getattr(settings, 'RAZORPAY_KEY_SECRET', None):
        return None
    return razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_KEY_SECRET))

from dash.models import Offer, Order
from django.utils import timezone

def checkout(request):
    return redirect('/?open_checkout=true')

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = request.POST
        # data will contain razorpay_payment_id, razorpay_order_id, razorpay_signature, plus our custom form fields
        client = get_razorpay_client()
        if client:
            try:
                # verify the signature
                client.utility.verify_payment_signature({
                    'razorpay_order_id': data.get('razorpay_order_id'),
                    'razorpay_payment_id': data.get('razorpay_payment_id'),
                    'razorpay_signature': data.get('razorpay_signature')
                })
                
                # Payment successful, create Order
                customer = Customers.objects.get(user=request.user)
                cart = Cart.objects.get(customer=customer)
                
                applied_coupon = request.session.get('applied_coupon', '')
                discount_amt = request.session.get('discount_amt', 0)
                
                order = Order.objects.create(
                    customer=customer,
                    coupon_code=applied_coupon,
                    discount=discount_amt,
                    email=customer.email or request.user.email,
                    phone=customer.phone_number or '',
                    full_name=data.get('full_name', 'Customer'),
                    address_line_1=data.get('address_line_1', ''),
                    address_line_2=data.get('address_line_2', ''),
                    city=data.get('city', ''),
                    state=data.get('state', ''),
                    pincode=data.get('pincode', ''),
                    total=data.get('total_amount', 0),
                    payment_method='razorpay',
                    razorpay_order_id=data.get('razorpay_order_id'),
                    razorpay_payment_id=data.get('razorpay_payment_id'),
                    razorpay_signature=data.get('razorpay_signature'),
                    payment_status='paid',
                    status='processing'
                )
                
                # Empty cart
                cart.cart_items.all().delete()
                if 'applied_coupon' in request.session:
                    del request.session['applied_coupon']
                if 'discount_amt' in request.session:
                    del request.session['discount_amt']
                
                # Send confirmation email
                try:
                    from django.core.mail import EmailMultiAlternatives
                    from django.template.loader import render_to_string
                    base_url = request.build_absolute_uri('/')[:-1]
                    html_content = render_to_string('emails/order_confirmation.html', {'order': order, 'base_url': base_url})
                    msg = EmailMultiAlternatives('Order Confirmation - Kapi Today', 'Your order is confirmed!', settings.DEFAULT_FROM_EMAIL, [order.email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send(fail_silently=False)
                    # Send tracking email immediately as requested
                    track_html = render_to_string('emails/track_order.html', {'order': order, 'base_url': base_url})
                    msg2 = EmailMultiAlternatives('Track Your Kapi Today Order', 'Track your coffee order!', settings.DEFAULT_FROM_EMAIL, [order.email])
                    msg2.attach_alternative(track_html, "text/html")
                    msg2.send(fail_silently=False)

                except Exception as e:
                    print("Order email failed:", e)

                return JsonResponse({'status': 'success', 'order_id': order.id})
            except Exception as e:
                print("Payment verification failed", e)
                return JsonResponse({'status': 'failure', 'error': str(e)})
    return JsonResponse({'status': 'invalid'})

# ==========================================
# FAST CHECKOUT APIS
# ==========================================
from django.template.loader import render_to_string

def _calculate_fc_totals(request, cart_items):
    subtotal = sum((item.variant.price if item.variant else 0) * item.quantity for item in cart_items)
    
    discount = 0
    applied_coupon = request.session.get('applied_coupon')
    
    if applied_coupon:
        now = timezone.now()
        offer = Offer.objects.filter(coupon_code__iexact=applied_coupon, status='Active', valid_from__lte=now, valid_to__gte=now).first()
        if offer:
            if offer.action_type == 'percentage_off':
                discount = (subtotal * offer.discount_value) / 100
                if offer.max_discount_cap and discount > offer.max_discount_cap:
                    discount = offer.max_discount_cap
            elif offer.action_type == 'flat_off':
                discount = offer.discount_value
                if discount > subtotal:
                    discount = subtotal
        else:
            del request.session['applied_coupon']
            applied_coupon = None

    total_after_discount = float(subtotal) - float(discount)
    shipping_charge = 0 if total_after_discount > 999 else 50
    
    auto_shipping_offer = Offer.objects.filter(trigger='automatic', action_type='free_shipping', status='Active').first()
    if auto_shipping_offer and total_after_discount >= float(auto_shipping_offer.min_order_amount or 0):
        shipping_charge = 0
        
    total = total_after_discount + shipping_charge
    request.session['discount_amt'] = float(discount)
    
    return float(subtotal), float(discount), applied_coupon, float(shipping_charge), float(total)


def fc_get_state(request):
    cart = _get_or_create_cart(request)
    cart_items = cart.cart_items.all().select_related('product', 'variant')
    
    subtotal, discount, applied_coupon, shipping_charge, total = _calculate_fc_totals(request, cart_items)
    
    is_authenticated = request.user.is_authenticated
    past_addresses = []
    
    if is_authenticated:
        customer, _ = Customers.objects.get_or_create(user=request.user)
        past_orders = Order.objects.filter(customer=customer).exclude(address_line_1='').order_by('-created_at')
        seen_addresses = set()
        for o in past_orders:
            addr_key = f"{o.address_line_1}-{o.pincode}".lower()
            if addr_key not in seen_addresses:
                seen_addresses.add(addr_key)
                past_addresses.append({
                    'full_name': o.full_name,
                    'address_line_1': o.address_line_1,
                    'address_line_2': o.address_line_2,
                    'city': o.city,
                    'state': o.state,
                    'pincode': o.pincode
                })
                if len(past_addresses) >= 5:
                    break
                    
    now = timezone.now()
    offers = Offer.objects.filter(status='Active', trigger='coupon', valid_to__gte=now).exclude(coupon_code__isnull=True).exclude(coupon_code='')
    available_offers = [{'code': o.coupon_code, 'desc': o.description} for o in offers]
    
    # Get up to 3 recommended products (random or latest)
    from dash.models import Product
    cart_product_ids = [item.product.id for item in cart_items]
    recommended_qs = Product.objects.prefetch_related('product_variant').filter(product_variant__isnull=False).distinct().exclude(id__in=cart_product_ids).order_by('?')[:3]
    recommended = list(recommended_qs)
    for r in recommended:
        variants = list(r.product_variant.all())
        v = variants[0] if variants else None
        r.computed_price = v.price if v else None
        r.computed_variant_id = v.id if v else ''

    
    # Render the cart items HTML so we don't have to build it in JS
    cart_html = render_to_string('main/partials/fc_cart_items.html', {
        'cart_items': cart_items,
        'recommended': recommended
    }, request=request)
    
    return JsonResponse({
        'success': True,
        'is_authenticated': is_authenticated,
        'cart_count': sum(i.quantity for i in cart_items),
        'cart_html': cart_html,
        'subtotal': subtotal,
        'discount': discount,
        'applied_coupon': applied_coupon,
        'shipping_charge': shipping_charge,
        'total': total,
        'past_addresses': past_addresses,
        'available_offers': available_offers
    })


@csrf_exempt
def fc_update_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action') # 'add', 'sub', 'remove'
        item_id = data.get('item_id')
        
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        if action == 'add':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'sub':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        elif action == 'remove':
            cart_item.delete()
            
        return fc_get_state(request)
    return JsonResponse({'success': False})


@csrf_exempt
def fc_apply_coupon(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code', '').strip()
        action = data.get('action', 'apply')
        
        if action == 'remove':
            if 'applied_coupon' in request.session:
                del request.session['applied_coupon']
            return fc_get_state(request)
            
        now = timezone.now()
        offer = Offer.objects.filter(coupon_code__iexact=code, status='Active', valid_from__lte=now, valid_to__gte=now).first()
        if offer:
            request.session['applied_coupon'] = offer.coupon_code
        else:
            return JsonResponse({'success': False, 'error': 'Invalid or expired coupon.'})
            
        return fc_get_state(request)
    return JsonResponse({'success': False})


@csrf_exempt
def fc_init_payment(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Not logged in'})
            
        cart = _get_or_create_cart(request)
        cart_items = cart.cart_items.all()
        if not cart_items:
            return JsonResponse({'success': False, 'error': 'Cart is empty'})
            
        subtotal, discount, applied_coupon, shipping_charge, total = _calculate_fc_totals(request, cart_items)
        amount = int(total * 100)
        
        client = get_razorpay_client()
        if client:
            try:
                razorpay_order = client.order.create(dict(amount=amount, currency="INR", payment_capture='1'))
                return JsonResponse({
                    'success': True,
                    'key': settings.RAZORPAY_API_KEY,
                    'amount': amount,
                    'order_id': razorpay_order['id'],
                    'total': total,
                })
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
                
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@csrf_exempt
def fc_verify_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        client = get_razorpay_client()
        if client:
            try:
                client.utility.verify_payment_signature({
                    'razorpay_order_id': data.get('razorpay_order_id'),
                    'razorpay_payment_id': data.get('razorpay_payment_id'),
                    'razorpay_signature': data.get('razorpay_signature')
                })
                
                customer = Customers.objects.get(user=request.user)
                cart = Cart.objects.get(customer=customer)
                
                applied_coupon = request.session.get('applied_coupon', '')
                discount_amt = request.session.get('discount_amt', 0)
                
                order = Order.objects.create(
                    customer=customer,
                    coupon_code=applied_coupon,
                    discount=discount_amt,
                    email=customer.email or request.user.email,
                    phone=customer.phone_number or '',
                    full_name=data.get('full_name', 'Customer'),
                    address_line_1=data.get('address_line_1', ''),
                    address_line_2=data.get('address_line_2', ''),
                    city=data.get('city', ''),
                    state=data.get('state', ''),
                    pincode=data.get('pincode', ''),
                    total=data.get('total_amount', 0),
                    payment_method='razorpay',
                    razorpay_order_id=data.get('razorpay_order_id'),
                    razorpay_payment_id=data.get('razorpay_payment_id'),
                    razorpay_signature=data.get('razorpay_signature'),
                    payment_status='paid',
                    status='pending'
                )
                
                for item in cart.cart_items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        variant=item.variant,
                        product_name=item.product.name,
                        variant_name=item.variant.title if item.variant else ''
                    )
                
                cart.cart_items.all().delete()
                if 'applied_coupon' in request.session:
                    del request.session['applied_coupon']
                if 'discount_amt' in request.session:
                    del request.session['discount_amt']
                
                # We could send email here if we want, ignoring for brevity of the API
                
                return JsonResponse({'success': True, 'order_db_id': order.id})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})
