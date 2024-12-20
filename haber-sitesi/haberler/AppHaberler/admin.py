from django.contrib import admin
from .models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category", "slug")
    list_filter = ("category",)
    search_fields = ("category",)
    prepopulated_fields = {"slug" : ("category",)}
    ordering = ("-category",)
    fieldsets = (
        ("Kategoriler", {"fields": ("category",)}),
        ("Sluglar", {"fields": ("slug",)})
    )




class HaberAdmin(admin.ModelAdmin):
    list_display = ("kaynak", "baslik", "tarih") 
    list_filter = ("tarih",)
    search_fields = ("baslik",)
    ordering = ("-tarih",)
    fieldsets = (
        ("Kaynak", {"fields": ("kaynak",)}),
        ("Başlık", {"fields": ("baslik",)}),
        ("Link", {"fields": ("link",)}),
        ("Tarih", {"fields": ("tarih",)}),
        ("Açıklama", {"fields": ("aciklama",)}),
        ("Resim", {"fields": ("resim",)}),
    )
    
    readonly_fields = ("kaynak", "baslik", "link", "tarih", "aciklama", "resim")

    


admin.site.register(Category, CategoryAdmin)
admin.site.register(Haber, HaberAdmin)


