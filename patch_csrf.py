filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

target = """<!-- FAST CHECKOUT DRAWER -->
    <div class="offcanvas offcanvas-end" tabindex="-1" id="fastCheckoutDrawer" aria-labelledby="fcDrawerLabel" style="width: 100%; max-width: 500px; border-left: none; box-shadow: -5px 0 25px rgba(0,0,0,0.1); background-color: #fdfaf4;">"""
    
addition = """<!-- FAST CHECKOUT DRAWER -->
    <div class="offcanvas offcanvas-end" tabindex="-1" id="fastCheckoutDrawer" aria-labelledby="fcDrawerLabel" style="width: 100%; max-width: 500px; border-left: none; box-shadow: -5px 0 25px rgba(0,0,0,0.1); background-color: #fdfaf4;">
        <form style="display:none;">{% csrf_token %}</form>"""

content = content.replace(target, addition)

with open(filepath, 'w') as f:
    f.write(content)
