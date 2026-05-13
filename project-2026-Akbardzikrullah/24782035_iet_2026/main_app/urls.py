from django.urls import path
from .views import (
    ReportListView,
    ReportDetailView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,
    search_reports,
    report_detail_api
)

app_name = 'main_app'

urlpatterns = [
    path('', ReportListView.as_view(), name='report_list'),
    path('detail/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('add/', ReportCreateView.as_view(), name='report_create'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='report_update'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='report_delete'),
    path('update-status/<int:pk>/', ReportUpdateStatusView.as_view(), name='update_status'),

    # 🔥 AJAX
    path('search/', search_reports, name='search_reports'),
    path('api/detail/<int:pk>/', report_detail_api, name='report_detail_api'),
]