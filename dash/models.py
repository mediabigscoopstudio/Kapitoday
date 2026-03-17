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
    category_image = models.ImageField(upload_to='subcategory_images/', null=True, blank=True)
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