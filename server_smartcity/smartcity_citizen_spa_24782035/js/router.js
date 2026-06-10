const routes = {
    '#login': `
        <div class="row justify-content-center mt-5">
            <div class="col-md-4 card shadow-sm border-0 p-4">
                <h4 class="text-center fw-bold mb-4">Login Warga</h4>
                <form id="loginForm">
                    <input type="text" id="loginUsername" class="form-control mb-3" placeholder="Username" required>
                    <input type="password" id="loginPassword" class="form-control mb-3" placeholder="Password" required>
                    <button type="submit" class="btn btn-primary w-100 fw-bold">Masuk</button>
                </form>
            </div>
        </div>
    `,
    '#dashboard': `
        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 80px;">
                    <button class="btn btn-primary btn-lg w-100 fw-bold mb-3" onclick="openNewReportModal()">
                        <i class="bi bi-plus-circle-fill me-2"></i>Laporan Baru
                    </button>
                    
                    <div class="card border-0 shadow-sm mt-3">
                        <div class="card-header bg-white fw-bold">Rekap Status</div>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Draft <span class="badge bg-secondary rounded-pill" id="count-draft">0</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Diproses <span class="badge bg-warning text-dark rounded-pill" id="count-inprogress">0</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Selesai <span class="badge bg-success rounded-pill" id="count-resolved">0</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </aside>
            
            <section class="col-12 col-lg-9">
                <ul class="nav nav-tabs mb-4">
                    <li class="nav-item">
                        <a class="nav-link active text-dark fw-bold" href="#" onclick="loadDashboardData('my_reports', 1); return false;">Laporan Saya</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-muted" href="#" onclick="loadDashboardData('feed', 1); return false;">Feed Kota</a>
                    </li>
                </ul>
                <div id="listContainer" class="row mt-3"></div>
                <div id="paginationContainer" class="mt-4"></div>
            </section>
        </div>
    `
};

function handleRouting() {
    const hash = window.location.hash || '#login';
    const appContent = document.getElementById('app-content');
    
    if (hash === '#dashboard' && !localStorage.getItem('access_token')) {
        window.location.hash = '#login';
        return;
    }

    if (appContent) appContent.innerHTML = routes[hash] || routes['#login'];
    
    // Update menu navigasi (logout button)
    if (typeof updateNavbar === 'function') updateNavbar();

    if (hash === '#login' && typeof setupLoginForm === 'function') {
        setupLoginForm();
    } else if (hash === '#dashboard' && typeof loadDashboardData === 'function') {
        setTimeout(() => loadDashboardData('my_reports', 1), 100);
    }
}

window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);