import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """                cart.cart_items.all().delete()
                if 'applied_coupon' in request.session:
                    del request.session['applied_coupon']
                if 'discount_amt' in request.session:
                    del request.session['discount_amt']
                
                # We could send email here if we want, ignoring for brevity of the API
                
                return JsonResponse({'success': True, 'order_db_id': order.id})"""

new_block = """                cart.cart_items.all().delete()
                if 'applied_coupon' in request.session:
                    del request.session['applied_coupon']
                if 'discount_amt' in request.session:
                    del request.session['discount_amt']
                
                # Send confirmation email
                try:
                    from django.core.mail import EmailMultiAlternatives
                    from django.template.loader import render_to_string
                    from django.conf import settings
                    base_url = request.build_absolute_uri('/')[:-1]
                    html_content = render_to_string('emails/order_confirmation.html', {'order': order, 'base_url': base_url})
                    msg = EmailMultiAlternatives('Order Confirmation - Kapi Today', 'Your order is confirmed!', settings.DEFAULT_FROM_EMAIL, [order.email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send(fail_silently=False)
                    
                    # Send tracking email immediately as requested
                    track_html = render_to_string('emails/track_order.html', {'order': order, 'base_url': base_url})
                    msg2 = EmailMultiAlternatives('Track Your Kapi Today Order', 'Track your coffee order!', settings.DEFAULT_FROM_EMAIL, [order.email])
                    msg2.attach_alternative(track_html, "text/html")
                    msg2.send(fail_silently=False)
                except Exception as e:
                    print("Order email failed:", e)
                
                return JsonResponse({'success': True, 'order_db_id': order.id})"""

content = content.replace(old_block, new_block)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched email logic.")
