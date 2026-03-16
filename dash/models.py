from django.db import models
from django.contrib.auth.models import User
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

    def __str__(self):
        return f"{self.category.title} > {self.title}"
    
class Variant(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='variant_images/', null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name    
    
class Highlight(models.Model):
    icon = models.ImageField(upload_to='highlight_icons/', null=True, blank=True)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class APlusContent(models.Model):
    highlight = models.ForeignKey(Highlight, on_delete=models.CASCADE, related_name='a_plus_contents')
    content = models.TextField()
    image = models.ImageField(upload_to='aplus_images/', null=True, blank=True)
    image_alt = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"A+ Content for {self.highlight.text}"
    
