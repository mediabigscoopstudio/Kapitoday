import re

filepath = '/Volumes/Juggernut_Assist/Projects/Kapi/Kapitoday/template/main/base.html'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the single button with the dual buttons
old_btn = """<button id="fc-cta-btn" onclick="fcNextStep()" style="display:block; width:100%; background:#a67c52; color:#fff; text-align:center; padding:15px; border-radius:8px; font-weight:700; font-size:1.1rem; border:none; margin-top:15px; cursor:pointer;">Continue to Login &rarr;</button>"""

new_btn = """<div style="display:flex; gap:10px; margin-top:15px;">
                <button id="fc-back-btn" onclick="fcPrevStep()" style="display:none; width:30%; background:#f4f4f4; color:#555; text-align:center; padding:15px; border-radius:8px; font-weight:700; font-size:1rem; border:1px solid #ddd; cursor:pointer;">&larr; Back</button>
                <button id="fc-cta-btn" onclick="fcNextStep()" style="flex:1; background:#a67c52; color:#fff; text-align:center; padding:15px; border-radius:8px; font-weight:700; font-size:1.1rem; border:none; cursor:pointer;">Continue to Login &rarr;</button>
            </div>"""

content = content.replace(old_btn, new_btn)

# Add fcPrevStep and update fcRenderStepCTA
old_render = """    function fcRenderStepCTA() {
        let btn = document.getElementById('fc-cta-btn');"""
new_render = """    function fcPrevStep() {
        if(fcState.step === 'address') fcSetStep('cart');
        else if(fcState.step === 'offers') fcSetStep('address');
        else if(fcState.step === 'payment') fcSetStep('offers'); // Although payment triggers Razorpay directly
    }
    
    function fcRenderStepCTA() {
        let btn = document.getElementById('fc-cta-btn');
        let backBtn = document.getElementById('fc-back-btn');"""

content = content.replace(old_render, new_render)

old_states = """        if(fcState.step === 'cart') {
            btn.innerHTML = fcState.isAuthenticated ? 'Continue to Address &rarr;' : 'Continue to Login &rarr;';
        } else if(fcState.step === 'login') {
            document.getElementById('fcFooter').style.display = 'none';
        } else if(fcState.step === 'address') {
            document.getElementById('fcFooter').style.display = 'block';
            btn.innerHTML = 'Continue to Offers &rarr;';
        } else if(fcState.step === 'offers') {
            document.getElementById('fcFooter').style.display = 'block';
            btn.innerHTML = 'Proceed to Payment &rarr;';
        }"""
new_states = """        if(fcState.step === 'cart') {
            btn.innerHTML = fcState.isAuthenticated ? 'Continue to Address &rarr;' : 'Continue to Login &rarr;';
            if(backBtn) backBtn.style.display = 'none';
        } else if(fcState.step === 'login') {
            document.getElementById('fcFooter').style.display = 'none';
        } else if(fcState.step === 'address') {
            document.getElementById('fcFooter').style.display = 'block';
            btn.innerHTML = 'Continue to Offers &rarr;';
            if(backBtn) backBtn.style.display = 'block';
        } else if(fcState.step === 'offers') {
            document.getElementById('fcFooter').style.display = 'block';
            btn.innerHTML = 'Proceed to Payment &rarr;';
            if(backBtn) backBtn.style.display = 'block';
        }"""
content = content.replace(old_states, new_states)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched base footer navigation.")
