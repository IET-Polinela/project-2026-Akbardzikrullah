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
    return user.is_authenticated and getattr(user, 'is_admin', False)


def home(request):
    return render(request, 'main_app/home.html')


# 1. LIST: Admin exclude DRAFT, Citizen = Admin + DRAFT miliknya
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            # Tamu cuma bisa lihat yang bukan draft
            return Report.objects.exclude(status='DRAFT')
        
        if is_admin(user):
            # Admin exclude DRAFT
            return Report.objects.exclude(status='DRAFT')
        else:
            # Citizen lihat punya dia (termasuk draft) ATAU laporan publik (bukan draft)
            return Report.objects.filter(Q(reporter=user) | ~Q(status='DRAFT'))


class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'


# 2. CREATE: Citizen yang bikin
class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:report_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "❌ Anda harus login untuk membuat laporan!")
            return redirect('main_app:report_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Otomatis isi kolom reporter pakai user yang lagi login!
        form.instance.reporter = self.request.user
        return super().form_valid(form)


# 3. EDIT & DELETE: Cuma Citizen pemilik laporan (Admin gak boleh)
class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:report_list')

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()
        # Kalau yang login bukan reporternya (pemilik aslinya), tolak!
        if request.user != report.reporter:
            messages.error(request, "❌ Anda tidak berhak mengedit laporan ini!")
            return redirect('main_app:report_list')
        return super().dispatch(request, *args, **kwargs)


class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('main_app:report_list')

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()
        # Kalau yang login bukan reporternya (pemilik aslinya), tolak!
        if request.user != report.reporter:
            messages.error(request, "❌ Anda tidak berhak menghapus laporan ini!")
            return redirect('main_app:report_list')
        return super().dispatch(request, *args, **kwargs)


# 4. KHUSUS ADMIN: Cuma Ngubah Status Aja
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


# 🔍 LIVE SEARCH (Filter disamakan dengan ListView)
def search_reports(request):
    query = request.GET.get('q', '')
    user = request.user

    # Aturan filter data disamakan biar pas nyari nggak bocor
    if not user.is_authenticated:
        base_qs = Report.objects.exclude(status='DRAFT')
    elif is_admin(user):
        base_qs = Report.objects.exclude(status='DRAFT')
    else:
        base_qs = Report.objects.filter(Q(reporter=user) | ~Q(status='DRAFT'))

    reports = base_qs.filter(
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