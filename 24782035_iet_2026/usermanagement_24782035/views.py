from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout


# ✅ REGISTER
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.save()

            login(request, user)
            messages.success(request, "✅ Registrasi berhasil! Kamu sudah login.")
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


# ✅ LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "✅ Login berhasil!")
            return redirect('home')
        else:
            messages.error(request, "❌ Username atau password salah!")

    return render(request, 'registration/login.html')  # 🔥 FIX PATH


# ✅ LOGOUT
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logout berhasil!")
        return redirect('/')  # 🔥 langsung ke home URL
    return redirect('/')