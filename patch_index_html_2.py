import os

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/index.html'
with open(filepath, 'r') as f:
    content = f.read()

css_addition = """
/* ==========================================
   STAGE 5: BESTSELLERS
   ========================================== */
.bestsellers-scroll {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 20px;
}
.bestsellers-scroll::-webkit-scrollbar {
    display: none;
}
.kapi-product-card {
    transition: transform 0.3s;
}
.kapi-product-card:hover {
    transform: translateY(-5px);
}
.variant-selector-pills .btn-check:checked + .btn-outline-secondary {
    background-color: var(--kapi-plantation-dark, #1B3A28);
    color: #fff;
    border-color: var(--kapi-plantation-dark, #1B3A28);
}
.variant-selector-pills .btn-outline-secondary {
    border-color: #dee2e6;
    color: var(--kapi-espresso);
}
"""
content = content.replace("</style>", css_addition + "\n</style>")

body_addition = """
    {% include 'main/components/bestsellers.html' %}
"""
content = content.replace("<!-- Stage 5-11 components will go here -->", body_addition + "\n    <!-- Stage 6-11 components will go here -->")

with open(filepath, 'w') as f:
    f.write(content)

print("index.html patched with Stage 5.")
