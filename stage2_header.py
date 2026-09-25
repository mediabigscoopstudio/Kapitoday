import os

BASE_DIR = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday'

# 1. announcement.html
announcement_html = """
<div class="announcement-bar d-none d-lg-block">
    <div class="container-fluid">
        <div class="d-flex justify-content-center align-items-center gap-4">
            <div class="announcement-item"><i class="bi bi-box-seam"></i> FREE SHIPPING ABOVE ₹799</div>
            <div class="announcement-item"><i class="bi bi-fire"></i> FRESHLY ROASTED & PACKED</div>
            <div class="announcement-item"><i class="bi bi-tree"></i> SOURCED FROM INDIAN PLANTATIONS</div>
            <div class="announcement-item"><i class="bi bi-heart"></i> TRUSTED BY 10,000+ COFFEE LOVERS</div>
        </div>
    </div>
</div>
<!-- Mobile Announcement Ticker (Optional, keeping it simple for now) -->
<div class="announcement-bar d-block d-lg-none">
    <div class="ticker-track">
        <div class="ticker-item"><i class="bi bi-box-seam"></i> FREE SHIPPING ABOVE ₹799</div>
        <div class="ticker-item"><i class="bi bi-fire"></i> FRESHLY ROASTED & PACKED</div>
        <div class="ticker-item"><i class="bi bi-tree"></i> SOURCED FROM INDIAN PLANTATIONS</div>
    </div>
</div>
"""
with open(os.path.join(BASE_DIR, 'template/main/components/announcement.html'), 'w') as f:
    f.write(announcement_html)


# 2. header.html
header_html = """
<header class="kapi-header">
    <div class="container-fluid px-4">
        <!-- Desktop Header -->
        <div class="row align-items-center d-none d-lg-flex py-3">
            <!-- Left Nav -->
            <div class="col-4">
                <nav class="desktop-nav-links">
                    <a href="/shop">Shop</a>
                    <a href="/origins">Origins</a>
                    <a href="/learn">Learn</a>
                    <a href="/about">Our Story</a>
                    <a href="/journal">Journal</a>
                </nav>
            </div>
            <!-- Center Logo -->
            <div class="col-4 text-center">
                <a href="/" class="header-logo">
                    <img src="/static/main/logos/Vector.webp" alt="Kapi Today" height="60">
                </a>
            </div>
            <!-- Right Actions -->
            <div class="col-4 d-flex justify-content-end align-items-center gap-3">
                <div class="search-bar">
                    <i class="bi bi-search"></i>
                    <input type="text" placeholder="Search coffee, equipment...">
                </div>
                <a href="/my-orders/" class="header-icon"><i class="bi bi-person"></i></a>
                <a href="/cart" class="header-icon position-relative">
                    <i class="bi bi-bag"></i>
                    {% if cart_items_count > 0 %}
                    <span class="cart-badge">{{ cart_items_count }}</span>
                    {% endif %}
                </a>
            </div>
        </div>

        <!-- Mobile Header -->
        <div class="d-flex d-lg-none align-items-center justify-content-between py-3">
            <button class="mobile-menu-btn" type="button" data-bs-toggle="offcanvas" data-bs-target="#mobileMenu">
                <i class="bi bi-list"></i>
            </button>
            
            <a href="/" class="header-logo">
                <img src="/static/main/logos/Vector.webp" alt="Kapi Today" height="50">
            </a>
            
            <div class="d-flex align-items-center gap-3">
                <a href="#" class="header-icon"><i class="bi bi-search"></i></a>
                <a href="/cart" class="header-icon position-relative">
                    <i class="bi bi-bag"></i>
                    {% if cart_items_count > 0 %}
                    <span class="cart-badge">{{ cart_items_count }}</span>
                    {% endif %}
                </a>
            </div>
        </div>
    </div>
</header>

<!-- Mobile Menu Offcanvas -->
<div class="offcanvas offcanvas-start" tabindex="-1" id="mobileMenu">
  <div class="offcanvas-header border-bottom">
    <img src="/static/main/logos/Vector.webp" alt="Kapi Today" height="40">
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <nav class="mobile-nav-links d-flex flex-column gap-3">
        <a href="/shop">Shop</a>
        <a href="/origins">Origins</a>
        <a href="/learn">Learn</a>
        <a href="/about">Our Story</a>
        <a href="/journal">Journal</a>
        <hr>
        {% if request.user.is_authenticated %}
        <a href="/my-orders/">My Account</a>
        <a href="/support/">Support</a>
        <a href="{% url 'logout' %}" class="text-danger">Logout</a>
        {% else %}
        <a href="{% url 'login' %}">Login / Register</a>
        {% endif %}
    </nav>
  </div>
</div>
"""
with open(os.path.join(BASE_DIR, 'template/main/components/header.html'), 'w') as f:
    f.write(header_html)


print("Header and Announcement components created.")
