from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(viewsets.ModelViewSet):
    # Mengizinkan akses tanpa autentikasi sesuai instruksi lab
    permission_classes = [permissions.AllowAny]
    
    # Mengambil semua data dari model Report untuk ditampilkan di API
    queryset = Report.objects.all()
    
    # Menggunakan serializer yang sudah kita buat sebelumnya
    serializer_class = ReportSerializer