from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now



class Category(models.Model):
    category = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, db_index=True, blank=True)

    
    def __str__(self):
        return self.category
    
    
    class Meta:
        verbose_name_plural = "Kategoriler"




class Haber(models.Model):
    kaynak = models.CharField(max_length=100)
    baslik = models.CharField(max_length=255)
    link = models.URLField(unique=True)
    tarih = models.DateTimeField(default=now)
    aciklama = models.TextField()
    resim = models.URLField(blank=True, null=True)
    
    
    def __str__(self):
        return self.baslik
    
    
    class Meta:
        verbose_name_plural = "Haberler"
    
    
