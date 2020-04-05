from django.urls import path

from .views import *

# router = routers.DefaultRouter()
# router.register(r'words', views.WordView,basename='Word')
# router.register(r'word_appearance', views.WordAppearanceView,basename='WordAppearance')
# router.register(r'videos', views.VideoView,basename='Video')
# router.register(r'captions', views.CaptionView,basename='Caption')
# router.register(r'fetch_setting', views.FetchSettingView,basename='FetchSetting')

urlpatterns = [
    # path(r'', include(router.urls)),
    # path(r'words/', WordListApiView.as_view({'get': 'list'}))
]
