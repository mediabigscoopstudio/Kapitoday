import os

BASE_DIR = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday'

# 1. testimonials.html
testimonials_html = """
<section class="kapi-testimonials py-5" style="background-color: var(--kapi-cream-warm, #F5EDE0);">
    <div class="container py-5">
        <div class="text-center mb-5">
            <div class="text-gold text-uppercase fw-bold mb-3" style="letter-spacing: 1.5px; font-size: 0.8rem;">LOVED BY COFFEE ENTHUSIASTS</div>
            <h2 class="display-5 fw-bold mb-3" style="font-family: var(--font-heading); color: var(--kapi-espresso);">What Our Sippers Say</h2>
        </div>
        
        <div class="row g-4">
            <div class="col-md-4">
                <div class="card h-100 border-0 p-4 rounded-4 shadow-sm">
                    <div class="text-warning mb-3">★★★★★</div>
                    <p class="fst-italic text-muted mb-4">"The Araku Valley coffee tastes just like the filter coffee I had in my grandmother's house. Incredible quality!"</p>
                    <div class="d-flex align-items-center gap-3 mt-auto">
                        <div class="rounded-circle bg-secondary" style="width: 40px; height: 40px; background-image: url('https://i.pravatar.cc/100?img=11'); background-size: cover;"></div>
                        <div>
                            <div class="fw-bold" style="color: var(--kapi-espresso); font-size: 0.9rem;">Rohan S.</div>
                            <div class="text-muted small">Bengaluru</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card h-100 border-0 p-4 rounded-4 shadow-sm">
                    <div class="text-warning mb-3">★★★★★</div>
                    <p class="fst-italic text-muted mb-4">"Finally an Indian coffee brand that feels premium and authentic. The packaging, flavour and story - everything is top notch."</p>
                    <div class="d-flex align-items-center gap-3 mt-auto">
                        <div class="rounded-circle bg-secondary" style="width: 40px; height: 40px; background-image: url('https://i.pravatar.cc/100?img=5'); background-size: cover;"></div>
                        <div>
                            <div class="fw-bold" style="color: var(--kapi-espresso); font-size: 0.9rem;">Ananya K.</div>
                            <div class="text-muted small">Delhi</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card h-100 border-0 p-4 rounded-4 shadow-sm">
                    <div class="text-warning mb-3">★★★★★</div>
                    <p class="fst-italic text-muted mb-4">"The best coffee I've had in a long time. You can truly taste the difference."</p>
                    <div class="d-flex align-items-center gap-3 mt-auto">
                        <div class="rounded-circle bg-secondary" style="width: 40px; height: 40px; background-image: url('https://i.pravatar.cc/100?img=12'); background-size: cover;"></div>
                        <div>
                            <div class="fw-bold" style="color: var(--kapi-espresso); font-size: 0.9rem;">Vikram M.</div>
                            <div class="text-muted small">Mumbai</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
"""
with open(os.path.join(BASE_DIR, 'template/main/components/testimonials.html'), 'w') as f:
    f.write(testimonials_html)

# 2. community.html
community_html = """
<section class="kapi-community bg-dark text-white py-5" style="background-color: #111 !important;">
    <div class="container-fluid py-4">
        <div class="row align-items-center mb-4 px-4">
            <div class="col-md-4 mb-4 mb-md-0">
                <div class="text-gold text-uppercase fw-bold mb-2" style="letter-spacing: 1.5px; font-size: 0.8rem;">A COMMUNITY</div>
                <h2 class="display-6 fw-bold mb-3" style="font-family: var(--font-heading);">That Lives<br>and Brews Kapi</h2>
                <a href="#" class="btn btn-outline-light rounded-pill px-4">Follow @kapitoday &rarr;</a>
            </div>
            <div class="col-md-8">
                <div class="d-flex gap-3 overflow-auto" style="scrollbar-width: none; padding-bottom: 10px;">
                    <img src="/static/main/images/home/community-01.webp" alt="Community 1" class="rounded-4 object-fit-cover" style="width: 200px; height: 200px; flex-shrink: 0; background: #333;">
                    <img src="/static/main/images/home/community-02.webp" alt="Community 2" class="rounded-4 object-fit-cover" style="width: 200px; height: 200px; flex-shrink: 0; background: #333;">
                    <img src="/static/main/images/home/community-03.webp" alt="Community 3" class="rounded-4 object-fit-cover" style="width: 200px; height: 200px; flex-shrink: 0; background: #333;">
                    <img src="/static/main/images/home/community-04.webp" alt="Community 4" class="rounded-4 object-fit-cover" style="width: 200px; height: 200px; flex-shrink: 0; background: #333;">
                    <img src="/static/main/images/home/community-05.webp" alt="Community 5" class="rounded-4 object-fit-cover" style="width: 200px; height: 200px; flex-shrink: 0; background: #333;">
                </div>
            </div>
        </div>
    </div>
</section>
"""
with open(os.path.join(BASE_DIR, 'template/main/components/community.html'), 'w') as f:
    f.write(community_html)

