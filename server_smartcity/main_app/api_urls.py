from rest_framework.routers import DefaultRouter
from .api_views import ReportViewSet

# Menggunakan DefaultRouter untuk otomatisasi URL endpoint
router = DefaultRouter()

# Registrasi ReportViewSet dengan awalan rute 'report'
router.register(r'report', ReportViewSet, basename='report')

# Mengatur urlpatterns agar menggunakan hasil dari router
urlpatterns = router.urls