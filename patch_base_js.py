import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

target = "function updateCartItem(id, action) {"

addition = """function fcAddRecommended(productId) {
        // Find the first variant ID if any (we can assume default or None)
        fetch('/shop/add-to-cart/', {
            method: 'POST',
            headers: {'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded'},
            body: new URLSearchParams({
                'product_id': productId,
                'quantity': 1,
                'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : ''
            })
        }).then(r => r.json()).then(data => {
            if(data.success) fcUpdateUI(data);
        });
    }
    
    function updateCartItem(id, action) {"""

content = content.replace(target, addition)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched base js for recommended.")
