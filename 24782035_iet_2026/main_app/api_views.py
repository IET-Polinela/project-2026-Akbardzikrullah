from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly

# === TAMBAHAN BARU: Class Pagination ===
class ReportPagination(PageNumberPagination):
    page_size = 10                   # Setiap halaman maksimal 10 data
    page_size_query_param = 'page_size'  # Client boleh override lewat ?page_size=
    max_page_size = 100              # Batas maksimal override-nya 100

class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    pagination_class = ReportPagination   # TAMBAHAN: aktifkan pagination

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]
        return [permissions.IsAuthenticated()]

    # === MODIFIKASI: get_queryset() sekarang punya sorting + filtering ===
    def get_queryset(self):
        user = self.request.user

        # Sorting: selalu urut dari yang paling baru diupdate
        queryset = Report.objects.all().order_by('-updated_at')

        # Filtering: baca parameter ?tab= dari URL
        tab = self.request.query_params.get('tab', None)

        if tab == 'my_reports':
            # Tab "Laporan Saya": hanya laporan MILIK user yang login
            queryset = queryset.filter(reporter=user)

        elif tab == 'feed':
            # Tab "Feed Kota": laporan dari warga LAIN yang BUKAN DRAFT
            queryset = queryset.filter(~Q(reporter=user) & ~Q(status='DRAFT'))

        return queryset

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)