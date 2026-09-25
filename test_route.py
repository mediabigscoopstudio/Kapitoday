import os, django
from django.test import Client
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kapitoday.settings")
django.setup()

from django.contrib.auth.models import User

# Need a superuser to test dash routes
su = User.objects.filter(is_superuser=True).first()
if su:
    c = Client()
    c.force_login(su)
    resp = c.get('/dash/support-kanban/')
    print(resp.status_code)
    if resp.status_code == 500:
        # print error traceback somehow? Actually the client might throw it if DEBUG is true.
        try:
            resp = c.get('/dash/support-kanban/', follow=True)
            print(resp.content.decode('utf-8')[:500])
        except Exception as e:
            import traceback
            traceback.print_exc()
else:
    print("No superuser found.")
