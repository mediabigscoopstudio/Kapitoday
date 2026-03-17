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
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)