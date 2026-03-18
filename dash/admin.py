from django.contrib import admin
from .models import Customers, Category, SubCategory, Product, ProductImage, Variant, Highlight, APlusContent,Offer
from .models import Support,Cart,CartItem,Order,OrderItem

admin.site.register(Customers)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Variant)
admin.site.register(Highlight)
admin.site.register(APlusContent)
admin.site.register(Offer)
admin.site.register(Support)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)