from django.contrib import admin
from .models import Main_info, Category, Product, Blog, Review, Guest_Review


@admin.register(Main_info)
class Main_infoAdmin(admin.ModelAdmin):
    list_display = ('address', 'number_phone_1', 'number_phone_2', 'email')
    search_fields = ('address', 'email', 'number_phone_1', 'number_phone_2')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount', 'available', 'quality_checking', 'views')
    list_filter = ('category', 'discount', 'available', 'quality_checking')
    search_fields = ('name', 'category__name', 'short_description')
    list_editable = ('price', 'discount', 'available', 'quality_checking')
    list_per_page = 20
    autocomplete_fields = ['category']
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'price', 'discount', 'discount_price')
        }),
        ('Описание', {
            'fields': ('short_description', 'full_description'),
            'classes': ('collapse',)
        }),
        ('Характеристики', {
            'fields': ('width', 'height', 'quality_checking', 'guarantee'),
        }),
        ('Медиа', {
            'fields': ('img',),
        }),
        ('Дополнительно', {
            'fields': ('available', 'views'),
            'classes': ('collapse',)
        }),
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'stars', 'date', 'is_public')
    list_filter = ('stars', 'is_public', 'product__category')
    search_fields = ('name', 'email', 'product__name', 'text')
    list_editable = ('is_public',)
    list_per_page = 20
    actions = ['make_public', 'make_private']

    @admin.action(description="Опубликовать выбранные отзывы")
    def make_public(self, request, queryset):
        queryset.update(is_public=True)

    @admin.action(description="Снять с публикации выбранные отзывы")
    def make_private(self, request, queryset):
        queryset.update(is_public=False)


class Guest_ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'date', 'is_public')
    list_filter = ('is_public', 'product__category')
    search_fields = ('name', 'tel_number', 'email', 'product__name', 'text')
    list_editable = ('is_public',)
    list_per_page = 20
    actions = ['make_public', 'make_private']

    @admin.action(description="Опубликовать выбранные отзывы")
    def make_public(self, request, queryset):
        queryset.update(is_public=True)

    @admin.action(description="Снять с публикации выбранные отзывы")
    def make_private(self, request, queryset):
        queryset.update(is_public=False)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'short_description', 'text_1', 'text_2', 'text_3')
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('title', 'short_description', 'img')
        }),
        ('Содержание', {
            'fields': ('text_1', 'img_1', 'text_2', 'img_2', 'text_3'),
        }),
    )


admin.site.register(Product, ProductAdmin)
# admin.site.register(Blog, BlogAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Guest_Review, Guest_ReviewAdmin)