from modeltranslation.translator import register, TranslationOptions
from .models import Main_info, Category, Product, Blog


@register(Main_info)
class Main_infoTranslationOptions(TranslationOptions):
    fields = ('Our_mission', 'address',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'full_description', 'guarantee',)


@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'text_1', 'text_2', 'text_3')
