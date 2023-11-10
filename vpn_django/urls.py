from django.contrib import admin
from django.urls import include, path
from vpn_site import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('statistics/', views.stats_view, name='statistics'),
    path('sites/', views.sites_view, name='sites'),
    path('<str:site_name><path:route>', views.proxy_view, name='proxy'),
]
