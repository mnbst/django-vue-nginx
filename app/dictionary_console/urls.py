from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'words', views.WordView)
router.register(r'videos', views.VideoView)
router.register(r'captions', views.CaptionView)
router.register(r'video_excepted', views.VideoExceptedView)

urlpatterns = [path(r'', include(router.urls))]
