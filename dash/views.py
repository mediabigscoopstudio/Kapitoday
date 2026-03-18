from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import Category,SubCategory,Product,ProductImage,Highlight,APlusContent,Variant,Offer,Customers,Support,Cart,CartItem,OrderItem,Order

def superadmin_required(user):
    return user.is_superuser 

def login_view(request):
    if request.method == 'POST':  
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'dash/signin.html')

def logout_view(request):
    logout(request)
    return redirect('/login_view')

from django.core.paginator import Paginator

@user_passes_test(superadmin_required, login_url=('/login_view'))
def index(request):
    all_orders = Order.objects.all().order_by('-created_at')
    paginator  = Paginator(all_orders, 20)
    page       = request.GET.get('page')
    orders     = paginator.get_page(page)
    return render(request,'dash/index.html', {'orders': orders})

# Category Management Section

@user_passes_test(superadmin_required, login_url=('/login_view'))
def category(request):
    categories = Category.objects.all().order_by('-id')
    return render(request,'dash/category/categories.html',{'categories':categories})

@user_passes_test(superadmin_required, login_url=('/login_view'))
def add_category(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')
        category_image = request.FILES.get('category_image')

        Category.objects.create(
            title=title,
            description=description,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            category_image=category_image
        )
        return redirect('/category')
    return render(request,'dash/category/add_category.html')

@user_passes_test(superadmin_required, login_url=('/login_view'))
def edit_category(request,id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.title = request.POST.get('title')
        category.description = request.POST.get('description')
        category.meta_title = request.POST.get('meta_title')
        category.meta_description = request.POST.get('meta_description')
        category.meta_keywords = request.POST.get('meta_keywords')
        if request.FILES.get('category_image'):
            category.category_image = request.FILES.get('category_image')
        category.save()
        return redirect('/category')
    return render(request,'dash/category/edit_category.html',{'data':category})

@user_passes_test(superadmin_required, login_url=('/login_view'))
def delete_category(request,id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('/category')

@user_passes_test(superadmin_required, login_url=('/login_view'))
def enable_category(request,id):
    category = get_object_or_404(Category, id=id)
    category.status = "Enabled"
    category.save()
    return redirect('/category')

@user_passes_test(superadmin_required, login_url=('/login_view'))
def disable_category(request,id):
    category = get_object_or_404(Category, id=id)
    category.status = "Disabled"
    category.save()
    return redirect('/category')

# Sub-Category Management Section
def add_sub_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('description')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')

        SubCategory.objects.create(
            category_id=category_id,
            title=title,
            description=description,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
        )
        return redirect('/sub_category_list')

    categories = Category.objects.filter(status='Enabled').order_by('-id')
    return render(request, 'dash/subcategory/add_sub_category.html', {'categories': categories})


def edit_sub_category(request, pk):
    sub_category = get_object_or_404(SubCategory, pk=pk)

    if request.method == 'POST':
        sub_category.category_id = request.POST.get('category')
        sub_category.title = request.POST.get('title')
        sub_category.description = request.POST.get('description')
        sub_category.meta_title = request.POST.get('meta_title')
        sub_category.meta_description = request.POST.get('meta_description')
        sub_category.meta_keywords = request.POST.get('meta_keywords')
        sub_category.save()
        return redirect('/sub_category_list')

    categories = Category.objects.filter(status='Enabled').order_by('-id')
    return render(request, 'dash/subcategory/edit_sub_category.html', {'data': sub_category, 'categories': categories})


def sub_category_list(request):
    sub_categories = SubCategory.objects.all().order_by('-id')
    return render(request, 'dash/subcategory/sub_category_list.html', {'sub_categories': sub_categories})


def enable_sub_category(request, pk):
    sub_category = get_object_or_404(SubCategory, pk=pk)
    sub_category.status = 'Enabled'
    sub_category.save()
    return redirect('/sub_category_list')


def disable_sub_category(request, pk):
    sub_category = get_object_or_404(SubCategory, pk=pk)
    sub_category.status = 'Disabled'
    sub_category.save()
    return redirect('/sub_category_list')


def delete_sub_category(request, pk):
    sub_category = get_object_or_404(SubCategory, pk=pk)
    sub_category.delete()
    return redirect('/sub_category_list')

#Product Management System 

@user_passes_test(superadmin_required, login_url=('/login_view'))
def product(request):
    products = Product.objects.all().order_by('-id')
    variants = Variant.objects.all()
    context = {
        'products':products,
        'variants':variants,
    }
    return render(request, 'dash/product/products.html', context)
 
@user_passes_test(superadmin_required, login_url=('/login_view'))
def add_product(request):
    if request.method == 'POST':

        # Core Info
        category_id      = request.POST.get('category')
        sub_category_id  = request.POST.get('sub_category') or None
        name             = request.POST.get('name')
        description      = request.POST.get('description')
        thumbnail        = request.FILES.get('thumbnail')

        # SEO
        meta_title       = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keywords    = request.POST.get('meta_keywords')
        meta_image       = request.FILES.get('meta_image')

        product = Product.objects.create(
            category_id=category_id,
            sub_category_id=sub_category_id,
            name=name,
            description=description,
            thumbnail=thumbnail,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            meta_image=meta_image,
        )

        # Product Images
        product_images     = request.FILES.getlist('product_images')
        product_image_alts = request.POST.getlist('product_image_alt')
        for i, image in enumerate(product_images):
            ProductImage.objects.create(
                product=product,
                image=image,
                alt_text=product_image_alts[i] if i < len(product_image_alts) else ''
            )

        # Variants
        variant_names      = request.POST.getlist('variant_name')
        variant_prices     = request.POST.getlist('variant_price')
        variant_gsts       = request.POST.getlist('variant_gst')
        variant_quantities = request.POST.getlist('variant_quantity')
        variant_statuses   = request.POST.getlist('variant_status')
        variant_images     = request.FILES.getlist('variant_image')
        variant_weights    = request.POST.getlist('variant_weight')
        variant_lengths    = request.POST.getlist('variant_length')
        variant_breadths   = request.POST.getlist('variant_breadth')
        variant_heights    = request.POST.getlist('variant_height')

        for i, vname in enumerate(variant_names):
            if vname.strip():
                Variant.objects.create(
                    product=product,
                    name=vname,
                    price=variant_prices[i]      if i < len(variant_prices)     else 0,
                    gst=variant_gsts[i]          if i < len(variant_gsts)       else 0,
                    quantity=variant_quantities[i] if i < len(variant_quantities) else 0,
                    status=variant_statuses[i]   if i < len(variant_statuses)   else 'Enabled',
                    image=variant_images[i]      if i < len(variant_images)     else None,
                    weight=variant_weights[i]    if i < len(variant_weights)    else 0.5,
                    length=variant_lengths[i]    if i < len(variant_lengths)    else 1.0,
                    breadth=variant_breadths[i]  if i < len(variant_breadths)   else 1.0,
                    height=variant_heights[i]    if i < len(variant_heights)    else 1.0,
                )

        # Highlights
        highlight_texts = request.POST.getlist('highlight_text')
        highlight_icons = request.FILES.getlist('highlight_icon')
        for i, htext in enumerate(highlight_texts):
            if htext.strip():
                Highlight.objects.create(
                    product=product,
                    text=htext,
                    icon=highlight_icons[i] if i < len(highlight_icons) else None,
                )

        # A+ Content
        aplus_images = request.FILES.getlist('aplus_image')
        aplus_alts   = request.POST.getlist('aplus_alt')
        for i, aimage in enumerate(aplus_images):
            APlusContent.objects.create(
                product=product,
                image=aimage,
                image_alt=aplus_alts[i] if i < len(aplus_alts) else ''
            )

        return redirect('/products')

    categories = Category.objects.filter(status='Enabled').order_by('-id')
    return render(request, 'dash/product/add_product.html', {'categories': categories})


@user_passes_test(superadmin_required, login_url=('/login_view'))
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.category_id      = request.POST.get('category')
        product.sub_category_id  = request.POST.get('sub_category') or None
        product.name             = request.POST.get('name')
        product.description      = request.POST.get('description')
        product.meta_title       = request.POST.get('meta_title')
        product.meta_description = request.POST.get('meta_description')
        product.meta_keywords    = request.POST.get('meta_keywords')
        if request.FILES.get('thumbnail'):
            product.thumbnail = request.FILES.get('thumbnail')
        if request.FILES.get('meta_image'):
            product.meta_image = request.FILES.get('meta_image')
        product.save()

        # New Product Images
        product_images     = request.FILES.getlist('product_images')
        product_image_alts = request.POST.getlist('product_image_alt')
        for i, image in enumerate(product_images):
            ProductImage.objects.create(
                product=product,
                image=image,
                alt_text=product_image_alts[i] if i < len(product_image_alts) else ''
            )

        # Update Existing Variants
        for v in product.product_variant.all():
            name     = request.POST.get(f'existing_variant_name_{v.id}')
            price    = request.POST.get(f'existing_variant_price_{v.id}')
            gst      = request.POST.get(f'existing_variant_gst_{v.id}')
            quantity = request.POST.get(f'existing_variant_quantity_{v.id}')
            status   = request.POST.get(f'existing_variant_status_{v.id}')
            weight   = request.POST.get(f'existing_variant_weight_{v.id}')
            length   = request.POST.get(f'existing_variant_length_{v.id}')
            breadth  = request.POST.get(f'existing_variant_breadth_{v.id}')
            height   = request.POST.get(f'existing_variant_height_{v.id}')
            if name:
                v.name     = name
                v.price    = price    or v.price
                v.gst      = gst      or v.gst
                v.quantity = quantity or v.quantity
                v.status   = status   or v.status
                v.weight   = weight   or v.weight
                v.length   = length   or v.length
                v.breadth  = breadth  or v.breadth
                v.height   = height   or v.height
            if request.FILES.get(f'existing_variant_image_{v.id}'):
                v.image = request.FILES.get(f'existing_variant_image_{v.id}')
            v.save()

        # New Variants
        variant_names      = request.POST.getlist('variant_name')
        variant_prices     = request.POST.getlist('variant_price')
        variant_gsts       = request.POST.getlist('variant_gst')
        variant_quantities = request.POST.getlist('variant_quantity')
        variant_statuses   = request.POST.getlist('variant_status')
        variant_images     = request.FILES.getlist('variant_image')
        variant_weights    = request.POST.getlist('variant_weight')
        variant_lengths    = request.POST.getlist('variant_length')
        variant_breadths   = request.POST.getlist('variant_breadth')
        variant_heights    = request.POST.getlist('variant_height')

        for i, vname in enumerate(variant_names):
            if vname.strip():
                Variant.objects.create(
                    product=product,
                    name=vname,
                    price=variant_prices[i]      if i < len(variant_prices)     else 0,
                    gst=variant_gsts[i]          if i < len(variant_gsts)       else 0,
                    quantity=variant_quantities[i] if i < len(variant_quantities) else 0,
                    status=variant_statuses[i]   if i < len(variant_statuses)   else 'Enabled',
                    image=variant_images[i]      if i < len(variant_images)     else None,
                    weight=variant_weights[i]    if i < len(variant_weights)    else 0.5,
                    length=variant_lengths[i]    if i < len(variant_lengths)    else 1.0,
                    breadth=variant_breadths[i]  if i < len(variant_breadths)   else 1.0,
                    height=variant_heights[i]    if i < len(variant_heights)    else 1.0,
                )

        # New Highlights
        highlight_texts = request.POST.getlist('highlight_text')
        highlight_icons = request.FILES.getlist('highlight_icon')
        for i, htext in enumerate(highlight_texts):
            if htext.strip():
                Highlight.objects.create(
                    product=product,
                    text=htext,
                    icon=highlight_icons[i] if i < len(highlight_icons) else None,
                )

        # New A+ Content
        aplus_images = request.FILES.getlist('aplus_image')
        aplus_alts   = request.POST.getlist('aplus_alt')
        for i, aimage in enumerate(aplus_images):
            APlusContent.objects.create(
                product=product,
                image=aimage,
                image_alt=aplus_alts[i] if i < len(aplus_alts) else ''
            )

        return redirect('/products')

    categories    = Category.objects.filter(status='Enabled').order_by('-id')
    subcategories = SubCategory.objects.filter(category=product.category, status='Enabled').order_by('-id')
    return render(request, 'dash/product/edit_product.html', {
        'data':           product,
        'categories':     categories,
        'subcategories':  subcategories,
        'variants':       product.product_variant.all(),
        'product_images': product.product_images.all(),
        'highlights':     product.product_highlight.all(),
        'aplus_contents': product.product_content.all(),
    }) 

 
from django.http import JsonResponse

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(
        category_id=category_id, status='Enabled'
    ).values('id', 'title')
    return JsonResponse(list(subcategories), safe=False)

#Offer Management System 

@user_passes_test(superadmin_required, login_url=('/login_view'))
def offers(request):
    all_offers = Offer.objects.all().order_by('-created_at')
    context = {
        'offers':          all_offers,
        'scheduled_count': all_offers.filter(status='Scheduled').count(),
        'expired_count':   all_offers.filter(status='Expired').count(),
        'total_used':      sum(o.used_count for o in all_offers),
    }
    return render(request,'dash/offers/offers.html',context)

@user_passes_test(superadmin_required, login_url=('/login_view'))
def add_offer(request):
    if request.method == 'POST':
 
        # ── Core ──
        title       = request.POST.get('title')
        description = request.POST.get('description')
        trigger     = request.POST.get('trigger')
        status      = request.POST.get('status')
 
        # ── Coupon ──
        coupon_code      = request.POST.get('coupon_code') or None
        usage_limit      = request.POST.get('usage_limit') or None
        one_per_customer = request.POST.get('one_per_customer') == 'True'
 
        # ── Condition ──
        condition_type = request.POST.get('condition_type')
        min_order_amount   = request.POST.get('min_order_amount') or None
        min_quantity       = request.POST.get('min_quantity') or None
        condition_product_id     = request.POST.get('condition_product') or None
        condition_category_id    = request.POST.get('condition_category') or None
        condition_sub_category_id = request.POST.get('condition_sub_category') or None
 
        # ── Action ──
        action_type      = request.POST.get('action_type')
        discount_value   = request.POST.get('discount_value') or 0
        max_discount_cap = request.POST.get('max_discount_cap') or None
        free_product_id  = request.POST.get('free_product') or None
        free_variant_id  = request.POST.get('free_variant') or None
        bundle_price     = request.POST.get('bundle_price') or None
        bundle_products  = request.POST.getlist('bundle_products')
        buy_quantity     = request.POST.get('buy_quantity') or None
        get_quantity     = request.POST.get('get_quantity') or None
 
        # ── Validity ──
        valid_from = request.POST.get('valid_from')
        valid_to   = request.POST.get('valid_to')
        stackable  = request.POST.get('stackable') == 'True'
        priority   = request.POST.get('priority') or 0
 
        offer = Offer.objects.create(
            title=title,
            description=description,
            trigger=trigger,
            status=status,
            coupon_code=coupon_code,
            usage_limit=usage_limit,
            one_per_customer=one_per_customer,
            condition_type=condition_type,
            min_order_amount=min_order_amount,
            min_quantity=min_quantity,
            condition_product_id=condition_product_id,
            condition_category_id=condition_category_id,
            condition_sub_category_id=condition_sub_category_id,
            action_type=action_type,
            discount_value=discount_value,
            max_discount_cap=max_discount_cap,
            free_product_id=free_product_id,
            free_variant_id=free_variant_id,
            bundle_price=bundle_price,
            buy_quantity=buy_quantity,
            get_quantity=get_quantity,
            valid_from=valid_from,
            valid_to=valid_to,
            stackable=stackable,
            priority=priority,
        )
 
        # ManyToMany bundle products
        if bundle_products:
            offer.bundle_products.set(bundle_products)
 
        return redirect('/offers')
 
    context = {
        'products':     Product.objects.all().order_by('name'),
        'variants':     Variant.objects.all().order_by('product__name'),
        'categories':   Category.objects.filter(status='Enabled').order_by('title'),
        'subcategories': SubCategory.objects.filter(status='Enabled').order_by('title'),
    }
    return render(request, 'dash/offers/add_offer.html', context)
 
 
@user_passes_test(superadmin_required, login_url=('/login_view'))
def delete_offer(request, id):
    offer = get_object_or_404(Offer, id=id)
    offer.delete()
    return redirect('/offers')
 
 
@user_passes_test(superadmin_required, login_url=('/login_view'))
def activate_offer(request, id):
    offer = get_object_or_404(Offer, id=id)
    offer.status = 'Active'
    offer.save()
    return redirect('/offers')
 
 
@user_passes_test(superadmin_required, login_url=('/login_view'))
def deactivate_offer(request, id):
    offer = get_object_or_404(Offer, id=id)
    offer.status = 'Inactive'
    offer.save()
    return redirect('/offers')

@user_passes_test(superadmin_required, login_url=('/login_view'))
def edit_offer(request, id):
    offer = get_object_or_404(Offer, id=id)
 
    if request.method == 'POST':
 
        # ── Core ──
        offer.title       = request.POST.get('title')
        offer.description = request.POST.get('description')
        offer.trigger     = request.POST.get('trigger')
        offer.status      = request.POST.get('status')
 
        # ── Coupon ──
        offer.coupon_code      = request.POST.get('coupon_code') or None
        offer.usage_limit      = request.POST.get('usage_limit') or None
        offer.one_per_customer = request.POST.get('one_per_customer') == 'True'
 
        # ── Condition ──
        offer.condition_type              = request.POST.get('condition_type')
        offer.min_order_amount            = request.POST.get('min_order_amount') or None
        offer.min_quantity                = request.POST.get('min_quantity') or None
        offer.condition_product_id        = request.POST.get('condition_product') or None
        offer.condition_category_id       = request.POST.get('condition_category') or None
        offer.condition_sub_category_id   = request.POST.get('condition_sub_category') or None
 
        # ── Action ──
        offer.action_type      = request.POST.get('action_type')
        offer.discount_value   = request.POST.get('discount_value') or 0
        offer.max_discount_cap = request.POST.get('max_discount_cap') or None
        offer.free_product_id  = request.POST.get('free_product') or None
        offer.free_variant_id  = request.POST.get('free_variant') or None
        offer.bundle_price     = request.POST.get('bundle_price') or None
        offer.buy_quantity     = request.POST.get('buy_quantity') or None
        offer.get_quantity     = request.POST.get('get_quantity') or None
 
        # ── Validity ──
        offer.valid_from = request.POST.get('valid_from')
        offer.valid_to   = request.POST.get('valid_to')
        offer.stackable  = request.POST.get('stackable') == 'True'
        offer.priority   = request.POST.get('priority') or 0
 
        offer.save()
 
        # ManyToMany bundle products
        bundle_products = request.POST.getlist('bundle_products')
        offer.bundle_products.set(bundle_products)
 
        return redirect('/offers')
 
    context = {
        'data':          offer,
        'products':      Product.objects.all().order_by('name'),
        'variants':      Variant.objects.all().order_by('product__name'),
        'categories':    Category.objects.filter(status='Enabled').order_by('title'),
        'subcategories': SubCategory.objects.filter(status='Enabled').order_by('title'),
    }
    return render(request, 'dash/offers/edit_offer.html', context)

# Customers Management
@user_passes_test(superadmin_required, login_url=('/login_view'))
def customers(request):
    customers = Customers.objects.all().order_by('-id')
    return render(request, 'dash/customer/customers.html', {'customers': customers})

# Support Management
@user_passes_test(superadmin_required, login_url=('/login_view'))
def support(request):
    enquiries = Support.objects.all().order_by('-created_at')
    return render(request, 'dash/support/support.html', {'enquiries': enquiries})


@user_passes_test(superadmin_required, login_url=('/login_view'))
def resolve_enquiry(request, id):
    enquiry = get_object_or_404(Support, id=id)
    enquiry.status = 'Resolved'
    enquiry.save()
    return redirect('/support')

#Intelligence 
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta

def intelligence(request):
    today = timezone.now().date()
    this_month_start = today.replace(day=1)

    context = {
        # Products
        'total_products':     Product.objects.count(),
        'out_of_stock':       Variant.objects.filter(quantity=0).count(),
        'low_stock':          Variant.objects.filter(quantity__gt=0, quantity__lt=10).count(),
        'disabled_products':  0,

        # Orders
        'orders_today':       Order.objects.filter(created_at__date=today).count(),
        'revenue_today':      Order.objects.filter(created_at__date=today, payment_status='paid').aggregate(t=Sum('total'))['t'] or 0,
        'revenue_month':      Order.objects.filter(created_at__date__gte=this_month_start, payment_status='paid').aggregate(t=Sum('total'))['t'] or 0,
        'revenue_all_time':   Order.objects.filter(payment_status='paid').aggregate(t=Sum('total'))['t'] or 0,
        'avg_order_value':    Order.objects.filter(payment_status='paid').aggregate(a=Avg('total'))['a'] or 0,
        'pending_orders':     Order.objects.filter(status='pending').count(),
        'orders_by_status':   Order.objects.values('status').annotate(count=Count('id')),

        # Carts
        'active_carts':       Cart.objects.filter(is_abandoned=False).count(),
        'abandoned_carts':    Cart.objects.filter(is_abandoned=True).count(),

        # Offers
        'active_offers':      Offer.objects.filter(status='Active').count(),
        'total_discount':     Order.objects.aggregate(t=Sum('discount'))['t'] or 0,
        'expiring_offers':    Offer.objects.filter(valid_to__date__lte=today + timedelta(days=7), status='Active').count(),

        # Support
        'pending_support':    Support.objects.filter(status='Pending').count(),
        'resolved_today':     Support.objects.filter(status='Resolved', created_at__date=today).count(),
        'total_support':      Support.objects.count(),
    }
    return render(request, 'dash/intelligence/intelligence.html', context)

#Order Managment

@user_passes_test(superadmin_required, login_url=('/login_view'))
def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    order_items = order.order_items.all()
    return render(request, 'dash/orders/detail.html', {
        'order':       order,
        'order_items': order_items,
    })


@user_passes_test(superadmin_required, login_url=('/login_view'))
def update_order_status(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            order.status = new_status
            order.save()
    return redirect(f'/order_detail/{id}')


@user_passes_test(superadmin_required, login_url=('/login_view'))
def revoke_order(request, id):
    order = get_object_or_404(Order, id=id)

    # Restore stock for each item
    for item in order.order_items.all():
        if item.variant:
            item.variant.quantity += item.quantity
            item.variant.save()

    order.status = 'cancelled'
    order.save()
    return redirect(f'/order_detail/{id}')


@user_passes_test(superadmin_required, login_url=('/login_view'))
def fulfill_order(request, id):
    import requests
    import json

    order = get_object_or_404(Order, id=id)

    # ── Shiprocket Auth ──
    auth_response = requests.post(
        'https://apiv2.shiprocket.in/v1/external/auth/login',
        json={
            'email':    'YOUR_SHIPROCKET_EMAIL',
            'password': 'YOUR_SHIPROCKET_PASSWORD',
        }
    )
    token = auth_response.json().get('token')

    if not token:
        order.notes += '\n[Shiprocket] Auth failed.'
        order.save()
        return redirect(f'/order_detail/{id}')

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type':  'application/json',
    }

    # ── Build Order Items for Shiprocket ──
    items = []
    for item in order.order_items.all():
        items.append({
            'name':          item.product_name,
            'sku':           f'SKU-{item.product_id or 0}',
            'units':         item.quantity,
            'selling_price': str(item.price),
            'discount':      '0',
            'tax':           str(item.gst),
        })

    # ── Create Shiprocket Order ──
    payload = {
        'order_id':               str(order.id),
        'order_date':             order.created_at.strftime('%Y-%m-%d %H:%M'),
        'pickup_location':        'Primary',
        'channel_id':             '',
        'comment':                order.notes or '',
        'billing_customer_name':  order.full_name,
        'billing_last_name':      '',
        'billing_address':        order.address_line_1,
        'billing_address_2':      order.address_line_2,
        'billing_city':           order.city,
        'billing_pincode':        order.pincode,
        'billing_state':          order.state,
        'billing_country':        order.country,
        'billing_email':          order.email,
        'billing_phone':          order.phone,
        'shipping_is_billing':    True,
        'order_items':            items,
        'payment_method':         'Prepaid' if order.payment_method == 'razorpay' else 'COD',
        'sub_total':              str(order.subtotal),
        'length':                 str(order.total_length),
        'breadth':                str(order.total_breadth),
        'height':                 str(order.total_height),
        'weight':                 str(order.total_weight),
    }

    sr_response = requests.post(
        'https://apiv2.shiprocket.in/v1/external/orders/create/adhoc',
        headers=headers,
        json=payload,
    )
    sr_data = sr_response.json()

    if sr_response.status_code == 200 and sr_data.get('order_id'):
        order.shiprocket_order_id    = str(sr_data.get('order_id', ''))
        order.shiprocket_shipment_id = str(sr_data.get('shipment_id', ''))
        order.awb_code               = str(sr_data.get('awb_code', ''))
        order.courier_name           = str(sr_data.get('courier_name', ''))
        order.status                 = 'ready_for_pickup'
        order.notes += f'\n[Shiprocket] Order created. AWB: {order.awb_code}'
    else:
        order.notes += f'\n[Shiprocket] Failed: {sr_data}'

    order.save()
    return redirect(f'/order_detail/{id}')