import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

# Replace targets
content = content.replace('data-bs-target="#cartDrawer"', 'data-bs-target="#fastCheckoutDrawer"')
content = content.replace('aria-labelledby="cartDrawerLabel"', 'aria-labelledby="fcDrawerLabel"')

# Inject CSS link
css_tag = '<link rel="stylesheet" href="{% static \'main/css/checkout.css\' %}">'
if css_tag not in content:
    content = content.replace("{% block 'css' %}{% endblock 'css' %}", "{% block 'css' %}{% endblock 'css' %}\n  " + css_tag)

# Replace the Drawer HTML
old_drawer_regex = re.compile(r'<div class="offcanvas offcanvas-end cart-drawer".*?</div>\s*</div>\s*<!-- ============================', re.DOTALL)

new_drawer = """<!-- FAST CHECKOUT DRAWER -->
    <div class="offcanvas offcanvas-end" tabindex="-1" id="fastCheckoutDrawer" aria-labelledby="fcDrawerLabel" style="width: 100%; max-width: 500px; border-left: none; box-shadow: -5px 0 25px rgba(0,0,0,0.1); background-color: #fdfaf4;">
        
        <!-- Header & Progress -->
        <div style="background: #3A2A1D; color: #fff;">
            <div style="padding: 15px 20px; display: flex; justify-content: space-between; align-items: center;">
                <h5 style="margin: 0; font-family: serif; font-size: 1.2rem;">Kapi Today Checkout</h5>
                <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close" style="filter: invert(1); opacity: 0.8;"></button>
            </div>
            <div id="fcProgress" style="display: flex; background: #4a3625; padding: 10px 20px; font-size: 0.75rem; color: rgba(255,255,255,0.6); justify-content: space-between;">
                <span class="fc-pstep active" id="fc-ps-cart">Cart</span> →
                <span class="fc-pstep" id="fc-ps-address">Address</span> →
                <span class="fc-pstep" id="fc-ps-offers">Offers</span> →
                <span class="fc-pstep" id="fc-ps-payment">Payment</span>
            </div>
        </div>

        <div class="fc-body" id="fcBody" style="padding: 0; overflow-y: auto; overflow-x: hidden; display: flex; flex-direction: column; flex: 1;">
            
            <!-- STEP 1: CART -->
            <div id="fc-step-cart" class="fc-step-container active" style="padding: 20px; display:block;">
                <div id="fc-cart-items-container">
                    {% include 'main/partials/fc_cart_items.html' %}
                </div>
            </div>

            <!-- STEP 2: LOGIN -->
            <div id="fc-step-login" class="fc-step-container" style="padding: 20px; display:none; text-align:center;">
                <h3 style="font-family: serif; color: #3A2A1D; margin-bottom: 15px; margin-top:20px;">Welcome to Kapi Today</h3>
                <p style="color:#666; font-size:0.9rem;">Log in to view your saved addresses, orders and exclusive offers.</p>
                <div id="fcGoogleBtnContainer" style="margin-top: 30px; display: flex; justify-content: center;">
                    <!-- Google button renders here -->
                </div>
            </div>

            <!-- STEP 3: ADDRESS -->
            <div id="fc-step-address" class="fc-step-container" style="padding: 20px; display:none;">
                <h6 style="font-weight:700; color:#3A2A1D; margin-bottom:15px;">Deliver To</h6>
                <div id="fc-address-list"></div>
                <hr style="border:0; border-top:1px dashed #ddd; margin: 20px 0;">
                <h6 style="font-weight:700; color:#3A2A1D; margin-bottom:15px;">Add New Address</h6>
                <form id="fc-address-form">
                    <div style="margin-bottom: 10px;">
                        <input type="text" id="fc-name" class="form-control" placeholder="Full Name" required>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <input type="text" id="fc-line1" class="form-control" placeholder="House No, Building, Street" required>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <input type="text" id="fc-line2" class="form-control" placeholder="Locality / Landmark">
                    </div>
                    <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                        <input type="text" id="fc-city" class="form-control" placeholder="City" required>
                        <input type="text" id="fc-state" class="form-control" placeholder="State" required>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <input type="text" id="fc-pin" class="form-control" placeholder="Pincode" required pattern="[0-9]{6}">
                    </div>
                </form>
            </div>

            <!-- STEP 4: OFFERS -->
            <div id="fc-step-offers" class="fc-step-container" style="padding: 20px; display:none;">
                <h6 style="font-weight:700; color:#3A2A1D; margin-bottom:15px;">Available Offers</h6>
                
                <div style="display:flex; gap:10px; margin-bottom:20px;">
                    <input type="text" id="fc-coupon-input" class="form-control" placeholder="Enter coupon code">
                    <button onclick="fcApplyCoupon()" style="background:#333; color:#fff; border:none; border-radius:6px; padding:0 20px; font-weight:600;">Apply</button>
                </div>
                
                <div id="fc-applied-coupon-msg" style="display:none; background:#e8f5e9; padding:10px 15px; border-radius:6px; border:1px dashed #4caf50; margin-bottom:20px; align-items:center; justify-content:space-between;">
                    <span style="color:#2e7d32; font-weight:600;"><i class="bi bi-tag-fill"></i> <span id="fc-applied-code"></span></span>
                    <button onclick="fcRemoveCoupon()" style="background:none; border:none; color:#d32f2f; cursor:pointer; font-weight:bold;">Remove</button>
                </div>
                
                <div id="fc-offers-list"></div>
            </div>

            <!-- STEP 5: CONFIRMATION -->
            <div id="fc-step-success" class="fc-step-container" style="padding: 40px 20px; display:none; text-align:center;">
                <i class="bi bi-check-circle-fill" style="font-size:4rem; color:#2e7d32;"></i>
                <h3 style="font-family:serif; color:#3A2A1D; margin-top:20px;">Order Placed!</h3>
                <p style="color:#666;">Order #<span id="fc-success-id"></span></p>
                <div style="margin-top:30px; text-align:left; background:#fff; padding:20px; border-radius:8px; border:1px solid #eee;">
                    <p style="margin-bottom:10px;"><i class="bi bi-check-circle-fill" style="color:#2e7d32; margin-right:8px;"></i> Order Confirmed</p>
                    <p style="margin-bottom:10px; color:#aaa;"><i class="bi bi-circle" style="margin-right:8px;"></i> Preparing</p>
                    <p style="color:#aaa; margin:0;"><i class="bi bi-circle" style="margin-right:8px;"></i> Out for Delivery</p>
                </div>
                <button onclick="window.location.reload()" style="background:#3A2A1D; color:#fff; border:none; padding:12px 30px; border-radius:25px; margin-top:30px; font-weight:bold; width:100%;">Continue Shopping</button>
            </div>
            
        </div>
        
        <!-- Sticky Footer -->
        <div class="fc-footer" id="fcFooter" style="padding: 15px 20px; background: #fff; border-top: 1px solid #eee; box-shadow: 0 -2px 10px rgba(0,0,0,0.05); display:none;">
            <div style="display:flex; justify-content:space-between; font-size:0.9rem; color:#555; margin-bottom:5px;">
                <span>Item Total</span><span id="fc-subtotal">₹0</span>
            </div>
            <div id="fc-discount-row" style="display:none; justify-content:space-between; font-size:0.9rem; color:#2e7d32; font-weight:500; margin-bottom:5px;">
                <span>Discount</span><span id="fc-discount">-₹0</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.9rem; color:#555; margin-bottom:10px;">
                <span>Shipping</span><span id="fc-shipping">₹0</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:1.1rem; font-weight:700; color:#3A2A1D; border-top:1px dashed #ddd; padding-top:10px;">
                <span>Total</span><span id="fc-total">₹0</span>
            </div>
            <button id="fc-cta-btn" onclick="fcNextStep()" style="display:block; width:100%; background:#a67c52; color:#fff; text-align:center; padding:15px; border-radius:8px; font-weight:700; font-size:1.1rem; border:none; margin-top:15px; cursor:pointer;">Continue to Login &rarr;</button>
        </div>

    </div>
    
    <!-- ============================"""

