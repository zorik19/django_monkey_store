from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline


from .models import *


class CollectionNamesInline(admin.TabularInline):

    model = Brand.collection.through


class ImageGalleryInline(GenericTabularInline):
    model = ImageGallery
    readonly_fields = ('image_url',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ImageGalleryInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    inlines = [CollectionNamesInline, ImageGalleryInline]
    exclude = ('collection',) # maby this


admin.site.register(KindClothes)
admin.site.register(CollectionName)
admin.site.register(TextileType)
admin.site.register(ImageGallery)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Notification)