# 3. newsletter.html
newsletter_html = """
<section class="kapi-newsletter text-center py-5 position-relative" style="background-color: var(--kapi-red-oxide, #8B3A2A); color: #fff;">
    <!-- Add some faint background texture if available -->
    <div class="container py-5 position-relative z-2">
        <div class="text-gold text-uppercase fw-bold mb-3" style="letter-spacing: 1.5px; font-size: 0.8rem;">JOIN THE KAPI CULTURE</div>
        <h2 class="display-4 fw-bold mb-4" style="font-family: var(--font-heading);">Good Coffee.<br>Brighter Days.</h2>
        <p class="mb-4 mx-auto text-white-50" style="max-width: 500px;">
            Get updates on new harvests, brewing tips, exclusive offers and stories from our plantations.
        </p>
        
        <form class="d-flex mx-auto position-relative" style="max-width: 400px;">
            <i class="bi bi-envelope position-absolute top-50 translate-middle-y ms-3 text-muted"></i>
            <input type="email" class="form-control rounded-pill ps-5 py-3 border-0 bg-white" placeholder="Enter your email address" required>
            <button class="btn btn-warning rounded-pill position-absolute top-0 end-0 h-100 px-4 fw-bold" style="background-color: var(--kapi-gold-accent); border: none; color: var(--kapi-espresso);">Subscribe</button>
        </form>
    </div>
</section>
"""
with open(os.path.join(BASE_DIR, 'template/main/components/newsletter.html'), 'w') as f:
    f.write(newsletter_html)

# 4. footer.html
footer_html = """
<footer class="kapi-footer py-5" style="background-color: var(--kapi-espresso, #2C1810); color: #fff;">
    <div class="container py-4">
        <div class="row g-4">
            <div class="col-lg-4 mb-4 mb-lg-0">
                <img src="/static/main/logos/Vector.webp" alt="Kapi Today" height="50" class="mb-3" style="filter: brightness(0) invert(1);">
                <p class="text-gold fw-bold mb-4" style="font-family: var(--font-heading); font-style: italic;">From South India to the World.</p>
                <div class="d-flex gap-3">
                    <a href="#" class="text-white-50 text-decoration-none fs-5 hover-gold"><i class="bi bi-instagram"></i></a>
                    <a href="#" class="text-white-50 text-decoration-none fs-5 hover-gold"><i class="bi bi-youtube"></i></a>
                    <a href="#" class="text-white-50 text-decoration-none fs-5 hover-gold"><i class="bi bi-linkedin"></i></a>
                    <a href="#" class="text-white-50 text-decoration-none fs-5 hover-gold"><i class="bi bi-twitter-x"></i></a>
                </div>
            </div>
            
            <div class="col-6 col-lg-2 offset-lg-1">
                <h6 class="text-uppercase fw-bold mb-4 text-white">Shop</h6>
                <ul class="list-unstyled d-flex flex-column gap-2 small text-white-50">
                    <li><a href="/shop" class="text-decoration-none text-white-50 hover-white">All Coffee</a></li>
                    <li><a href="/shop?category=single-origin" class="text-decoration-none text-white-50 hover-white">Single Origin</a></li>
                    <li><a href="/shop?category=instant" class="text-decoration-none text-white-50 hover-white">Instant Coffee</a></li>
                    <li><a href="/shop?category=nespresso" class="text-decoration-none text-white-50 hover-white">Nespresso Pods</a></li>
                    <li><a href="/shop?category=equipment" class="text-decoration-none text-white-50 hover-white">Equipment</a></li>
                </ul>
            </div>
            
            <div class="col-6 col-lg-2">
                <h6 class="text-uppercase fw-bold mb-4 text-white">About</h6>
                <ul class="list-unstyled d-flex flex-column gap-2 small text-white-50">
                    <li><a href="/about" class="text-decoration-none text-white-50 hover-white">Our Story</a></li>
                    <li><a href="/about#plantations" class="text-decoration-none text-white-50 hover-white">Our Plantations</a></li>
                    <li><a href="/about#farmers" class="text-decoration-none text-white-50 hover-white">Our Farmers</a></li>
                    <li><a href="/sustainability" class="text-decoration-none text-white-50 hover-white">Sustainability</a></li>
                    <li><a href="/journal" class="text-decoration-none text-white-50 hover-white">Journal</a></li>
                </ul>
            </div>
            
            <div class="col-6 col-lg-2">
                <h6 class="text-uppercase fw-bold mb-4 text-white">Support</h6>
                <ul class="list-unstyled d-flex flex-column gap-2 small text-white-50">
                    <li><a href="/shipping" class="text-decoration-none text-white-50 hover-white">Shipping</a></li>
                    <li><a href="/returns" class="text-decoration-none text-white-50 hover-white">Returns</a></li>
                    <li><a href="/faq" class="text-decoration-none text-white-50 hover-white">FAQs</a></li>
                    <li><a href="/track" class="text-decoration-none text-white-50 hover-white">Track Order</a></li>
                    <li><a href="/wholesale" class="text-decoration-none text-white-50 hover-white">Wholesale</a></li>
                    <li><a href="/support" class="text-decoration-none text-white-50 hover-white">Help Center</a></li>
                </ul>
            </div>
        </div>
        
        <hr class="border-secondary my-5">
        
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-center small text-white-50">
            <p class="mb-2 mb-md-0">&copy; 2026 Kapi Today. All rights reserved.</p>
            <div class="d-flex gap-4">
                <a href="/privacy" class="text-decoration-none text-white-50 hover-white">Privacy Policy</a>
                <a href="/terms" class="text-decoration-none text-white-50 hover-white">Terms & Conditions</a>
                <span>Made in India 🇮🇳</span>
            </div>
        </div>
    </div>
</footer>
"""
with open(os.path.join(BASE_DIR, 'template/main/components/footer.html'), 'w') as f:
    f.write(footer_html)

print("Stage 9-11 components created.")
