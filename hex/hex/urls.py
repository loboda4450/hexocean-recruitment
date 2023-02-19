from django.urls import include, path, re_path
from rest_framework import routers
from images import views
from django.views.static import serve
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'images', views.ImageViewSet, basename='image')
router.register(r'permissions', views.PermissionViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^pics/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,})
]
