from django.contrib import admin
from .models import Word
from .models import Caption
from .models import Video
from .models import FetchSetting

admin.site.register(Word)
admin.site.register(Caption)
admin.site.register(Video)
admin.site.register(FetchSetting)
