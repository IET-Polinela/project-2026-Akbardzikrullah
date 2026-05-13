from django.contrib import admin
from django.urls import path, include
from main_app.views import home
from usermanagement_24782035.views import login_view, logout_view, register

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔐 AUTH (PAKAI CUSTOM)
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),

    # 🏠 HOME
    path('', home, name='home'),

    # 📄 FITUR
    path('reports/', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),

    # 📊 DASHBOARD
    path('dashboard/', include('dashboard_24782035.urls')),

    # 🌐 REST API (Lab Session 9)
    # Menghubungkan rute API menggunakan include dengan path dasar api/
    path('api/', include('main_app.api_urls')),
]