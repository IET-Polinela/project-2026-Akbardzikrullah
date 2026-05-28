// Sesuaikan dengan URL server Django kamu
const BASE_URL = 'http://127.0.0.1:8000';

async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    // 1. Ambil access_token dari penyimpanan lokal browser
    const token = localStorage.getItem('access_token');
    
    // 2. Siapkan Headers standar
    const headers = {
        'Content-Type': 'application/json',
    };

    // 3. Kalau tokennya ada, sisipkan ke dalam Headers Authorization
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    // 4. Siapkan konfigurasi fetch
    const config = {
        method: method,
        headers: headers,
    };

    // 5. Kalau ada bodyData (misal pas login/register), ubah jadi string JSON
    if (bodyData) {
        config.body = JSON.stringify(bodyData);
    }

    // 6. Lakukan request ke backend
    try {
        const response = await fetch(BASE_URL + endpoint, config);
        return response; // Kembalikan response utuh untuk dicek di auth.js
    } catch (error) {
        console.error('Error saat request API:', error);
        alert('Gagal terhubung ke server. Pastikan server Django menyala.');
    }
}