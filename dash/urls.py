from django.contrib import admin
from django.urls import path
from dash import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.index,name='index'),
    path("login_view",views.login_view,name='login_view'),
    path("logout_view",views.logout_view,name='logout_view'),
    #Category Management urls
    path("category",views.category,name='category'),
    path("add_category",views.add_category,name='add_category'),
    path("edit_category/<id>",views.edit_category,name='edit_category'),
    path("delete_category/<id>",views.delete_category,name='delete_category'),
    path("enable_category/<id>",views.enable_category,name='enable_category'),
    path("disable_category/<id>",views.disable_category,name='disable_category'),
    #Sub-Category Management 
    path('sub_category_list', views.sub_category_list, name='sub_category_list'),
    path('add_sub_category', views.add_sub_category, name='add_sub_category'),
    path('edit_sub_category/<int:pk>/', views.edit_sub_category, name='edit_sub_category'),
    path('enable_sub_category/<int:pk>/', views.enable_sub_category, name='enable_sub_category'),
    path('disable_sub_category/<int:pk>/', views.disable_sub_category, name='disable_sub_category'),
    path('delete_sub_category/<int:pk>/', views.delete_sub_category, name='delete_sub_category'),
    #Product Management urls
    path('products/', views.product, name='product'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<id>', views.edit_product, name='edit_product'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)