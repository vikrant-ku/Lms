from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'The St. Lamart Sr. Sec. School'
admin.site.site_title = 'The St. Lamart Admin'
admin.site.site_url = 'https://stlamartschooluk.com/'
admin.site.index_title = 'The St. Lamart Sr. Sec. School'
admin.empty_value_display = '**Empty**'

urlpatterns = [
    path('main_admin/', admin.site.urls),
    path('', include('student.urls')),
    path('admin/', include('admins.urls')),
    path('library/', include('library.urls')),
    path('teacher/', include('teacher.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)