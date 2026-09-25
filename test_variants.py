import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kapitoday.settings")
django.setup()

from dash.models import Product
p = Product.objects.prefetch_related('product_variant').first()
if p:
    variants = p.product_variant.all()
    print("Product:", p.name)
    if variants:
        print("Variants:", [(v.id, v.price) for v in variants])
    else:
        print("No variants")
