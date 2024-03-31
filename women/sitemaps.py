from django.contrib.sitemaps import Sitemap
from .models import Women

class PostSitemap(Sitemap):
    changefreq = 'montly'
    priority = 0.9
    
    def items(self):
        return Women.published.all()
    
    def lasmod(self, obj):
        return obj.time_update