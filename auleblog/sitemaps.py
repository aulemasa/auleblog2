#coding: utf-8

from django.contrib.sitemaps import Sitemap
from .models import Article

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Article.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.date_pub
