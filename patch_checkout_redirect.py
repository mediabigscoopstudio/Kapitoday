import re
filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/main/views.py'
with open(filepath, 'r') as f:
    content = f.read()

# I will just replace the content of `def checkout(request):` with a redirect
# because the prompt says: "The checkout should NOT redirect the customer to a traditional checkout page."
old_checkout = re.search(r"@login_required\(login_url='/\?trigger_login=true'\)\ndef checkout\(request\):.*?(?=@csrf_exempt\ndef verify_payment)", content, re.DOTALL)

if old_checkout:
    new_checkout = """def checkout(request):
    return redirect('/?open_checkout=true')

"""
    content = content.replace(old_checkout.group(0), new_checkout)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Replaced checkout view with a redirect.")
