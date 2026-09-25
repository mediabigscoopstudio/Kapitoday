from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('auth/google-login/', views.google_login, name='google_login'),
    path('logout/', views.custom_logout, name='logout'),
    path('subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),

    path("", views.index, name='index'),
    path("about", views.about, name='about'),
    path("learn", views.learn, name='learn'),
    
    # CMS / Content Routes
    path("content/", views.content, name='content'),
    # Shop Routes
    path("shop/", views.shop, name='shop'),
    path("shop/category/<slug:category_slug>/", views.shop, name='shop_category'),
    path("shop/add-to-cart/", views.add_to_cart, name='add_to_cart'),
    path("<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/", views.product_detail, name='product_detail'),
    
    # Must come after exact matches to avoid catching them
    path("<slug:category_slug>/", views.content, name='category_detail'),
    path("<slug:category_slug>/<slug:article_slug>/", views.article_detail, name='article_detail'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
