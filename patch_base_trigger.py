import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

old_trigger = """  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('trigger_login') === 'true') {
      google.accounts.id.prompt();
  }"""

new_trigger = """  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('trigger_login') === 'true') {
      google.accounts.id.prompt();
  }
  
  if (urlParams.get('open_checkout')) {
      const step = urlParams.get('open_checkout') === 'true' ? 'cart' : urlParams.get('open_checkout');
      const cartOffcanvas = document.getElementById('fastCheckoutDrawer');
      const bsOffcanvas = bootstrap.Offcanvas.getInstance(cartOffcanvas) || new bootstrap.Offcanvas(cartOffcanvas);
      
      // Wait slightly for FC state to initialize
      setTimeout(() => {
          bsOffcanvas.show();
          if (step !== 'cart') fcSetStep(step);
      }, 300);
  }"""

content = content.replace(old_trigger, new_trigger)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched base.html URL trigger.")
