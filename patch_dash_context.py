import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/dash/views.py'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """    return render(request, 'dash/index.html', {
        'orders': orders,
        'grouped_orders': grouped_orders,
        'all_orders_count': all_orders.count()
    })"""

new_code = """    return render(request, 'dash/index.html', {
        'orders': orders,
        'grouped_orders': grouped_orders,
        'all_orders_count': all_orders.count(),
        'current_filter': time_filter
    })"""

if "current_filter" not in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched dash context.")
else:
    print("Already patched.")
