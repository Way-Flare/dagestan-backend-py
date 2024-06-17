from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from app.spectacular import urlpatterns as spectacular_urls

v1 = [
    path("places/", include("place.urls")),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(v1)),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
urlpatterns += spectacular_urls
