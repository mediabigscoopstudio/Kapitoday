import os

BASE_DIR = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday'

# 1. roast_spectrum.html
roast_html = """
<section class="kapi-roast-spectrum py-5 text-white" style="background-color: var(--kapi-espresso);">
    <div class="container py-5">
        <div class="row">
            <div class="col-lg-4 mb-5 mb-lg-0">
                <div class="text-gold text-uppercase fw-bold mb-3" style="letter-spacing: 1.5px; font-size: 0.8rem;">FIND YOUR FLAVOR</div>
                <h2 class="display-4 fw-bold mb-4" style="font-family: var(--font-heading);">The Roast<br>Spectrum</h2>
                <p class="mb-5 text-white-50" style="line-height: 1.8;">From light and bright to dark and bold, explore roasts crafted for every mood and moment.</p>
                <a href="/shop" class="btn btn-outline-light rounded-pill px-4 py-2" style="color: var(--kapi-gold-accent); border-color: var(--kapi-gold-accent);">Learn About Roasts &rarr;</a>
            </div>
            <div class="col-lg-7 offset-lg-1">
                <div class="d-flex flex-column gap-3">
                    <a href="/shop?roast=light" class="roast-card text-decoration-none text-white p-4 rounded-4 d-flex align-items-center justify-content-between" style="background: linear-gradient(to right, rgba(255,255,255,0.05), rgba(255,255,255,0.01)); border: 1px solid rgba(255,255,255,0.1);">
                        <div class="d-flex align-items-center gap-4">
                            <div class="roast-bean" style="width: 60px; height: 60px; border-radius: 50%; background: #c8882a;"></div>
                            <div>
                                <h4 class="mb-1" style="font-family: var(--font-heading);">Light Roast</h4>
                                <p class="mb-0 text-white-50 small">Bright, fruity and vibrant. Discover the origin.</p>
                            </div>
                        </div>
                        <i class="bi bi-arrow-right text-gold fs-4"></i>
                    </a>
                    
                    <a href="/shop?roast=medium" class="roast-card text-decoration-none text-white p-4 rounded-4 d-flex align-items-center justify-content-between" style="background: linear-gradient(to right, rgba(255,255,255,0.05), rgba(255,255,255,0.01)); border: 1px solid rgba(255,255,255,0.1);">
                        <div class="d-flex align-items-center gap-4">
                            <div class="roast-bean" style="width: 60px; height: 60px; border-radius: 50%; background: #8B4513;"></div>
                            <div>
                                <h4 class="mb-1" style="font-family: var(--font-heading);">Medium Roast</h4>
                                <p class="mb-0 text-white-50 small">Balanced, smooth and versatile.</p>
                            </div>
                        </div>
                        <i class="bi bi-arrow-right text-gold fs-4"></i>
                    </a>
                    
                    <a href="/shop?roast=dark" class="roast-card text-decoration-none text-white p-4 rounded-4 d-flex align-items-center justify-content-between" style="background: linear-gradient(to right, rgba(255,255,255,0.05), rgba(255,255,255,0.01)); border: 1px solid rgba(255,255,255,0.1);">
                        <div class="d-flex align-items-center gap-4">
                            <div class="roast-bean" style="width: 60px; height: 60px; border-radius: 50%; background: #3E2218;"></div>
                            <div>
                                <h4 class="mb-1" style="font-family: var(--font-heading);">Dark Roast</h4>
                                <p class="mb-0 text-white-50 small">Bold, rich and full-bodied.</p>
                            </div>
                        </div>
                        <i class="bi bi-arrow-right text-gold fs-4"></i>
                    </a>
                    
                    <a href="/shop?roast=monsoon" class="roast-card text-decoration-none text-white p-4 rounded-4 d-flex align-items-center justify-content-between" style="background: linear-gradient(to right, rgba(255,255,255,0.05), rgba(255,255,255,0.01)); border: 1px solid rgba(255,255,255,0.1);">
                        <div class="d-flex align-items-center gap-4">
                            <div class="roast-bean" style="width: 60px; height: 60px; border-radius: 50%; background: #D4C4AA;"></div>
                            <div>
                                <h4 class="mb-1" style="font-family: var(--font-heading);">Monsoon Malabar</h4>
                                <p class="mb-0 text-white-50 small">Unique, low acidity and earthy.</p>
                            </div>
                        </div>
                        <i class="bi bi-arrow-right text-gold fs-4"></i>
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>
"""
with open(os.path.join(BASE_DIR, 'template/main/components/roast_spectrum.html'), 'w') as f:
    f.write(roast_html)

