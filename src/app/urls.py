from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

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

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
urlpatterns += spectacular_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
