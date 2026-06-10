let currentTab  = 'my_reports'; 
let currentPage = 1;            
let editingReportId = null;     

function updateNavbar() {
    const navMenus = document.getElementById('nav-menus');
    if (!navMenus) return;
    if (localStorage.getItem('access_token')) {
        navMenus.innerHTML = `<button class="btn btn-outline-light btn-sm fw-bold" onclick="logout()"><i class="bi bi-box-arrow-right me-1"></i>Logout</button>`;
    } else {
        navMenus.innerHTML = '';
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.hash = '#login';
    updateNavbar();
}

async function loadDashboardData(tab = currentTab, page = currentPage) {
    currentTab  = tab;
    currentPage = page;

    // Update styling tab aktif
    const navLinks = document.querySelectorAll('.nav-tabs .nav-link');
    navLinks.forEach(link => {
        link.classList.remove('active', 'text-dark', 'fw-bold');
        link.classList.add('text-muted');
        if ((tab === 'my_reports' && link.textContent.includes('Laporan Saya')) || 
            (tab === 'feed' && link.textContent.includes('Feed Kota'))) {
            link.classList.add('active', 'text-dark', 'fw-bold');
            link.classList.remove('text-muted');
        }
    });

    const response = await requestAPI(`/api/report/?tab=${tab}&page=${page}`, 'GET');

    if (response && response.status === 200) {
        const data        = await response.json();
        const reports     = data.results || []; 
        const totalCount  = data.count   || 0;   
        const totalPages  = Math.ceil(totalCount / 10); 

        renderList(reports, tab);           
        renderPagination(totalPages);       
        loadSummaryStats();                 
    } else {
        document.getElementById('listContainer').innerHTML = `<div class="col-12 text-center text-muted p-5"><p>Gagal memuat data laporan.</p></div>`;
    }
}

function renderList(reports, tab) {
    const listContainer = document.getElementById('listContainer');
    if (!listContainer) return;

    if (reports.length === 0) {
        listContainer.innerHTML = `<div class="col-12 text-center text-muted p-5"><h5>Belum ada laporan.</h5></div>`;
        return;
    }

    const statusConfig = {
        'DRAFT':       { label: 'Draft',        color: 'secondary', pct: 10  },
        'REPORTED':    { label: 'Dilaporkan',   color: 'info',      pct: 30  },
        'VERIFIED':    { label: 'Diverifikasi', color: 'primary',   pct: 50  },
        'IN_PROGRESS': { label: 'Diproses',     color: 'warning',   pct: 75  },
        'RESOLVED':    { label: 'Selesai',      color: 'success',   pct: 100 },
    };

    const cardsHTML = reports.map(report => {
        const cfg     = statusConfig[report.status] || { label: report.status, color: 'dark', pct: 0 };
        const isOwner = report.is_owner;
        const reporterName = tab === 'feed' ? 'Warga Anonim' : (report.reporter_name || 'Tidak Diketahui');

        const editButton = (isOwner && report.status === 'DRAFT')
            ? `<button class="btn btn-sm btn-outline-warning text-dark fw-bold w-100" onclick="editDraft(${report.id})"><i class="bi bi-pencil-fill me-1"></i>Edit Draft</button>`
            : '';

        return `
            <div class="col-md-6 mb-4">
                <div class="card h-100 shadow-sm border-0">
                    <div class="card-body">
                        <span class="badge bg-${cfg.color} mb-2">${cfg.label}</span>
                        <h5 class="card-title fw-bold">${report.title}</h5>
                        <p class="card-text text-muted small">${report.description.substring(0, 100)}...</p>
                        <hr>
                        <p class="card-text small mb-1"><i class="bi bi-geo-alt-fill text-danger me-1"></i>${report.location}</p>
                        <p class="card-text small text-muted"><i class="bi bi-person-circle me-1"></i>${reporterName}</p>
                    </div>
                    <div class="card-footer bg-transparent border-0 pb-3">
                        <small class="text-muted fw-bold">Progress:</small>
                        <div class="progress mt-1 mb-3" style="height: 10px;">
                            <div class="progress-bar bg-${cfg.color} progress-bar-striped progress-bar-animated" role="progressbar" style="width: ${cfg.pct}%"></div>
                        </div>
                        ${editButton}
                    </div>
                </div>
            </div>
        `;
    }).join('');

    listContainer.innerHTML = cardsHTML;
}

function renderPagination(totalPages) {
    const paginationContainer = document.getElementById('paginationContainer');
    if (!paginationContainer) return;

    if (totalPages <= 1) {
        paginationContainer.innerHTML = '';
        return;
    }

    let buttonsHTML = '';
    for (let i = 1; i <= totalPages; i++) {
        const isActive = i === currentPage ? 'active' : '';
        buttonsHTML += `<li class="page-item ${isActive}"><button class="page-link" onclick="loadDashboardData('${currentTab}', ${i})">${i}</button></li>`;
    }

    paginationContainer.innerHTML = `<nav><ul class="pagination justify-content-center">${buttonsHTML}</ul></nav>`;
}

async function loadSummaryStats() {
    const response = await requestAPI('/api/report/?tab=my_reports&page_size=1000', 'GET');
    if (response && response.status === 200) {
        const data    = await response.json();
        const reports = data.results || [];
        
        const draftCount      = reports.filter(r => r.status === 'DRAFT').length;
        const inProgressCount = reports.filter(r => ['REPORTED', 'VERIFIED', 'IN_PROGRESS'].includes(r.status)).length;
        const resolvedCount   = reports.filter(r => r.status === 'RESOLVED').length;

        const elDraft      = document.getElementById('count-draft');
        const elInProgress = document.getElementById('count-inprogress');
        const elResolved   = document.getElementById('count-resolved');

        if (elDraft)      elDraft.textContent      = draftCount;
        if (elInProgress) elInProgress.textContent = inProgressCount;
        if (elResolved)   elResolved.textContent   = resolvedCount;
    }
}

async function editDraft(id) {
    editingReportId = id;
    const response = await requestAPI(`/api/report/${id}/`, 'GET');
    if (response && response.status === 200) {
        const report = await response.json();
        document.getElementById('fieldTitle').value       = report.title;
        document.getElementById('fieldCategory').value    = report.category;
        document.getElementById('fieldDescription').value = report.description;
        document.getElementById('fieldLocation').value    = report.location;
        document.getElementById('reportModalLabel').innerHTML = '<i class="bi bi-pencil-square me-2"></i>Edit Laporan Draft';
        
        const modal = new bootstrap.Modal(document.getElementById('reportModal'));
        modal.show();
    }
}

function openNewReportModal() {
    editingReportId = null;
    document.getElementById('reportForm').reset();
    document.getElementById('reportModalLabel').innerHTML = '<i class="bi bi-pencil-square me-2"></i>Buat Laporan Baru';
    const modal = new bootstrap.Modal(document.getElementById('reportModal'));
    modal.show();
}

async function submitReport(statusToSend) {
    const title       = document.getElementById('fieldTitle').value.trim();
    const category    = document.getElementById('fieldCategory').value;
    const description = document.getElementById('fieldDescription').value.trim();
    const location    = document.getElementById('fieldLocation').value.trim();

    if (!title || !category || !description || !location) {
        alert('Semua field wajib diisi!');
        return;
    }

    const payload = { title, category, description, location, status: statusToSend };
    let method = editingReportId === null ? 'POST' : 'PUT';
    let endpoint = editingReportId === null ? '/api/report/' : `/api/report/${editingReportId}/`;

    const response = await requestAPI(endpoint, method, payload);

    if (response && (response.status === 201 || response.status === 200)) {
        const modalEl    = document.getElementById('reportModal');
        const modalInst  = bootstrap.Modal.getInstance(modalEl);
        if (modalInst) modalInst.hide();

        document.getElementById('reportForm').reset();
        editingReportId = null; 
        loadDashboardData(currentTab, currentPage);
    } else {
        alert('Gagal menyimpan laporan.');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const btnDraft  = document.getElementById('btnDraft');
    const btnSubmit = document.getElementById('btnSubmit');

    if (btnDraft)  btnDraft.addEventListener('click', () => submitReport('DRAFT'));
    if (btnSubmit) btnSubmit.addEventListener('click', () => submitReport('REPORTED'));
});