// Sesuaikan dengan URL server Django kamu
const BASE_URL = "http://103.151.63.85:8004";

async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    // 1. Ambil access_token dari penyimpanan lokal browser
    const token = localStorage.getItem('access_token');

    const config = buildRequestConfig(method, bodyData, token);

    // 2. Lakukan request ke backend
    try {
        const response = await fetch(BASE_URL + endpoint, config);

        if (
            response.status === 401 &&
            endpoint !== '/api/token/' &&
            endpoint !== '/api/token/refresh/' &&
            localStorage.getItem('refresh_token')
        ) {
            const refreshed = await refreshAccessToken();

            if (refreshed) {
                const retryConfig = buildRequestConfig(
                    method,
                    bodyData,
                    localStorage.getItem('access_token')
                );
                return await fetch(BASE_URL + endpoint, retryConfig);
            } else {
                // Bersihkan sesi, pemicu alert "Sesi berakhir", dan redirect ke #login
                clearSessionAndRedirect();
                
                // Melempar error agar fungsi pemanggil di UI langsung berhenti 
                // dan tidak memunculkan alert "Gagal menyimpan laporan."
                throw new Error("Sesi berakhir");
            }
        }

        return response; // Kembalikan response utuh untuk dicek caller
    } catch (error) {
        // Jika error berasal dari token habis, jangan tampilkan alert gagal terhubung server
        if (error.message === "Sesi berakhir") {
            throw error;
        }
        console.error('Error saat request API:', error);
        alert('Gagal terhubung ke server. Pastikan server Django menyala.');
    }
}

function buildRequestConfig(method, bodyData, token) {
    const headers = {
        'Content-Type': 'application/json',
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        method: method,
        headers: headers,
    };

    if (bodyData) {
        config.body = JSON.stringify(bodyData);
    }

    return config;
}

async function refreshAccessToken() {
    try {
        const response = await fetch(BASE_URL + '/api/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                refresh: localStorage.getItem('refresh_token'),
            }),
        });

        if (!response.ok) return false;

        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        return true;
    } catch (error) {
        console.error('Error saat refresh token:', error);
        return false;
    }
}

function clearSessionAndRedirect() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    alert('Sesi berakhir. Silakan login kembali.');
    window.location.hash = '#login';
}