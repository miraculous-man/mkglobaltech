from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500, handler400
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('app.urls')),
    path('accounts/', include('accounts.urls')),
    path('programs/', include('course.urls')),
    path('result/', include('result.urls')),
    path('search/', include('search.urls')),
    path('quiz/', include('quiz.urls')),

    path('payments/', include('payments.urls')),

    path('accounts/api/', include('accounts.api.urls', namespace='accounts-api')),
    
    path('admin_dashboard', include('admin_argon.urls')),
    
    path('admin/', admin.site.urls),
    path('library/', include('lmsApp.urls')),

    path('id_card/', include('eqrApp.urls')),
    path('base/', include('base.urls')),
    path('api/', include('base.api.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'app.views.handler404'
# handler500 = 'app.views.handler500'
# handler400 = 'app.views.handler400'
