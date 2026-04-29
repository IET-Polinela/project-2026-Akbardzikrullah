from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Report
from .forms import ReportForm


# ==============================
# 🔐 CEK ADMIN (HELPER)
# ==============================
def is_admin(user):
    return user.is_authenticated and user.is_admin


# ==============================
# 🏠 HOME
# ==============================
def home(request):
    return render(request, 'main_app/home.html')


# ==============================
# 📄 LIST (SEMUA USER)
# ==============================
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'


# ==============================
# 📄 DETAIL (SEMUA USER)
# ==============================
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'


# ==============================
# ➕ CREATE (ADMIN ONLY + ALERT)
# ==============================
class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('main_app:report_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, "❌ Hanya admin yang boleh menambahkan laporan!")
            return redirect('main_app:report_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "✅ Laporan berhasil ditambahkan!")
        return super().form_valid(form)
# ==============================
# ✏️ UPDATE (ADMIN ONLY + ALERT)
# ==============================
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

    def form_valid(self, form):
        messages.success(self.request, "✅ Laporan berhasil diperbarui!")
        return super().form_valid(form)


# ==============================
# 🗑 DELETE (ADMIN ONLY + ALERT)
# ==============================
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('main_app:report_list')

    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user):
            messages.error(request, "❌ Hanya admin yang bisa menghapus laporan!")
            return redirect('main_app:report_list')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "✅ Laporan berhasil dihapus!")
        return super().delete(request, *args, **kwargs)


# ==============================
# 🔄 UPDATE STATUS (ADMIN ONLY + ALERT)
# ==============================
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        if not is_admin(request.user):
            messages.error(request, "❌ Hanya admin yang bisa mengubah status!")
            return redirect('main_app:report_list')

        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')

        allowed_transitions = {
            'REPORTED': 'VERIFIED',
            'VERIFIED': 'IN_PROGRESS',
            'IN_PROGRESS': 'RESOLVED',
        }

        if report.status in allowed_transitions and allowed_transitions[report.status] == new_status:
            report.status = new_status
            report.save()
            messages.success(request, f"✅ Status berhasil diubah menjadi {new_status}!")
        else:
            messages.error(request, "❌ Perubahan status tidak valid!")

        return redirect('main_app:report_list')