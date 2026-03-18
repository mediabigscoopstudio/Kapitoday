from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


class Customers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_account')
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.email})"


class Category(models.Model):
    title = models.TextField()
    description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    category_image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    status = models.CharField(max_length=255,default="Disabled")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:50])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    title = models.TextField()
    description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    status = models.CharField(max_length=255,default="Disabled")

    class Meta:
        unique_together = ('category', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:50])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.title} > {self.title}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='product_sub_category', null=True, blank=True)
    name = models.TextField()
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='product_thumbnails/', null=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    meta_image = models.ImageField(upload_to='product_meta_images/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True,default="Disabled")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name[:50])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variant')
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gst = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='variant_images/', null=True, blank=True)
    status = models.CharField(max_length=255,default="Disabled")

    def __str__(self):
        return self.name


class Highlight(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_highlight')
    icon = models.ImageField(upload_to='highlight_icons/', null=True, blank=True)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class APlusContent(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_content')
    image = models.ImageField(upload_to='aplus_images/', null=True, blank=True)
    image_alt = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.product.name
    
class Offer(models.Model):

    # ── Trigger Type ──
    TRIGGER_CHOICES = [
        ('coupon',    'Coupon Code'),
        ('automatic', 'Automatic'),
    ]

    # ── Condition Type ──
    CONDITION_TYPE_CHOICES = [
        ('none',          'No Condition'),
        ('min_order',     'Minimum Order Amount'),
        ('min_quantity',  'Minimum Quantity'),
        ('product',       'Specific Product in Cart'),
        ('category',      'Specific Category in Cart'),
        ('sub_category',  'Specific Sub Category in Cart'),
        ('first_order',   'First Order Only'),
    ]

    # ── Action Type ──
    ACTION_TYPE_CHOICES = [
        ('percentage_off',  'Percentage Off'),
        ('flat_off',        'Flat Amount Off'),
        ('free_shipping',   'Free Shipping'),
        ('free_product',    'Free Product Added to Cart'),
        ('bundle_price',    'Fixed Bundle Price'),
        ('bogo',            'Buy X Get Y Free'),
    ]

    # ── Status ──
    STATUS_CHOICES = [
        ('Active',   'Active'),
        ('Inactive', 'Inactive'),
        ('Expired',  'Expired'),
        ('Scheduled','Scheduled'),
    ]

    # ── Core ──
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    trigger     = models.CharField(max_length=20, choices=TRIGGER_CHOICES)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    # ── Coupon Specific ──
    coupon_code      = models.CharField(max_length=50, unique=True, null=True, blank=True)
    usage_limit      = models.PositiveIntegerField(null=True, blank=True, help_text='Leave blank for unlimited')
    used_count       = models.PositiveIntegerField(default=0)
    one_per_customer = models.BooleanField(default=False)

    # ── Condition ──
    condition_type     = models.CharField(max_length=30, choices=CONDITION_TYPE_CHOICES, default='none')
    min_order_amount   = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Used when condition is min_order')
    min_quantity       = models.PositiveIntegerField(null=True, blank=True, help_text='Used when condition is min_quantity')
    condition_product  = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='condition_offers')
    condition_category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='condition_offers')
    condition_sub_category = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='condition_offers')

    # ── Action ──
    action_type      = models.CharField(max_length=30, choices=ACTION_TYPE_CHOICES)
    discount_value   = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Percentage or flat amount')
    max_discount_cap = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Max discount allowed (for percentage off)')

    # ── Free Product / BOGO ──
    free_product     = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='free_in_offers')
    free_variant     = models.ForeignKey('Variant', on_delete=models.SET_NULL, null=True, blank=True, related_name='free_in_offers')
    buy_quantity     = models.PositiveIntegerField(null=True, blank=True, help_text='Buy X — for BOGO')
    get_quantity     = models.PositiveIntegerField(null=True, blank=True, help_text='Get Y free — for BOGO')

    # ── Bundle ──
    bundle_products  = models.ManyToManyField('Product', blank=True, related_name='bundle_offers')
    bundle_price     = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # ── Stacking ──
    stackable        = models.BooleanField(default=False, help_text='Can this stack with other discounts?')
    priority         = models.PositiveIntegerField(default=0, help_text='Higher number = applied first')

    # ── Validity ──
    valid_from       = models.DateTimeField()
    valid_to         = models.DateTimeField()

    # ── Auto ──
    created_at       = models.DateTimeField(default=timezone.now)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_trigger_display()} — {self.get_action_type_display()})"

    def is_valid(self):
        now = timezone.now()
        return self.status == 'Active' and self.valid_from <= now <= self.valid_to

    def is_usage_limit_reached(self):
        if self.usage_limit is None:
            return False
        return self.used_count >= self.usage_limit
    
class Support(models.Model):
    name       = models.CharField(max_length=255)
    email      = models.EmailField()
    phone      = models.CharField(max_length=15, blank=True)
    subject    = models.CharField(max_length=255)
    message    = models.TextField()
    status     = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} — {self.subject}"