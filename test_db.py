import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kapitoday.settings")
django.setup()

from dash.models import Category
cats = Category.objects.all()
for c in cats:
    print(c.name, c.image)
