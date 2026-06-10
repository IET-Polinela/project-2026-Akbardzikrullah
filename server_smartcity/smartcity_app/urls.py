from django.contrib import admin
from django.urls import path, include
from main_app.views import home
from usermanagement_24782035.views import login_view, logout_view, register

# 🔥 Import JWT & Register API Views (Lab 10)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from usermanagement_24782035.api_views import RegisterView

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

# 🔑 Endpoint JWT Token & Register Citizen (Lab Session 10)
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 👇 Ini dia tambahan endpoint buat register via API
    path('api/register/', RegisterView.as_view(), name='api_register'), 
]