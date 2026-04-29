from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from main_app.views import home  

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔐 AUTH
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # 🏠 HOME
    path('', home, name='home'),

    # 📄 FITUR UTAMA
    path('reports/', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),

    # 👤 USER
    path('', include('usermanagement_24782035.urls')),

    # 📊 DASHBOARD 
    path('dashboard/', include('dashboard_24782035.urls')),
]