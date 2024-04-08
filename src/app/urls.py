from django.contrib import admin
from django.urls import path, include

from app.spectacular import urlpatterns as spectacular_urls

v1 = [
    path("places/", include("place.urls")),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(v1)),
]

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
urlpatterns += spectacular_urls
