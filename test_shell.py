from dash.models import Product, Variant
p = Product.objects.first()
print("Product:", p.name)
print("Variants count:", p.product_variant.count())
if p.product_variant.exists():
    print("Price:", p.product_variant.first().price)
