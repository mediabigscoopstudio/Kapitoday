import os
import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the index view
pattern = r'def index\(request\):.*?return render\(request, \'main/index\.html\', {\'bestseller_products\': bestseller_products}\)'
replacement = """def index(request):
    from dash.models import Product, Category
    
    # 1. Categories for Category Strip
    categories = Category.objects.filter(status='Enabled')[:8]
    
    # 2. Bestseller Products (Eagerly fetch variants to prevent N+1 queries)
    bestseller_names = [
        'Kapi Today Araku Valley Medium Roast',
        'Kapi Today Chikmagalur Medium Roast',
        'Kapi Today South Indian Coffee Filter',
        'Kapi Today Wayanad Dark Roast'
    ]
    bestseller_products = []
    for name in bestseller_names:
        prod = Product.objects.prefetch_related('product_variant').filter(name__icontains=name.replace('Kapi Today ', '')).first()
        if prod:
            bestseller_products.append(prod)
    
    context = {
        'categories': categories,
        'bestseller_products': bestseller_products,
    }
    return render(request, 'main/index.html', context)"""

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
with open(filepath, 'w') as f:
    f.write(new_content)
print("views.py patched.")
