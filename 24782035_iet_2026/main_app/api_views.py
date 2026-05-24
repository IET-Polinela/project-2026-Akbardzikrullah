from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly  # <-- Import izin yang udah kita buat

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    # Aturan biar DRAFT orang lain nggak bocor di API
    def get_queryset(self):
        user = self.request.user
        
        # Kalau Admin, jangan tampilkan DRAFT
        if getattr(user, 'is_admin', False):
            return Report.objects.exclude(status='DRAFT')
            
        # Kalau Citizen, tampilkan DRAFT miliknya sendiri + semua yang bukan DRAFT
        return Report.objects.filter(Q(reporter=user) | ~Q(status='DRAFT'))

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)