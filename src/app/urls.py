from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from app.spectacular import urlpatterns as spectacular_urls

v1 = [
    path('places/', include('place.urls')),
    path('routes/', include('route.urls')),
    path('auth/', include('authenticate.urls')),
    path('profile/', include('user.urls'))
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(v1)),
]

urlpatterns += spectacular_urls
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.LOCAL_WORKING:
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
