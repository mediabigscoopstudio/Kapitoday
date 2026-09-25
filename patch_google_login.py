import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

old_login_success = """        .then(data => {
          if(data.success) {
            window.location.reload();
          } else {"""

new_login_success = """        .then(data => {
          if(data.success) {
            let fcDrawer = document.getElementById('fastCheckoutDrawer');
            if (fcDrawer && fcDrawer.classList.contains('show')) {
                fcFetchState();
                fcSetStep('address');
            } else {
                window.location.reload();
            }
          } else {"""

content = content.replace(old_login_success, new_login_success)

with open(filepath, 'w') as f:
    f.write(content)

print("Patched Google login callback.")