content = re.sub(old_drawer_regex, new_drawer, content)

# Also, we need to inject the script block for FC logic
js_injection = """
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
<script>
    // Fast Checkout State
    let fcState = {
        step: 'cart',
        isAuthenticated: false,
        cartCount: 0,
        subtotal: 0,
        discount: 0,
        appliedCoupon: null,
        shipping: 0,
        total: 0,
        pastAddresses: [],
        availableOffers: [],
        selectedAddress: null
    };
    
    document.addEventListener('DOMContentLoaded', function() {
        const drawerEl = document.getElementById('fastCheckoutDrawer');
        drawerEl.addEventListener('show.bs.offcanvas', function () {
            fcFetchState();
        });
        
        // Ensure Google Script renders the button
        if(typeof google !== 'undefined' && google.accounts) {
            google.accounts.id.renderButton(
                document.getElementById('fcGoogleBtnContainer'),
                { theme: 'outline', size: 'large', shape: 'pill', width: 280 }
            );
        }
    });
    
    function fcFetchState() {
        fetch('/api/fc/state/')
        .then(r => r.json())
        .then(data => {
            if(data.success) {
                fcUpdateUI(data);
            }
        });
    }
    
    function updateCartItem(id, action) {
        fetch('/api/fc/cart/update/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({item_id: id, action: action})
        }).then(r => r.json()).then(data => {
            if(data.success) fcUpdateUI(data);
        });
    }
    
    function fcApplyCoupon(code = null) {
        if(!code) code = document.getElementById('fc-coupon-input').value;
        fetch('/api/fc/coupon/apply/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({code: code, action: 'apply'})
        }).then(r => r.json()).then(data => {
            if(data.success) {
                fcUpdateUI(data);
            } else {
                Swal.fire('Error', data.error, 'error');
            }
        });
    }
    
    function fcRemoveCoupon() {
        fetch('/api/fc/coupon/apply/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action: 'remove'})
        }).then(r => r.json()).then(data => {
            if(data.success) fcUpdateUI(data);
        });
    }
    
    function fcUpdateUI(data) {
        fcState.isAuthenticated = data.is_authenticated;
        fcState.cartCount = data.cart_count;
        fcState.subtotal = data.subtotal;
        fcState.discount = data.discount;
        fcState.appliedCoupon = data.applied_coupon;
        fcState.shipping = data.shipping_charge;
        fcState.total = data.total;
        fcState.pastAddresses = data.past_addresses;
        fcState.availableOffers = data.available_offers;
        
        // Update header cart counters everywhere
        document.querySelectorAll('.cart-count, .cart-title-count').forEach(el => el.innerText = fcState.cartCount);
        
        // Update Cart HTML
        document.getElementById('fc-cart-items-container').innerHTML = data.cart_html;
        
        if (fcState.cartCount === 0) {
            document.getElementById('fcFooter').style.display = 'none';
        } else {
            document.getElementById('fcFooter').style.display = 'block';
            document.getElementById('fc-subtotal').innerText = '₹' + fcState.subtotal;
            document.getElementById('fc-shipping').innerText = fcState.shipping === 0 ? 'FREE' : '₹' + fcState.shipping;
            document.getElementById('fc-total').innerText = '₹' + fcState.total;
            
            if(fcState.discount > 0) {
                document.getElementById('fc-discount-row').style.display = 'flex';
                document.getElementById('fc-discount').innerText = '-₹' + fcState.discount;
            } else {
                document.getElementById('fc-discount-row').style.display = 'none';
            }
        }
        
        // Update Offers List
        let offersHtml = '';
        fcState.availableOffers.forEach(o => {
            offersHtml += `
            <div class="fc-offer-card" onclick="fcApplyCoupon('${o.code}')" style="background:#fffaf0; border:2px dashed #d4a373; padding:15px; border-radius:8px; margin-bottom:15px; cursor:pointer;">
                <div style="font-weight:800; color:#3A2A1D; margin-bottom:5px;">${o.code}</div>
                <div style="font-size:0.85rem; color:#666;">${o.desc}</div>
            </div>`;
        });
        document.getElementById('fc-offers-list').innerHTML = offersHtml;
        
        if(fcState.appliedCoupon) {
            document.getElementById('fc-applied-coupon-msg').style.display = 'flex';
            document.getElementById('fc-applied-code').innerText = fcState.appliedCoupon;
        } else {
            document.getElementById('fc-applied-coupon-msg').style.display = 'none';
        }
        
        // Update Address List
        if(fcState.pastAddresses.length > 0) {
            let addrHtml = '';
            fcState.pastAddresses.forEach((a, idx) => {
                let j = JSON.stringify(a).replace(/"/g, '&quot;');
                addrHtml += `
                <div class="fc-address-card" id="addr-card-${idx}" onclick="fcSelectAddress(${idx}, ${j})" style="background:#fff; border:1px solid #ddd; padding:15px; border-radius:8px; margin-bottom:15px; cursor:pointer;">
                    <div style="font-weight:700; color:#3A2A1D; margin-bottom:5px;">${a.full_name}</div>
                    <div style="font-size:0.85rem; color:#555;">${a.address_line_1}, ${a.city}, ${a.state} - ${a.pincode}</div>
                </div>`;
            });
            document.getElementById('fc-address-list').innerHTML = addrHtml;
        }
        
        fcRenderStepCTA();
    }
    
    function fcSelectAddress(idx, addr) {
        document.querySelectorAll('.fc-address-card').forEach(el => el.style.borderColor = '#ddd');
        document.getElementById('addr-card-' + idx).style.borderColor = '#a67c52';
        document.getElementById('addr-card-' + idx).style.backgroundColor = '#fdfaf4';
        
        document.getElementById('fc-name').value = addr.full_name;
        document.getElementById('fc-line1').value = addr.address_line_1;
        document.getElementById('fc-line2').value = addr.address_line_2;
        document.getElementById('fc-city').value = addr.city;
        document.getElementById('fc-state').value = addr.state;
        document.getElementById('fc-pin').value = addr.pincode;
    }
    
    function fcSetStep(step) {
        document.querySelectorAll('.fc-step-container').forEach(el => el.style.display = 'none');
        document.getElementById('fc-step-' + step).style.display = 'block';
        fcState.step = step;
        
        // Update progress bar UI
        let steps = ['cart', 'address', 'offers', 'payment'];
        let activeIdx = steps.indexOf(step === 'login' ? 'cart' : step);
        steps.forEach((s, idx) => {
            let el = document.getElementById('fc-ps-' + s);
            if(el) {
                el.className = 'fc-pstep';
                if(idx === activeIdx) el.classList.add('active');
                if(idx < activeIdx) el.classList.add('completed');
            }
        });
        
        fcRenderStepCTA();
    }
    
    function fcRenderStepCTA() {
        let btn = document.getElementById('fc-cta-btn');
        if(fcState.step === 'cart') {
            btn.innerHTML = fcState.isAuthenticated ? 'Continue to Address &rarr;' : 'Continue to Login &rarr;';
        } else if(fcState.step === 'login') {
            document.getElementById('fcFooter').style.display = 'none';
        } else if(fcState.step === 'address') {
            document.getElementById('fcFooter').style.display = 'block';
            btn.innerHTML = 'Continue to Offers &rarr;';
        } else if(fcState.step === 'offers') {
            document.getElementById('fcFooter').style.display = 'block';
            btn.innerHTML = 'Proceed to Payment &rarr;';
        }
    }
    
    function fcNextStep() {
        if(fcState.step === 'cart') {
            if(!fcState.isAuthenticated) fcSetStep('login');
            else fcSetStep('address');
        } else if(fcState.step === 'address') {
            // Validate address
            const form = document.getElementById('fc-address-form');
            if(!form.checkValidity()) {
                form.reportValidity();
                return;
            }
            fcSetStep('offers');
        } else if(fcState.step === 'offers') {
            fcInitiatePayment();
        }
    }
    
    // Wire up progress bar clicking to go backward
    document.querySelectorAll('.fc-pstep').forEach(el => {
        el.addEventListener('click', function() {
            if(this.classList.contains('completed')) {
                let step = this.id.replace('fc-ps-', '');
                fcSetStep(step);
            }
        });
    });
    
    function fcInitiatePayment() {
        let btn = document.getElementById('fc-cta-btn');
        btn.innerHTML = 'Processing...';
        btn.disabled = true;
        
        fetch('/api/fc/payment/init/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        }).then(r => r.json()).then(data => {
            if(data.success) {
                var options = {
                    "key": data.key,
                    "amount": data.amount,
                    "currency": "INR",
                    "name": "Kapi Today",
                    "description": "Fast Checkout",
                    "order_id": data.order_id,
                    "handler": function (response) {
                        fcVerifyPayment(response);
                    },
                    "theme": { "color": "#3A2A1D" }
                };
                var rzp1 = new Razorpay(options);
                rzp1.on('payment.failed', function (response){
                    btn.innerHTML = 'Proceed to Payment &rarr;';
                    btn.disabled = false;
                    Swal.fire('Payment Failed', response.error.description, 'error');
                });
                rzp1.open();
            } else {
                btn.innerHTML = 'Proceed to Payment &rarr;';
                btn.disabled = false;
                Swal.fire('Error', data.error, 'error');
            }
        });
    }
    
    function fcVerifyPayment(rzpResponse) {
        const form = document.getElementById('fc-address-form');
        
        let payload = {
            razorpay_payment_id: rzpResponse.razorpay_payment_id,
            razorpay_order_id: rzpResponse.razorpay_order_id,
            razorpay_signature: rzpResponse.razorpay_signature,
            full_name: form.querySelector('#fc-name').value,
            address_line_1: form.querySelector('#fc-line1').value,
            address_line_2: form.querySelector('#fc-line2').value,
            city: form.querySelector('#fc-city').value,
            state: form.querySelector('#fc-state').value,
            pincode: form.querySelector('#fc-pin').value,
            total_amount: fcState.total
        };
        
        fetch('/api/fc/payment/verify/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        }).then(r => r.json()).then(data => {
            if(data.success) {
                document.getElementById('fcFooter').style.display = 'none';
                document.getElementById('fc-success-id').innerText = data.order_db_id;
                fcSetStep('success');
            } else {
                let btn = document.getElementById('fc-cta-btn');
                btn.innerHTML = 'Proceed to Payment &rarr;';
                btn.disabled = false;
                Swal.fire('Error', 'Payment verification failed: ' + data.error, 'error');
            }
        });
    }

</script>
"""
content = content.replace("</body>", js_injection + "\n</body>")

with open(filepath, 'w') as f:
    f.write(content)

print("Replaced Drawer in base.html successfully.")
