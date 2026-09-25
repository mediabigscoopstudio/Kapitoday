
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
from dash.models import ArticleCategory, Author, Article, ArticleFAQ, ArticleHowTo

def index(request):
    return render(request, 'main/index.html')

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
    cart = None
    if request.user.is_authenticated:
        try:
            customer = Customers.objects.get(user=request.user)
            cart, _ = Cart.objects.get_or_create(customer=customer)
        except Customers.DoesNotExist:
            pass
    
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
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()
        elif cart_item.quantity <= 0:
            cart_item.delete()
            
        # AJAX Response handling
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json'
        if is_ajax:
            cart_items = cart.cart_items.all().select_related('product', 'variant')
            cart_total = sum((item.variant.price if item.variant else 0) * item.quantity for item in cart_items)
            cart_count = sum(item.quantity for item in cart_items)
            
            from django.template.loader import render_to_string
            context = {
                'global_cart_items': cart_items,
                'global_cart_total': cart_total,
                'global_cart_count': cart_count,
            }
            cart_html = render_to_string('main/partials/cart_drawer_items.html', context, request=request)
            
            return JsonResponse({
                'success': True,
                'cart_count': cart_count,
                'cart_total': cart_total,
                'cart_html': cart_html
            })
            
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
            
            # Send welcome email if created
            if created:
                try:
                    send_mail(
                        'Welcome to Kapi Today!',
                        f'Hi {first_name},\n\nThank you for joining Kapi Today. Explore our premium South Indian filter coffees and estate single origins!\n\nCheers,\nThe Kapi Today Team',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=True,
                    )
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
