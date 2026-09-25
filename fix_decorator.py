import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/dash/views.py'
with open(filepath, 'r') as f:
    content = f.read()

bad_code = """@user_passes_test(superadmin_required, login_url=('/login_view'))
from datetime import timedelta
from django.utils import timezone

def index(request):"""

good_code = """from datetime import timedelta
from django.utils import timezone

@user_passes_test(superadmin_required, login_url=('/login_view'))
def index(request):"""

content = content.replace(bad_code, good_code)

with open(filepath, 'w') as f:
    f.write(content)
print("Fixed decorator syntax.")