# 2. brew_methods.html
brew_html = """
<section class="kapi-brew-methods py-5" style="background-color: var(--kapi-cream, #FAF6F0);">
    <div class="container py-5">
        <div class="text-center mb-5">
            <div class="text-gold text-uppercase fw-bold mb-3" style="letter-spacing: 1.5px; font-size: 0.8rem;">BREW BETTER</div>
            <h2 class="display-5 fw-bold mb-3" style="font-family: var(--font-heading); color: var(--kapi-espresso);">Ways to Brew Kapi</h2>
            <p class="text-muted mx-auto" style="max-width: 500px;">Different methods. Different flavours. Same great coffee.</p>
        </div>
        
        <div class="row g-4">
            <!-- Method 1 -->
            <div class="col-12 col-md-6 col-lg-3">
                <div class="card h-100 border-0 bg-transparent text-center brew-card">
                    <img src="/static/main/images/home/filter-brew.webp" class="card-img-top rounded-4 mb-3 object-fit-cover" alt="South Indian Filter" style="height: 250px; background: #EBE0D0;">
                    <h5 class="fw-bold" style="color: var(--kapi-espresso);">South Indian Filter</h5>
                    <p class="text-muted small mb-3">Traditional & Timeless</p>
                    <a href="/learn" class="text-gold text-decoration-none fw-bold small">Learn &rarr;</a>
                </div>
            </div>
            <!-- Method 2 -->
            <div class="col-12 col-md-6 col-lg-3">
                <div class="card h-100 border-0 bg-transparent text-center brew-card">
                    <img src="/static/main/images/home/pour-over.webp" class="card-img-top rounded-4 mb-3 object-fit-cover" alt="Pour Over" style="height: 250px; background: #EBE0D0;">
                    <h5 class="fw-bold" style="color: var(--kapi-espresso);">Pour Over</h5>
                    <p class="text-muted small mb-3">Clean & Flavorful</p>
                    <a href="/learn" class="text-gold text-decoration-none fw-bold small">Learn &rarr;</a>
                </div>
            </div>
            <!-- Method 3 -->
            <div class="col-12 col-md-6 col-lg-3">
                <div class="card h-100 border-0 bg-transparent text-center brew-card">
                    <img src="/static/main/images/home/french-press.webp" class="card-img-top rounded-4 mb-3 object-fit-cover" alt="French Press" style="height: 250px; background: #EBE0D0;">
                    <h5 class="fw-bold" style="color: var(--kapi-espresso);">French Press</h5>
                    <p class="text-muted small mb-3">Bold & Full-bodied</p>
                    <a href="/learn" class="text-gold text-decoration-none fw-bold small">Learn &rarr;</a>
                </div>
            </div>
            <!-- Method 4 -->
            <div class="col-12 col-md-6 col-lg-3">
                <div class="card h-100 border-0 bg-transparent text-center brew-card">
                    <img src="/static/main/images/home/cold-brew.webp" class="card-img-top rounded-4 mb-3 object-fit-cover" alt="Cold Brew" style="height: 250px; background: #EBE0D0;">
                    <h5 class="fw-bold" style="color: var(--kapi-espresso);">Cold Brew</h5>
                    <p class="text-muted small mb-3">Smooth & Refreshing</p>
                    <a href="/learn" class="text-gold text-decoration-none fw-bold small">Learn &rarr;</a>
                </div>
            </div>
        </div>
        
        <div class="text-center mt-5">
            <a href="/learn" class="btn btn-outline-dark rounded-pill px-4 py-2" style="border-color: var(--kapi-espresso); color: var(--kapi-espresso);">Complete Brewing Guide &rarr;</a>
        </div>
    </div>
</section>
"""
with open(os.path.join(BASE_DIR, 'template/main/components/brew_methods.html'), 'w') as f:
    f.write(brew_html)

