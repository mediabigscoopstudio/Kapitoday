import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kapitoday.settings')
django.setup()

from dash.models import Product, Category, SubCategory

print("CATEGORIES:")
for c in Category.objects.all():
    print(f" - {c.title} (ID: {c.id})")
    
print("\nSUBCATEGORIES:")
for sc in SubCategory.objects.all():
    print(f" - {sc.title} (ID: {sc.id})")

print("\nPRODUCTS:")
for p in Product.objects.all()[:10]:
    print(f" - {p.name} (ID: {p.id}) (Cat: {p.category.title if p.category else 'None'})")
