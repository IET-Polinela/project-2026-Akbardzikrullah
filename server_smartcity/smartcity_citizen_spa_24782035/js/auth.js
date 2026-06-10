function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');
    
    // Pastikan form-nya ada di halaman sebelum ditambahkan event
    if (!loginForm) return;

    loginForm.addEventListener('submit', async function(event) {
        // WAJIB: Cegah form bawaan browser agar tidak reload halaman
        // Kalau reload, password bisa bocor di URL (GET request)
        event.preventDefault();

        // Ambil nilai yang diketik user
        const usernameInput = document.getElementById('loginUsername').value;
        const passwordInput = document.getElementById('loginPassword').value;

        // Siapkan payload (data yang mau dikirim)
        const payload = {
            username: usernameInput,
            password: passwordInput
        };

        // Ubah tombol jadi loading biar UX-nya bagus
        const submitBtn = loginForm.querySelector('button[type="submit"]');
        submitBtn.innerHTML = 'Memproses...';
        submitBtn.disabled = true;

        // Kirim request ke endpoint token Django
        const response = await requestAPI('/api/token/', 'POST', payload);

        // Jika responsenya 200 OK
        if (response && response.ok) {
            const data = await response.json();
            
            // Simpan token ke localStorage
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            
            alert('Login Berhasil!');
            
            // Ubah rute (halaman) ke dashboard
            window.location.hash = '#dashboard';
        } else {
            // Jika statusnya 401 (Unauthorized) atau lainnya
            alert('Login gagal! Periksa kembali Username dan Password Anda.');
            
            // Kembalikan tombol seperti semula
            submitBtn.innerHTML = 'Masuk';
            submitBtn.disabled = false;
        }
    });
}