from django.shortcuts import render, get_object_or_404, redirect
import feedparser
from pprint import pprint
from datetime import datetime
from bs4 import BeautifulSoup
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.timezone import now
import requests





def index_view(request):

    # Sayfa yüklendiğinde haberleri kaydet
    haber_kaydet(request)
    
    categories = Category.objects.all()
    
    ensonhaber_url = "https://www.ensonhaber.com/rss/ensonhaber.xml"
    ensonhaber = feedparser.parse(ensonhaber_url)
    
    pprint(ensonhaber["entries"][0])

    haberler = []

    for haber in ensonhaber.entries:
        haber_dict = {}
        haber_dict["kaynak"] = "EnSonHaber"
        haber_dict["baslik"] = haber.title
        haber_dict["link"] = haber.link
        
        dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
        haber_dict["tarih"] = dt.strftime('%d-%m-%Y %H:%M:%S')
        
        if "media_content" in haber:
            img_src = haber["media_content"][0]["url"]
        
        if img_src:
            haber_dict["resim"] = img_src
        
        else:
            print("resim bulunamadı")
        
        ensonhaber_summary = haber.summary
        description = BeautifulSoup(ensonhaber_summary, "html.parser")
        description_text = description.get_text()
        haber_dict["aciklama"] = description_text

        haberler.append(haber_dict)
    
    # Saat Bilgisi

    güncel_zaman = datetime.now().strftime("%H:%M:%S")

    mesaj = "Anasayfadasınız.."

        
    context = {
        "haberler": haberler,
        "categories": categories,
        "current_time": güncel_zaman,
        "mesaj": mesaj
    }

    return render(request, "index.html", context)





def category_view(request, category):
    categories = Category.objects.all()
    
    haberler = []

    # Farklı kategoriler için RSS kaynakları
    rss_urls = {
        "politika": "https://www.ensonhaber.com/rss/politika.xml",
        "ekonomi": "https://www.ensonhaber.com/rss/ekonomi.xml",
        "teknoloji": "https://www.ensonhaber.com/rss/teknoloji.xml",
        "spor": "https://www.ensonhaber.com/rss/kralspor.xml",
        "dunya": "https://www.ensonhaber.com/rss/dunya.xml",
        "magazin": "https://www.ensonhaber.com/rss/magazin.xml",
    }

    if category in rss_urls:
        ensonhaber_url = rss_urls[category]
        ensonhaber = feedparser.parse(ensonhaber_url)

        for haber in ensonhaber.entries:
            haber_dict = {
                "kaynak": "EnSonHaber",
                "baslik": haber.title,
                "link": haber.link,
                "tarih": datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z').strftime('%d-%m-%Y %H:%M:%S'),
            }

            img_src = haber.get("media_content", [{}])[0].get("url", None)
            haber_dict["resim"] = img_src if img_src else "Resim bulunamadı"

            description = BeautifulSoup(haber.summary, "html.parser")
            haber_dict["aciklama"] = description.get_text()
            
            haberler.append(haber_dict)
    
    
    # Kategori seçildiği an kullanıcıya mesaj gönder
    messages.info(request, f"{category.title()} sayfasındasınız..") 

    
    # Sayfalandırma
    sayfalandirici = Paginator(haberler, 6)
    sayfa_no = request.GET.get("page")
    sayfa_obj = sayfalandirici.get_page(sayfa_no)

    
    context = {
        "categories": categories,
        "haberler": sayfa_obj,
        "category": category,
    }

    return render(request, "category.html", context)





def haber_kaydet(request):
    
    ensonhaber_url = "https://www.ensonhaber.com/rss/ensonhaber.xml"
    ensonhaber = feedparser.parse(ensonhaber_url)

    for haber in ensonhaber.entries:
        haber_dict = {}
        haber_dict["kaynak"] = "EnSonHaber"
        haber_dict["baslik"] = haber.title
        haber_dict["link"] = haber.link
        
        
        # Yayın tarihini formatla ve datetime objesi olarak kaydet
        dt = datetime.strptime(haber.published, '%a, %d %b %Y %H:%M:%S %z')
        haber_dict["tarih"] = dt
        
        
        # Resim URL'sini kontrol et ve ekle
        if "media_content" in haber:
            img_src = haber["media_content"][0]["url"]
        
        if img_src:
            haber_dict["resim"] = img_src
        
        else:
            print("resim bulunamadı")

        
        # Açıklamayı al ve HTML'den temizle
        ensonhaber_summary = haber.summary
        description = BeautifulSoup(ensonhaber_summary, "html.parser")
        description_text = description.get_text()
        haber_dict["aciklama"] = description_text


        # Haber modeline uygun şekilde kaydet
        _ , created = Haber.objects.get_or_create(
            link = haber_dict["link"],  # Eşsiz alan olarak link kullanılıyor
            defaults = {
                "kaynak": haber_dict["kaynak"],
                "baslik": haber_dict["baslik"],
                "tarih": haber_dict["tarih"],
                "resim": haber_dict["resim"],
                "aciklama": haber_dict["aciklama"],
            }
        )
        
        if created:
            print(f"Haber veritabanına kaydedildi: {haber_dict['baslik']}")
        
        else:
            print(f"Haber zaten veritabanında mevcut: {haber_dict['baslik']}")
        
    return redirect("/")




    
