from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q

from .models import Report
from .forms import ReportForm


def is_admin(user):
    return user.is_authenticated and user.is_admin


def home(request):
    return render(request, 'main_app/home.html')


class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'


class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'


class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:report_list')

    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user):
            messages.error(request, "❌ Hanya admin yang boleh menambahkan laporan!")
            return redirect('main_app:report_list')
        return super().dispatch(request, *args, **kwargs)


class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:report_list')

    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user):
            messages.error(request, "❌ Hanya admin yang bisa mengedit laporan!")
            return redirect('main_app:report_list')
        return super().dispatch(request, *args, **kwargs)


class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('main_app:report_list')


class ReportUpdateStatusView(View):
    def post(self, request, pk):
        if not is_admin(request.user):
            return redirect('main_app:report_list')

        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')

        allowed = {
            'REPORTED': 'VERIFIED',
            'VERIFIED': 'IN_PROGRESS',
            'IN_PROGRESS': 'RESOLVED',
        }

        if report.status in allowed and allowed[report.status] == new_status:
            report.status = new_status
            report.save()

        return redirect('main_app:report_list')


# 🔍 LIVE SEARCH
def search_reports(request):
    query = request.GET.get('q', '')

    reports = Report.objects.filter(
        Q(title__icontains=query) |
        Q(category__icontains=query) |
        Q(location__icontains=query)
    )

    html = render_to_string(
        'main_app/_report_rows.html',
        {'reports': reports, 'user': request.user}
    )

    return JsonResponse({'html': html})


# 📦 DETAIL MODAL API
def report_detail_api(request, pk):
    report = get_object_or_404(Report, pk=pk)

    data = {
        'title': report.title,
        'category': report.category,
        'location': report.location,
        'status': report.status,
        'description': report.description,
    }

    return JsonResponse(data)