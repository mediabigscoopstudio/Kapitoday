import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/urls.py'
with open(filepath, 'r') as f:
    content = f.read()

target = "path('verify_payment/', views.verify_payment, name='verify_payment'),"
addition = """    path('verify_payment/', views.verify_payment, name='verify_payment'),
    
    # Fast Checkout APIs
    path('api/fc/state/', views.fc_get_state, name='fc_get_state'),
    path('api/fc/cart/update/', views.fc_update_cart, name='fc_update_cart'),
    path('api/fc/coupon/apply/', views.fc_apply_coupon, name='fc_apply_coupon'),
    path('api/fc/payment/init/', views.fc_init_payment, name='fc_init_payment'),
    path('api/fc/payment/verify/', views.fc_verify_payment, name='fc_verify_payment'),
"""

if target in content and "api/fc/state/" not in content:
    content = content.replace(target, addition)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Added Fast Checkout URLs.")
