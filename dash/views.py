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