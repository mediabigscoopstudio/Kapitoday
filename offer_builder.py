import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kapitoday.settings')
django.setup()

from dash.models import Offer, Product, Category

def create_offers():
    print("Clearing existing offers...")
    Offer.objects.all().delete()
    
    now = timezone.now()
    next_month = now + timedelta(days=30)
    next_year = now + timedelta(days=365)
    
    offers_created = []

    # 1. WELCOME15 - 15% off first order
    o1 = Offer.objects.create(
        title="Welcome to Kapi Today - 15% Off",
        description="Get 15% off your very first order.",
        trigger='coupon',
        coupon_code='WELCOME15',
        condition_type='first_order',
        action_type='percentage_off',
        discount_value=15.00,
        valid_from=now,
        valid_to=next_year,
        priority=100
    )
    offers_created.append(o1)
    
    # 2. AUTOMATIC FREE SHIPPING OVER ₹999
    o2 = Offer.objects.create(
        title="Free Shipping on Orders over ₹999",
        description="Automatic free shipping when you spend over ₹999.",
        trigger='automatic',
        condition_type='min_order',
        min_order_amount=999.00,
        action_type='free_shipping',
        stackable=True,
        valid_from=now,
        valid_to=next_year,
        priority=90
    )
    offers_created.append(o2)
    
    # 3. KAPI200 - Flat 200 off over 1499
    o3 = Offer.objects.create(
        title="Flat ₹200 Off",
        description="Use code KAPI200 to get ₹200 off on orders above ₹1499.",
        trigger='coupon',
        coupon_code='KAPI200',
        condition_type='min_order',
        min_order_amount=1499.00,
        action_type='flat_off',
        discount_value=200.00,
        valid_from=now,
        valid_to=next_month,
        priority=80
    )
    offers_created.append(o3)

    # 4. BOGO on Dark Roast
    dark_roast_cat = Category.objects.filter(title__icontains="Dark Roast").first()
    if dark_roast_cat:
        o4 = Offer.objects.create(
            title="Buy 1 Get 1 Free on Dark Roasts",
            description="Automatic BOGO on all our Dark Roast coffees.",
            trigger='automatic',
            condition_type='category',
            condition_category=dark_roast_cat,
            action_type='bogo',
            buy_quantity=1,
            get_quantity=1,
            valid_from=now,
            valid_to=now + timedelta(days=7), # Flash sale for 7 days
            priority=70
        )
        offers_created.append(o4)

    # 5. Free Accessory with Araku Valley Medium Roast
    araku_coffee = Product.objects.filter(name__icontains="Araku Valley Medium Roast").first()
    scoop = Product.objects.filter(name__icontains="Measuring Scoop").first()
    
    if araku_coffee and scoop:
        o5 = Offer.objects.create(
            title="Free Scoop with Araku Valley",
            description="Buy a pack of Araku Valley Medium Roast and get a free measuring scoop.",
            trigger='automatic',
            condition_type='product',
            condition_product=araku_coffee,
            action_type='free_product',
            free_product=scoop,
            valid_from=now,
            valid_to=next_month,
            priority=60
        )
        offers_created.append(o5)

    # 6. Coffee Enthusiast Bundle
    french_press = Product.objects.filter(name__icontains="French Press").first()
    araku_light = Product.objects.filter(name__icontains="Araku Valley Light Roast").first()
    
    if french_press and araku_light:
        o6 = Offer.objects.create(
            title="The French Press Starter Kit",
            description="Get the French Press and Araku Valley Light Roast together for a fixed bundle price of ₹1499.",
            trigger='automatic',
            condition_type='none',
            action_type='bundle_price',
            bundle_price=1499.00,
            valid_from=now,
            valid_to=next_year,
            priority=50
        )
        o6.bundle_products.add(french_press, araku_light)
        offers_created.append(o6)

    print("\nSuccessfully created the following offers:")
    for o in offers_created:
        print(f"✅ {o.title} (Trigger: {o.trigger}, Code: {o.coupon_code})")

if __name__ == "__main__":
    create_offers()
