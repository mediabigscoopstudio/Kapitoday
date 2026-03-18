from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import Category,SubCategory,Product,ProductImage,Highlight,APlusContent,Variant

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

@user_passes_test(superadmin_required, login_url=('/login_view'))
def index(request):
    return render(request,'dash/index.html')

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
        description      = request.POST.get('description')   # comes as HTML from Quill
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
        for i, vname in enumerate(variant_names):
            if vname.strip():
                Variant.objects.create(
                    product=product,
                    name=vname,
                    price=variant_prices[i]        if i < len(variant_prices)     else 0,
                    gst=variant_gsts[i]            if i < len(variant_gsts)       else 0,
                    quantity=variant_quantities[i] if i < len(variant_quantities) else 0,
                    status=variant_statuses[i]     if i < len(variant_statuses)   else 'Enabled',
                    image=variant_images[i]        if i < len(variant_images)     else None,
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
        product.description      = request.POST.get('description')   # HTML from Quill
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
 
        # New Variants
        variant_names      = request.POST.getlist('variant_name')
        variant_prices     = request.POST.getlist('variant_price')
        variant_gsts       = request.POST.getlist('variant_gst')
        variant_quantities = request.POST.getlist('variant_quantity')
        variant_statuses   = request.POST.getlist('variant_status')
        variant_images     = request.FILES.getlist('variant_image')
        for i, vname in enumerate(variant_names):
            if vname.strip():
                Variant.objects.create(
                    product=product,
                    name=vname,
                    price=variant_prices[i]        if i < len(variant_prices)     else 0,
                    gst=variant_gsts[i]            if i < len(variant_gsts)       else 0,
                    quantity=variant_quantities[i] if i < len(variant_quantities) else 0,
                    status=variant_statuses[i]     if i < len(variant_statuses)   else 'Enabled',
                    image=variant_images[i]        if i < len(variant_images)     else None,
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