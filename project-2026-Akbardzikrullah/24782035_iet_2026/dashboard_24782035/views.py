from django.views.generic import TemplateView
from django.http import JsonResponse
from main_app.models import Report
from django.db.models import Count


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'


def dashboard_data(request):
    total_reports = Report.objects.count()

    status_data = list(
        Report.objects.values('status').annotate(total=Count('id'))
    )

    category_data = list(
        Report.objects.values('category').annotate(total=Count('id'))
    )

    latest_reported = list(
        Report.objects.filter(status='REPORTED')
        .order_by('-id')[:5]
        .values('title', 'status')
    )

    latest_resolved = list(
        Report.objects.filter(status='RESOLVED')
        .order_by('-id')[:5]
        .values('title', 'status')
    )

    return JsonResponse({
        'total_reports': total_reports,
        'status_data': status_data,
        'category_data': category_data,
        'latest_reported': latest_reported,
        'latest_resolved': latest_resolved,
    })