import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

old_func = """function fcAddRecommended(productId) {
        // Find the first variant ID if any (we can assume default or None)
        fetch('/shop/add-to-cart/', {
            method: 'POST',
            headers: {'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded'},
            body: new URLSearchParams({
                'product_id': productId,
                'quantity': 1,
                'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : ''
            })"""

new_func = """function fcAddRecommended(productId, variantId = '') {
        let params = {
            'product_id': productId,
            'quantity': 1,
            'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : ''
        };
        if (variantId) params['variant_id'] = variantId;
        
        fetch('/shop/add-to-cart/', {
            method: 'POST',
            headers: {'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded'},
            body: new URLSearchParams(params)"""

content = content.replace(old_func, new_func)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched base js for recommended variants.")
