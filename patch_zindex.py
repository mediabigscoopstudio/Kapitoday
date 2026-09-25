filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/static/main/css/checkout.css'
with open(filepath, 'r') as f:
    content = f.read()

target = """#fastCheckoutDrawer {
    width: 100%;
    max-width: 500px;
    background-color: #fdfaf4; /* Warm cream */
    border-left: none;
    box-shadow: -5px 0 25px rgba(0,0,0,0.1);
}"""

addition = """#fastCheckoutDrawer {
    width: 100%;
    max-width: 500px;
    background-color: #fdfaf4; /* Warm cream */
    border-left: none;
    box-shadow: -5px 0 25px rgba(0,0,0,0.1);
    z-index: 1060 !important; /* Ensure it floats above sticky headers */
}"""

content = content.replace(target, addition)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched z-index in checkout.css.")
