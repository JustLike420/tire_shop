from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from shop.views import home_page
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home_page'),
    path('shop/', include('shop.urls')),
    path('user/', include('accounts.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
