import os
import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/index.html'
with open(filepath, 'r') as f:
    content = f.read()

# Add CSS for Stage 4
css_addition = """
/* ==========================================
   STAGE 4: CATEGORY & STORY
   ========================================== */
.category-strip-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none; /* Firefox */
}
.category-strip-container::-webkit-scrollbar {
    display: none; /* Safari and Chrome */
}
.category-strip {
    display: flex;
    gap: 20px;
    padding-bottom: 10px;
}
.category-card {
    text-align: center;
    text-decoration: none;
    flex: 0 0 auto;
    width: 100px;
}
.category-img-wrapper {
    width: 90px;
    height: 90px;
    border-radius: 24px; /* Squircle look */
    overflow: hidden;
    margin: 0 auto 10px;
    background-color: var(--kapi-cream-warm, #F5EDE0);
    transition: transform 0.3s;
    border: 1px solid rgba(0,0,0,0.05);
}
.category-card:hover .category-img-wrapper {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
.category-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.category-placeholder {
    width: 100%;
    height: 100%;
    background: var(--kapi-cream-dark, #EBE0D0);
}
.category-name {
    color: var(--kapi-espresso);
    font-size: 0.85rem;
    font-weight: 600;
}

.kapi-story-card {
    background-color: var(--kapi-cream, #FAF6F0);
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.05);
}
.kapi-story-image img {
    min-height: 400px;
}
"""

content = content.replace("</style>", css_addition + "\n</style>")

# Add Includes
body_addition = """
    {% include 'main/components/categories.html' %}
    {% include 'main/components/story.html' %}
"""
content = content.replace("<!-- Stage 4-11 components will go here -->", body_addition + "\n    <!-- Stage 5-11 components will go here -->")

with open(filepath, 'w') as f:
    f.write(content)

print("index.html patched with Stage 4.")
