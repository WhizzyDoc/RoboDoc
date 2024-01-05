from django.contrib import admin
from django.urls import path,include,re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from users import views as users_views
# from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import  login,

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('disease.urls')),
    path('model/',include('AI.urls')),
    path('user/',include('users.urls')),
    path('staff/',include('specialist.urls')),
    path('api/v1/',include('api.urls')),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='registration/password_reset_done.html'),
                       name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='registration/password_reset_complete.html'),
                       name='password_reset_complete'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
