import os

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/index.html'
with open(filepath, 'r') as f:
    content = f.read()

css_addition = """
/* ==========================================
   STAGE 6-8: ROAST, BREW, ORIGINS
   ========================================== */
.roast-card {
    transition: all 0.3s ease;
}
.roast-card:hover {
    background: rgba(255,255,255,0.1) !important;
    transform: translateX(10px);
}
.brew-card img {
    transition: transform 0.4s ease;
}
.brew-card:hover img {
    transform: scale(1.05);
}
"""
content = content.replace("</style>", css_addition + "\n</style>")

body_addition = """
    {% include 'main/components/roast_spectrum.html' %}
    {% include 'main/components/brew_methods.html' %}
    {% include 'main/components/origins_video.html' %}
"""
content = content.replace("<!-- Stage 6-11 components will go here -->", body_addition + "\n    <!-- Stage 9-11 components will go here -->")

with open(filepath, 'w') as f:
    f.write(content)

print("index.html patched with Stages 6-8.")
