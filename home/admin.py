from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(Gallery)
# admin.site.register(GalleryImage)
admin.site.register(News)
admin.site.register(Contact)
# admin.site.register(Emi)
# admin.site.register(Photo)
# admin.site.register(Gallery, GalleryImage)


class GalleryImageInline(admin.StackedInline):
    model = GalleryImage
    extra = 0

class GalleryAdmin(admin.ModelAdmin):
    inlines = [
        GalleryImageInline,
    ]

admin.site.register(Gallery, GalleryAdmin)