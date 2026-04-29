from django.views.generic import TemplateView
from django.http import JsonResponse
from main_app.models import Report
from django.db.models import Count


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # total laporan
        context['total_reports'] = Report.objects.count()

        # jumlah per kategori
        context['category_data'] = Report.objects.values('category').annotate(total=Count('id'))

        # jumlah per status
        context['status_data'] = Report.objects.values('status').annotate(total=Count('id'))

        return context


# API JSON
def dashboard_data(request):
    total_reports = Report.objects.count()

    category_data = list(
        Report.objects.values('category').annotate(total=Count('id'))
    )

    status_data = list(
        Report.objects.values('status').annotate(total=Count('id'))
    )

    return JsonResponse({
        'total_reports': total_reports,
        'category_data': category_data,
        'status_data': status_data,
    })