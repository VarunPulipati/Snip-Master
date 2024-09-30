import os
from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from .views import CustomLoginView, home, SignUpView, download_file
from . import views  # Corrected import statement
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),  # Ensure there's a view called 'home' in your views.py
    path('api/login/', CustomLoginView.as_view(), name='api_login'),
    path('api/signup/', SignUpView.as_view(), name='signup'),  # Updated to handle signup as API view
    path('download-software/', views.download_file, name='download-software'),
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', TemplateView.as_view(template_name='index.html')),  
    path('manifest.json', serve, {'path': 'manifest.json', 'document_root': os.path.join(settings.BASE_DIR, 'build')}),
# React's index.html
]

# Add this catch-all pattern to serve index.html from React's build folder
urlpatterns += [path('', TemplateView.as_view(template_name='index.html'))]
