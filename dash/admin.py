from django.contrib import admin
from .models import (
    # ── E-commerce ──────────────────────────────────────────────────────────
    Customers, Category, SubCategory, Product, ProductImage,
    Variant, Highlight, APlusContent, Offer,
    Support, Cart, CartItem, Order, OrderItem,
    # ── Content Management ───────────────────────────────────────────────────
    ArticleCategory, Author, Article, ArticleFAQ, ArticleHowTo,
)


# ═══════════════════════════════════════════════════════════════════════════
# EXISTING E-COMMERCE MODELS
# ═══════════════════════════════════════════════════════════════════════════

admin.site.register(Customers)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Variant)
admin.site.register(Highlight)
admin.site.register(APlusContent)
admin.site.register(Offer)
admin.site.register(Support)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)


# ═══════════════════════════════════════════════════════════════════════════
# CONTENT MANAGEMENT — INLINE MODELS
# ═══════════════════════════════════════════════════════════════════════════

class ArticleFAQInline(admin.TabularInline):
    model  = ArticleFAQ
    extra  = 1
    fields = ('question', 'answer')


class ArticleHowToInline(admin.TabularInline):
    model  = ArticleHowTo
    extra  = 1
    fields = ('step_name', 'step_text')


# ═══════════════════════════════════════════════════════════════════════════
# CONTENT MANAGEMENT — REGISTERED MODELS
# ═══════════════════════════════════════════════════════════════════════════

@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display        = ('title', 'status', 'display_order', 'show_in_nav', 'created_at')
    search_fields       = ('title', 'meta_keywords', 'description')
    list_filter         = ('status', 'show_in_nav')
    prepopulated_fields = {'slug': ('title',)}
    ordering            = ('display_order', 'title')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display        = ('name', 'designation', 'email', 'status', 'created_at')
    search_fields       = ('name', 'email', 'designation')
    list_filter         = ('status',)
    prepopulated_fields = {'slug': ('name',)}
    ordering            = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display        = ('title', 'author', 'category', 'status', 'created_at', 'views', 'likes')
    search_fields       = ('title', 'meta_keywords', 'meta_title')
    list_filter         = ('status', 'category', 'author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    ordering            = ('-created_at',)
    raw_id_fields       = ('author', 'category')
    inlines             = [ArticleFAQInline, ArticleHowToInline]
    readonly_fields     = ('views', 'likes', 'created_at', 'updated_at')


@admin.register(ArticleFAQ)
class ArticleFAQAdmin(admin.ModelAdmin):
    list_display  = ('question', 'article')
    search_fields = ('question', 'answer', 'article__title')
    list_filter   = ('article__category',)
    ordering      = ('article', 'id')


@admin.register(ArticleHowTo)
class ArticleHowToAdmin(admin.ModelAdmin):
    list_display  = ('step_name', 'article')
    search_fields = ('step_name', 'step_text', 'article__title')
    list_filter   = ('article__category',)
    ordering      = ('article', 'id')