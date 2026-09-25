import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

old_ajax = re.search(r"\.then\(data => \{\s*if \(data\.success\) \{\s*// Update cart count badges globally.*?(?=if \(submitBtn\))", content, re.DOTALL)

if old_ajax:
    new_ajax = """.then(data => {
            if (data.success) {
                if(typeof fcUpdateUI === 'function') fcUpdateUI(data);
                fcSetStep('cart');
                const cartOffcanvas = document.getElementById('fastCheckoutDrawer');
                const bsOffcanvas = bootstrap.Offcanvas.getInstance(cartOffcanvas) || new bootstrap.Offcanvas(cartOffcanvas);
                bsOffcanvas.show();
            }
            """
    content = content.replace(old_ajax.group(0), new_ajax)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched base.html AJAX add_to_cart handler.")
else:
    print("Could not find AJAX handler block.")
