import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

old_fcui = """        // Update header cart counters everywhere
        document.querySelectorAll('.cart-count, .cart-title-count').forEach(el => el.innerText = fcState.cartCount);
        
        // Update Cart HTML"""

new_fcui = """        // Update header cart counters everywhere
        document.querySelectorAll('.cart-count, .cart-title-count').forEach(el => el.innerText = fcState.cartCount);
        
        // Also update the nav text format e.g. "Cart (3)"
        const navCartLinks = document.querySelectorAll('a[data-bs-toggle="offcanvas"][data-bs-target="#fastCheckoutDrawer"]');
        navCartLinks.forEach(link => {
            if(link.innerHTML.includes('Cart (')) {
                link.innerHTML = '<i class="bi bi-bag"></i> Cart (' + fcState.cartCount + ')';
            }
        });
        
        // Update Cart HTML"""

content = content.replace(old_fcui, new_fcui)

with open(filepath, 'w') as f:
    f.write(content)
