from django.contrib import admin
from .models import Customers, Category, SubCategory, Product, ProductImage, Variant, Highlight, APlusContent

admin.site.register(Customers)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Variant)
admin.site.register(Highlight)
admin.site.register(APlusContent)