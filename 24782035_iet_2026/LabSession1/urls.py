from django.contrib import admin
from django.urls import path
from django.http import HttpResponse 

# Fungsi untuk menampilkan teks Selamat Datang
def welcome_view(request):
    return HttpResponse("Selamat Datang")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('welcome/', welcome_view), 
]
