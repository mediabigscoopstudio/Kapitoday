import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/dash/views.py'
with open(filepath, 'r') as f:
    content = f.read()

old_func = """def index(request):
    all_orders = Order.objects.all().order_by('-created_at')
    
    grouped_orders = {"""

new_func = """from datetime import timedelta
from django.utils import timezone

def index(request):
    time_filter = request.GET.get('time_filter', 'last_6_months')
    now = timezone.now()
    
    orders_qs = Order.objects.all().order_by('-created_at')
    
    if time_filter == 'today':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        orders_qs = orders_qs.filter(created_at__gte=start_date)
    elif time_filter == 'this_week':
        start_date = now - timedelta(days=now.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        orders_qs = orders_qs.filter(created_at__gte=start_date)
    elif time_filter == 'this_month':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        orders_qs = orders_qs.filter(created_at__gte=start_date)
    elif time_filter == 'this_quarter':
        quarter_month = ((now.month - 1) // 3) * 3 + 1
        start_date = now.replace(month=quarter_month, day=1, hour=0, minute=0, second=0, microsecond=0)
        orders_qs = orders_qs.filter(created_at__gte=start_date)
    elif time_filter == 'last_6_months':
        start_date = now - timedelta(days=180)
        orders_qs = orders_qs.filter(created_at__gte=start_date)
        
    all_orders = orders_qs
    
    grouped_orders = {"""

content = content.replace(old_func, new_func)

# We also need to pass the time_filter back to the template
old_render = "return render(request, 'dash/index.html', {'grouped_orders': grouped_orders})"
new_render = "return render(request, 'dash/index.html', {'grouped_orders': grouped_orders, 'current_filter': time_filter})"
content = content.replace(old_render, new_render)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched dash views for time filter.")
