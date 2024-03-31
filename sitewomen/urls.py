from django.contrib import admin
from django.urls import path, include
from women import views
from women.views import page_not_found
from sitewomen import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps.views import sitemap
from women.models import Women
from women.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
    path('users/', include('users.urls', namespace="users")),
    path("debug/", include("debug_toolbar.urls")),
    path('social-auth/', include('social_django.urls', namespace = 'social')), 
    path('captcha/', include('captcha.urls')),
    path('sitemap.xml', cache_page(86400)(sitemap), {'sitemaps': sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = page_not_found

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Известные порноактрисы"