# 3. origins_video.html
origins_html = """
<section class="kapi-origins-video position-relative" style="background-color: var(--kapi-plantation-dark, #1B3A28); color: #fff; overflow: hidden; min-height: 600px;">
    <!-- Background Video / Image -->
    <picture>
        <source media="(max-width: 767px)" srcset="/static/main/images/home/origins-poster.webp">
        <img src="/static/main/images/home/origins-poster.webp" alt="Western Ghats Coffee Origins" class="position-absolute w-100 h-100 object-fit-cover opacity-50 z-1" loading="lazy">
    </picture>
    <video autoplay loop muted playsinline class="position-absolute w-100 h-100 object-fit-cover opacity-50 z-1 d-none d-md-block" style="pointer-events: none;" preload="none" id="originsVideo">
        <source src="/static/main/images/home/origins.mp4" type="video/mp4">
    </video>
    
    <div class="position-absolute w-100 h-100 z-2" style="background: linear-gradient(to right, rgba(27,58,40,0.9) 0%, rgba(27,58,40,0.6) 50%, rgba(27,58,40,0.2) 100%);"></div>

    <div class="container position-relative z-3 py-5 h-100 d-flex flex-column justify-content-center" style="min-height: 600px;">
        <div class="row">
            <div class="col-lg-6">
                <div class="text-gold text-uppercase fw-bold mb-3" style="letter-spacing: 1.5px; font-size: 0.8rem;">OUR ORIGINS</div>
                <h2 class="display-4 fw-bold mb-4" style="font-family: var(--font-heading);">From the Mist-Covered<br>Slopes of the<br>Western Ghats</h2>
                <p class="mb-5 text-white-50 fs-5" style="line-height: 1.6; max-width: 480px;">
                    Our coffee comes from small farms, rich soils and people who have nurtured this land for generations. Taste a richer, more meaningful cup.
                </p>
                
                <div class="row g-4 mb-5">
                    <div class="col-4">
                        <div class="text-gold fw-bold display-6">5</div>
                        <div class="text-white-50 small text-uppercase">Regions</div>
                    </div>
                    <div class="col-4">
                        <div class="text-gold fw-bold display-6">1,200+</div>
                        <div class="text-white-50 small text-uppercase">Smallholder Farmers</div>
                    </div>
                    <div class="col-4">
                        <div class="text-gold fw-bold display-6">100%</div>
                        <div class="text-white-50 small text-uppercase">Indian Grown</div>
                    </div>
                </div>
                
                <a href="/about" class="btn btn-warning rounded-pill px-4 py-3 fw-bold" style="background-color: var(--kapi-gold-accent); border: none; color: var(--kapi-espresso);">
                    <i class="bi bi-play-fill fs-5 align-middle me-1"></i> Watch Our Story &rarr;
                </a>
            </div>
            
            <div class="col-lg-5 offset-lg-1 d-none d-lg-flex flex-column justify-content-center">
                <ul class="list-unstyled d-flex flex-column gap-4 mt-5">
                    <li class="d-flex align-items-center gap-3">
                        <i class="bi bi-check-circle-fill text-gold fs-4"></i>
                        <span class="fs-5 fw-bold">Sustainable Farming</span>
                    </li>
                    <li class="d-flex align-items-center gap-3">
                        <i class="bi bi-check-circle-fill text-gold fs-4"></i>
                        <span class="fs-5 fw-bold">Fair Trade Practices</span>
                    </li>
                    <li class="d-flex align-items-center gap-3">
                        <i class="bi bi-check-circle-fill text-gold fs-4"></i>
                        <span class="fs-5 fw-bold">Supporting Local Communities</span>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</section>
"""
with open(os.path.join(BASE_DIR, 'template/main/components/origins_video.html'), 'w') as f:
    f.write(origins_html)

print("Stage 6-8 components created.")
