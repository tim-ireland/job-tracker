const API_BASE = '/api';
let companies = [];
let applications = [];
let currentApplication = null;
let sortColumn = null;
let sortDirection = 'asc';
let showClosedApps = false;
let statusFilter = null;  // Track active status filter
let columnFilters = {};   // Track per-column text filters (string for plain inputs, array for tag inputs)
let tagFilters = {};      // Track Tom Select instances keyed by col name

document.addEventListener('DOMContentLoaded', async () => {
    loadDashboard();
    await loadCompanies();
    await loadApplications();
    setupEventListeners();
    setupTagFilters();
    setupModalClickOutside();
    setupSortableHeaders();
});

function setupEventListeners() {
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            const target = e.target.dataset.tab;
            switchTab(target);
        });
    });

    document.getElementById('addApplicationBtn').addEventListener('click', () => openApplicationModal());
    document.getElementById('addCompanyBtn').addEventListener('click', () => openCompanyModal());
    // importJobsBtn is commented out in HTML - skip event listener
    // document.getElementById('importJobsBtn').addEventListener('click', () => openImportJobsModal());
    document.getElementById('exportDUABtn').addEventListener('click', () => openDUAExportModal());
    document.getElementById('applicationForm').addEventListener('submit', handleApplicationSubmit);
    document.getElementById('companyForm').addEventListener('submit', handleCompanySubmit);
    // importJobsForm is only relevant if import button is active
    const importJobsForm = document.getElementById('importJobsForm');
    if (importJobsForm) {
        importJobsForm.addEventListener('submit', handleImportJobs);
    }
    
    // Show/hide closed applications toggle
    document.getElementById('showClosedApps').addEventListener('change', (e) => {
        showClosedApps = e.target.checked;
        updateApplicationList();
    });

    // Plain text column filters
    document.querySelectorAll('.col-filter').forEach(input => {
        input.addEventListener('input', (e) => {
            const col = e.target.dataset.col;
            columnFilters[col] = e.target.value.trim().toLowerCase();
            updateApplicationList();
        });
        // Prevent clicks on filter inputs from bubbling to sort headers
        input.addEventListener('click', (e) => e.stopPropagation());
    });

    document.querySelectorAll('.close-modal').forEach(btn => {
        btn.addEventListener('click', () => {
            closeModal(btn.closest('.modal').id);
        });
    });
}

function setupTagFilters() {
    const STATUS_OPTIONS = ['Pipeline', 'Applied', 'Screening', 'Interview', 'Offer', 'Closed', 'Rejected', 'Withdrawn', 'Accepted'];

    const tsConfig = (col, options, create) => ({
        plugins: ['remove_button'],
        maxItems: null,
        create,
        placeholder: 'Filter…',
        options: options.map(v => ({ value: v, text: v })),
        onChange(values) {
            tagFilters[col] = values;
            updateApplicationList();
        },
        onItemAdd() { this.setTextboxValue(''); this.refreshOptions(); },
    });

    const companyNames = [...new Set(companies.map(c => c.name))].sort();
    const roleNames    = [...new Set(applications.map(a => a.role).filter(Boolean))].sort();

    tagFilters['company'] = [];
    tagFilters['role']    = [];
    tagFilters['status']  = [];

    new TomSelect('#filter-company', tsConfig('company', companyNames, true));
    new TomSelect('#filter-role',    tsConfig('role',    roleNames,    true));
    new TomSelect('#filter-status',  tsConfig('status',  STATUS_OPTIONS, false));

    // Prevent clicks inside tag filters from bubbling to sort headers
    ['filter-company', 'filter-role', 'filter-status'].forEach(id => {
        document.getElementById(id)?.closest('th')
            ?.addEventListener('click', e => e.stopPropagation());
    });
}

function setupModalClickOutside() {
    // Close modal when clicking on the backdrop (outside modal content)
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            // Close if the click target is the modal itself (the backdrop)
            if (e.target === modal) {
                closeModal(modal.id);
            }
        });
    });
}

function setupSortableHeaders() {
    document.querySelectorAll('th.sortable').forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.sort;
            
            // Toggle direction if clicking same column
            if (sortColumn === column) {
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                sortColumn = column;
                sortDirection = 'asc';
            }
            
            // Update sort icons
            document.querySelectorAll('th.sortable .sort-icon').forEach(icon => {
                icon.className = 'fas fa-sort sort-icon';
            });
            
            const icon = header.querySelector('.sort-icon');
            icon.className = sortDirection === 'asc' 
                ? 'fas fa-sort-up sort-icon' 
                : 'fas fa-sort-down sort-icon';
            
            sortApplications();
        });
    });
}

function sortApplications() {
    if (!sortColumn) return;
    
    applications.sort((a, b) => {
        let aVal, bVal;
        
        switch(sortColumn) {
            case 'company':
                const companyA = companies.find(c => c.id === a.company_id);
                const companyB = companies.find(c => c.id === b.company_id);
                aVal = companyA ? companyA.name.toLowerCase() : '';
                bVal = companyB ? companyB.name.toLowerCase() : '';
                break;
            case 'role':
                aVal = a.role.toLowerCase();
                bVal = b.role.toLowerCase();
                break;
            case 'match_score':
                aVal = a.match_score || 0;
                bVal = b.match_score || 0;
                break;
            case 'priority':
                // P1 < P2 < P3 < P4 < P5
                // Handle both "P1" format and other text (e.g., "Medium")
                const parsePriority = (p) => {
                    if (!p) return 999;
                    const match = p.match(/P(\d+)/);
                    return match ? parseInt(match[1]) : 999;
                };
                aVal = parsePriority(a.priority);
                bVal = parsePriority(b.priority);
                break;
            case 'status':
                aVal = a.status.toLowerCase();
                bVal = b.status.toLowerCase();
                break;
            case 'salary':
                aVal = a.salary_range || '';
                bVal = b.salary_range || '';
                break;
            case 'date':
                aVal = a.date_applied ? new Date(a.date_applied).getTime() : 0;
                bVal = b.date_applied ? new Date(b.date_applied).getTime() : 0;
                break;
            default:
                return 0;
        }
        
        if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
        return 0;
    });
    
    updateApplicationList();
}

function switchTab(tabName) {
    document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    document.getElementById(`${tabName}Tab`).classList.add('active');
}

async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/dashboard`);
        const data = await response.json();
        document.getElementById('totalApps').textContent = data.total_applications;
        document.getElementById('pipelineApps').textContent = data.by_status.Pipeline || 0;
        const appliedCount = (data.by_status.Applied || 0) + (data.by_status.Screening || 0);
        document.getElementById('appliedApps').textContent = appliedCount;
        document.getElementById('screeningApps').textContent = data.by_status.Screening || 0;
        document.getElementById('interviews').textContent = data.by_status.Interview || 0;
        document.getElementById('offers').textContent = data.by_status.Offer || 0;
        document.getElementById('rejected').textContent = data.by_status.Rejected || 0;
        
        // Add click handlers for filtering
        setupDashboardFilters();
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function setupDashboardFilters() {
    // Make stat cards clickable
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.cursor = 'pointer';
        card.style.transition = 'transform 0.2s, box-shadow 0.2s';
        
        // Map card index to filter
        let filterStatus = null;
        switch(index) {
            case 0: filterStatus = null; break;  // Total - no filter
            case 1: filterStatus = 'Pipeline'; break;  // Pipeline
            case 2: filterStatus = 'Applied+Screening'; break;  // Applied (includes Screening)
            case 3: filterStatus = 'Screening'; break;
            case 4: filterStatus = 'Interview'; break;
            case 5: filterStatus = 'Offer'; break;
            case 6: filterStatus = 'Rejected'; break;
        }
        
        card.onclick = () => {
            // Toggle filter
            if (statusFilter === filterStatus) {
                statusFilter = null;  // Clear filter
                statCards.forEach(c => c.classList.remove('active-filter'));
            } else {
                statusFilter = filterStatus;
                statCards.forEach(c => c.classList.remove('active-filter'));
                card.classList.add('active-filter');
                
                // Auto-enable show closed if filtering for rejected
                if (filterStatus === 'Rejected') {
                    showClosedApps = true;
                    document.getElementById('showClosedApps').checked = true;
                }
            }
            
            updateApplicationList();
        };
        
        // Hover effect
        card.onmouseenter = () => {
            if (statusFilter !== filterStatus) {
                card.style.transform = 'translateY(-2px)';
            }
        };
        card.onmouseleave = () => {
            card.style.transform = 'translateY(0)';
        }
        
        card.onclick = () => {
            // Toggle filter
            if (statusFilter === filterStatus) {
                statusFilter = null;  // Clear filter
                statCards.forEach(c => c.classList.remove('active-filter'));
            } else {
                statusFilter = filterStatus;
                statCards.forEach(c => c.classList.remove('active-filter'));
                card.classList.add('active-filter');
                
                // Auto-enable show closed if filtering for rejected
                if (filterStatus === 'Rejected') {
                    showClosedApps = true;
                    document.getElementById('showClosedApps').checked = true;
                }
            }
            
            updateApplicationList();
        };
        
        // Hover effect
        card.onmouseenter = () => {
            if (statusFilter !== filterStatus) {
                card.style.transform = 'translateY(-2px)';
            }
        };
        card.onmouseleave = () => {
            card.style.transform = 'translateY(0)';
        };
    });
}

async function loadCompanies() {
    try {
        const response = await fetch(`${API_BASE}/companies`);
        companies = await response.json();
        updateCompanyList();
        updateCompanySelect();
    } catch (error) {
        console.error('Error loading companies:', error);
    }
}

function updateCompanyList() {
    const tbody = document.getElementById('companyTableBody');
    if (companies.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4">No companies yet</td></tr>';
        return;
    }
    tbody.innerHTML = companies.map(company => `
        <tr>
            <td><strong>${escapeHtml(company.name)}</strong></td>
            <td>${company.size || '-'}</td>
            <td>${company.tech_stack || '-'}</td>
            <td>
                <button class="btn btn-secondary btn-sm" onclick="editCompany(${company.id})">
                    <i class="fas fa-edit"></i> Edit
                </button>
                <button class="btn btn-danger btn-sm" onclick="deleteCompany(${company.id})">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </td>
        </tr>
    `).join('');
}

function updateCompanySelect() {
    const select = document.getElementById('companyId');
    select.innerHTML = '<option value="">Select Company...</option>' +
        companies.map(c => `<option value="${c.id}">${escapeHtml(c.name)}</option>`).join('');
}

async function loadApplications() {
    try {
        const response = await fetch(`${API_BASE}/applications`);
        applications = await response.json();
        updateApplicationList();
    } catch (error) {
        console.error('Error loading applications:', error);
    }
}

function updateApplicationList() {
    const tbody = document.getElementById('applicationTableBody');
    
    // Filter applications based on showClosedApps toggle
    const closedStatuses = ['Rejected', 'Withdrawn', 'Accepted'];
    let filteredApps = showClosedApps 
        ? applications 
        : applications.filter(app => !closedStatuses.includes(app.status));
    
    // Apply status filter if active
    if (statusFilter) {
        if (statusFilter === 'Applied+Screening') {
            // Special case: filter for Applied OR Screening (excluding Pipeline)
            filteredApps = filteredApps.filter(app => app.status === 'Applied' || app.status === 'Screening');
        } else {
            filteredApps = filteredApps.filter(app => app.status === statusFilter);
        }
    }

    // Apply tag filters (company, role, status) — OR within column, AND across columns
    Object.entries(tagFilters).forEach(([col, tags]) => {
        if (!tags || tags.length === 0) return;
        filteredApps = filteredApps.filter(app => {
            let value = '';
            if (col === 'company') {
                const c = companies.find(c => c.id === app.company_id);
                value = c ? c.name : '';
            } else if (col === 'role') {
                value = app.role || '';
            } else if (col === 'status') {
                value = app.status || '';
            }
            return tags.some(tag => value.toLowerCase().includes(tag.toLowerCase()));
        });
    });

    // Apply plain text column filters
    Object.entries(columnFilters).forEach(([col, term]) => {
        if (!term) return;
        filteredApps = filteredApps.filter(app => {
            let value = '';
            if (col === 'match_score') {
                value = app.match_score != null ? String(app.match_score) : '';
            } else if (col === 'priority') {
                value = app.priority || '';
            } else if (col === 'salary') {
                value = app.salary_range || '';
            } else if (col === 'date') {
                value = app.date_applied ? new Date(app.date_applied).toLocaleDateString() : '';
            }
            return value.toLowerCase().includes(term);
        });
    });
    
    if (filteredApps.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8">No applications to display</td></tr>';
        return;
    }
    
    tbody.innerHTML = filteredApps.map(app => {
        const company = companies.find(c => c.id === app.company_id);
        const companyName = company ? company.name : 'Unknown';
        const roleDisplay = app.job_url 
            ? `<a href="${escapeHtml(app.job_url)}" target="_blank" onclick="event.stopPropagation()" style="color: inherit; text-decoration: underline;">${escapeHtml(app.role)}</a>`
            : escapeHtml(app.role);
        return `
            <tr onclick="viewApplication(${app.id})" style="cursor: pointer;">
                <td><strong>${escapeHtml(companyName)}</strong></td>
                <td>${roleDisplay}</td>
                <td onclick="event.stopPropagation()">${renderMatchScore(app)}</td>
                <td><span class="badge badge-${app.priority.toLowerCase()}">${app.priority}</span></td>
                <td><span class="badge badge-${app.status.toLowerCase()}">${app.status}</span></td>
                <td>${app.salary_range ? escapeHtml(app.salary_range) : '-'}</td>
                <td>${app.date_applied ? new Date(app.date_applied).toLocaleDateString() : '-'}</td>
                <td onclick="event.stopPropagation()">
                    <button class="btn btn-info btn-sm" onclick="editApplication(${app.id})">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="deleteApplication(${app.id})">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

function openApplicationModal(applicationId = null, viewOnly = false) {
    currentApplication = applicationId;
    const modal = document.getElementById('applicationModal');
    const form = document.getElementById('applicationForm');
    const modalTitle = document.querySelector('#applicationModal .modal-header h2');
    const submitBtn = document.querySelector('#applicationModal button[type="submit"]');
    const pdfSection = document.getElementById('pdfFilesSection');
    
    // Update modal title
    if (viewOnly) {
        modalTitle.innerHTML = '<i class="fas fa-eye"></i> View Application';
        submitBtn.style.display = 'none';
    } else if (applicationId) {
        modalTitle.innerHTML = `<i class="fas fa-edit"></i> Edit Application (ID: ${applicationId})`;
        submitBtn.style.display = 'inline-flex';
    } else {
        modalTitle.innerHTML = '<i class="fas fa-plus"></i> Add Application';
        submitBtn.style.display = 'inline-flex';
    }
    
    if (applicationId) {
        const app = applications.find(a => a.id === applicationId);
        if (app) {
            document.getElementById('companyId').value = app.company_id;
            document.getElementById('role').value = app.role;
            document.getElementById('priority').value = app.priority;
            document.getElementById('status').value = app.status;
            document.getElementById('jobUrl').value = app.job_url || '';
            document.getElementById('resumeFilename').value = app.resume_filename || '';
            document.getElementById('coverLetterFilename').value = app.cover_letter_filename || '';
            document.getElementById('hiringManagerName').value = app.hiring_manager_name || '';
            document.getElementById('hiringManagerEmail').value = app.hiring_manager_email || '';
            document.getElementById('location').value = app.location || '';
            document.getElementById('remotePolicy').value = app.remote_policy || '';
            document.getElementById('salaryRange').value = app.salary_range || '';
            document.getElementById('appNotes').value = app.notes || '';
            
            // Load PDF files
            loadApplicationPDFs(applicationId);
            pdfSection.style.display = 'block';
        }
        
        // Disable all form inputs if view only
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.disabled = viewOnly;
        });
    } else {
        form.reset();
        pdfSection.style.display = 'none';
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.disabled = false;
        });
    }
    
    modal.classList.add('active');
}

function viewApplication(applicationId) {
    openApplicationModal(applicationId, true);
}

function editApplication(applicationId) {
    openApplicationModal(applicationId, false);
}

async function loadApplicationPDFs(applicationId) {
    try {
        const response = await fetch(`${API_BASE}/applications/${applicationId}/pdfs`);
        const data = await response.json();
        const pdfList = document.getElementById('pdfFilesList');
        
        console.log('Loading PDFs for application:', applicationId, 'Found:', data.pdfs?.length || 0);
        
        if (data.pdfs && data.pdfs.length > 0) {
            // Update resume/cover letter fields with actual filenames if found
            const resumeInput = document.getElementById('resumeFilename');
            const coverLetterInput = document.getElementById('coverLetterFilename');
            
            data.pdfs.forEach(pdf => {
                const lowerName = pdf.name.toLowerCase();
                if (lowerName.includes('resume') && !resumeInput.value) {
                    resumeInput.value = pdf.path;
                }
                if (lowerName.includes('cover') && !coverLetterInput.value) {
                    coverLetterInput.value = pdf.path;
                }
            });
            
            pdfList.innerHTML = data.pdfs.map(pdf => `
                <div class="pdf-file-item">
                    <i class="fas fa-file-pdf"></i>
                    <a href="/api/files/pdf/${pdf.path}" target="_blank">${escapeHtml(pdf.name)}</a>
                    <span class="pdf-file-size">${formatFileSize(pdf.size)}</span>
                </div>
            `).join('');
        } else {
            pdfList.innerHTML = '<p class="empty-state">No files found in application directory</p>';
        }
        
        // Setup drag and drop
        setupFileUpload(applicationId);
    } catch (error) {
        console.error('Error loading PDFs:', error);
        document.getElementById('pdfFilesList').innerHTML = '<p class="empty-state">Error loading files</p>';
    }
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function openCompanyModal() {
    const modal = document.getElementById('companyModal');
    document.getElementById('companyForm').reset();
    modal.classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

let currentCompany = null;

function openCompanyModal(companyId = null) {
    currentCompany = companyId;
    const modal = document.getElementById('companyModal');
    const form = document.getElementById('companyForm');
    
    if (companyId) {
        const company = companies.find(c => c.id === companyId);
        if (company) {
            document.getElementById('companyName').value = company.name;
            document.getElementById('website').value = company.website || '';
            document.getElementById('companySize').value = company.size || '';
            document.getElementById('techStack').value = company.tech_stack || '';
            document.getElementById('companyNotes').value = company.notes || '';
        }
        document.querySelector('#companyModal .modal-header h2').innerHTML = '<i class="fas fa-building"></i> Edit Company';
    } else {
        form.reset();
        document.querySelector('#companyModal .modal-header h2').innerHTML = '<i class="fas fa-building"></i> Add Company';
    }
    
    modal.classList.add('active');
}

async function handleApplicationSubmit(e) {
    e.preventDefault();
    
    const data = {
        company_id: parseInt(document.getElementById('companyId').value),
        role: document.getElementById('role').value,
        priority: document.getElementById('priority').value,
        status: document.getElementById('status').value,
        job_url: document.getElementById('jobUrl').value || null,
        resume_filename: document.getElementById('resumeFilename').value || null,
        cover_letter_filename: document.getElementById('coverLetterFilename').value || null,
        hiring_manager_name: document.getElementById('hiringManagerName').value || null,
        hiring_manager_email: document.getElementById('hiringManagerEmail').value || null,
        location: document.getElementById('location').value || null,
        remote_policy: document.getElementById('remotePolicy').value || null,
        salary_range: document.getElementById('salaryRange').value || null,
        notes: document.getElementById('appNotes').value || null
    };
    
    try {
        const url = currentApplication ? `${API_BASE}/applications/${currentApplication}` : `${API_BASE}/applications`;
        const method = currentApplication ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            const result = await response.json();
            closeModal('applicationModal');
            if (currentApplication) {
                // Edit: patch in-place to preserve scroll/sort position
                const idx = applications.findIndex(a => a.id === result.id);
                if (idx !== -1) applications[idx] = result;
                updateApplicationList();
            } else {
                // New application: full reload to include it
                await loadApplications();
            }
            loadDashboard();
            
            // If status changed to a closed status, show helpful message
            const closedStatuses = ['Rejected', 'Withdrawn', 'Accepted'];
            if (closedStatuses.includes(data.status) && !showClosedApps) {
                setTimeout(() => {
                    alert(`Application marked as "${data.status}". Enable "Show Closed" to view it in the list.`);
                }, 100);
            }
        } else {
            const error = await response.json();
            alert('Error saving application: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving application:', error);
        alert('Error saving application: ' + error.message);
    }
}

async function handleCompanySubmit(e) {
    e.preventDefault();
    
    const data = {
        name: document.getElementById('companyName').value,
        website: document.getElementById('website').value || null,
        size: document.getElementById('companySize').value || null,
        tech_stack: document.getElementById('techStack').value || null,
        notes: document.getElementById('companyNotes').value || null
    };
    
    try {
        const url = currentCompany 
            ? `${API_BASE}/companies/${currentCompany}`
            : `${API_BASE}/companies`;
        
        const method = currentCompany ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            closeModal('companyModal');
            loadCompanies();
        } else {
            const error = await response.json();
            alert(error.detail || 'Error saving company');
        }
    } catch (error) {
        console.error('Error saving company:', error);
        alert('Error saving company');
    }
}

function editCompany(id) {
    openCompanyModal(id);
}

async function deleteApplication(id) {
    if (!confirm('Delete this application?')) return;
    
    try {
        await fetch(`${API_BASE}/applications/${id}`, { method: 'DELETE' });
        loadApplications();
        loadDashboard();
    } catch (error) {
        console.error('Error deleting application:', error);
    }
}

async function deleteCompany(id) {
    if (!confirm('Delete this company?')) return;
    
    try {
        await fetch(`${API_BASE}/companies/${id}`, { method: 'DELETE' });
        loadCompanies();
        loadApplications();
    } catch (error) {
        console.error('Error deleting company:', error);
    }
}

function openImportJobsModal() {
    document.getElementById('jobUrls').value = '';
    document.getElementById('importProgress').style.display = 'none';
    document.getElementById('importResults').style.display = 'none';
    openModal('importJobsModal');
}

async function handleImportJobs(e) {
    e.preventDefault();
    
    const urls = document.getElementById('jobUrls').value;
    const progressDiv = document.getElementById('importProgress');
    const resultsDiv = document.getElementById('importResults');
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    progressDiv.style.display = 'block';
    resultsDiv.style.display = 'none';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/jobs/import-urls`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ urls: urls })
        });
        
        const result = await response.json();
        
        progressDiv.style.display = 'none';
        resultsDiv.style.display = 'block';
        
        let html = '<div style="padding: 15px; background: var(--bg-primary); border-radius: 8px;">';
        
        if (result.success > 0) {
            html += `<div style="color: var(--sol-green); margin-bottom: 10px;">
                <i class="fas fa-check-circle"></i> Successfully imported ${result.success} job(s)
            </div>`;
            
            html += '<div style="margin-top: 10px;"><strong>Imported Jobs:</strong><ul style="margin: 5px 0; padding-left: 20px;">';
            result.created.forEach(job => {
                html += `<li>${escapeHtml(job.company)} - ${escapeHtml(job.role)}</li>`;
            });
            html += '</ul></div>';
        }
        
        if (result.failed > 0) {
            html += `<div style="color: var(--sol-orange); margin-top: 15px;">
                <i class="fas fa-exclamation-triangle"></i> ${result.failed} job(s) failed to import
            </div>`;
            
            html += '<div style="margin-top: 10px;"><strong>Errors:</strong><ul style="margin: 5px 0; padding-left: 20px;">';
            result.errors.forEach(err => {
                html += `<li style="color: var(--sol-red); font-size: 0.9em;">${escapeHtml(err.error)}</li>`;
            });
            html += '</ul></div>';
        }
        
        html += '</div>';
        html += '<div style="margin-top: 15px;"><button class="btn btn-primary" onclick="closeImportAndReload()">Done</button></div>';
        
        resultsDiv.innerHTML = html;
        
    } catch (error) {
        progressDiv.style.display = 'none';
        resultsDiv.style.display = 'block';
        resultsDiv.innerHTML = `
            <div style="color: var(--sol-red); padding: 15px;">
                <i class="fas fa-times-circle"></i> Error: ${escapeHtml(error.message)}
            </div>
        `;
    } finally {
        submitBtn.disabled = false;
    }
}

function closeImportAndReload() {
    closeModal('importJobsModal');
    loadApplications();
    loadDashboard();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// MA DUA Export Functions
let currentDUAReport = '';
let currentDUAWeekStart = '';

function openDUAExportModal() {
    document.getElementById('duaPreview').style.display = 'none';
    document.getElementById('duaCopyBtn').style.display = 'none';
    document.getElementById('duaDownloadBtn').style.display = 'none';
    document.getElementById('duaWeekStart').value = '';
    currentDUAReport = '';
    openModal('duaExportModal');
}

function getLastSunday(date) {
    const d = new Date(date);
    const day = d.getDay();
    const diff = day === 0 ? 0 : day;
    d.setDate(d.getDate() - diff);
    return d;
}

async function selectDUAWeek(period) {
    const today = new Date();
    let weekStart;
    
    if (period === 'this') {
        weekStart = getLastSunday(today);
    } else if (period === 'last') {
        const lastWeek = new Date(today);
        lastWeek.setDate(lastWeek.getDate() - 7);
        weekStart = getLastSunday(lastWeek);
    }
    
    const weekStartStr = weekStart.toISOString().split('T')[0];
    document.getElementById('duaWeekStart').value = weekStartStr;
    await loadDUAReport(weekStartStr);
}

const duaWeekStartInput = document.getElementById('duaWeekStart');
if (duaWeekStartInput) {
    duaWeekStartInput.addEventListener('change', async (e) => {
        if (e.target.value) {
            const selectedDate = new Date(e.target.value);
            const sunday = getLastSunday(selectedDate);
            const weekStartStr = sunday.toISOString().split('T')[0];
            e.target.value = weekStartStr;
            await loadDUAReport(weekStartStr);
        }
    });
}

async function loadDUAReport(weekStart) {
    try {
        const response = await fetch(`${API_BASE}/reports/dua-weekly?week_start=${weekStart}`);
        const report = await response.text();
        
        currentDUAReport = report;
        currentDUAWeekStart = weekStart;
        
        document.getElementById('duaPreviewText').textContent = report;
        document.getElementById('duaPreview').style.display = 'block';
        document.getElementById('duaCopyBtn').style.display = 'inline-block';
        document.getElementById('duaDownloadBtn').style.display = 'inline-block';
    } catch (error) {
        alert('Error loading report: ' + error.message);
    }
}

function copyDUAReport() {
    navigator.clipboard.writeText(currentDUAReport).then(() => {
        const btn = document.getElementById('duaCopyBtn');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        setTimeout(() => {
            btn.innerHTML = originalText;
        }, 2000);
    }).catch(err => {
        alert('Failed to copy to clipboard: ' + err);
    });
}

function downloadDUAReport() {
    const blob = new Blob([currentDUAReport], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `MA_DUA_Activity_${currentDUAWeekStart}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// File Upload Functions
function setupFileUpload(applicationId) {
    const uploadZone = document.getElementById('fileUploadZone');
    const fileInput = document.getElementById('fileInput');
    
    if (!uploadZone || !fileInput) return;
    
    // Click to upload
    uploadZone.onclick = () => fileInput.click();
    
    // File input change
    fileInput.onchange = (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(applicationId, e.target.files);
        }
    };
    
    // Drag and drop
    uploadZone.ondragover = (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.add('drag-over');
    };
    
    uploadZone.ondragleave = (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.remove('drag-over');
    };
    
    uploadZone.ondrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.remove('drag-over');
        
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(applicationId, e.dataTransfer.files);
        }
    };
}

async function handleFileUpload(applicationId, files) {
    const progressDiv = document.getElementById('uploadProgress');
    const fileInput = document.getElementById('fileInput');
    progressDiv.style.display = 'block';
    
    try {
        for (const file of files) {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch(`${API_BASE}/applications/${applicationId}/upload`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Upload failed');
            }
        }
        
        // Reset file input
        fileInput.value = '';
        
        // Reload PDFs list
        await loadApplicationPDFs(applicationId);
        
        // Show success message briefly
        progressDiv.innerHTML = '<i class="fas fa-check-circle"></i> Upload complete!';
        setTimeout(() => {
            progressDiv.style.display = 'none';
            progressDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
        }, 2000);
        
    } catch (error) {
        console.error('Upload error:', error);
        fileInput.value = '';
        progressDiv.innerHTML = `<i class="fas fa-times-circle"></i> Error: ${error.message}`;
        setTimeout(() => {
            progressDiv.style.display = 'none';
            progressDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
        }, 3000);
    }
}

// ==================== BULK JOB SCORING ====================

// Actions dropdown toggle
document.getElementById('actionsDropdownBtn')?.addEventListener('click', (e) => {
    e.stopPropagation();
    const menu = document.getElementById('actionsDropdownMenu');
    menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
});

// Close dropdown when clicking outside
document.addEventListener('click', () => {
    const menu = document.getElementById('actionsDropdownMenu');
    if (menu) menu.style.display = 'none';
});

// Score Pipeline Jobs button
document.getElementById('scorePipelineBtn')?.addEventListener('click', () => {
    document.getElementById('actionsDropdownMenu').style.display = 'none';
    openModal('bulkScoringModal');
    resetScoringModal();
});

// Bulk Import button
document.getElementById('bulkImportBtn')?.addEventListener('click', () => {
    document.getElementById('actionsDropdownMenu').style.display = 'none';
    
    // Reset modal state
    const form = document.getElementById('bulkImportForm');
    const cancelBtn = form.querySelector('button.btn-secondary');
    const submitBtn = form.querySelector('button[type="submit"]');
    const progress = document.getElementById('bulkImportProgress');
    const results = document.getElementById('bulkImportResults');
    
    cancelBtn.innerHTML = '<i class="fas fa-times"></i> Cancel';
    submitBtn.style.display = '';
    submitBtn.disabled = false;
    progress.style.display = 'none';
    results.style.display = 'none';
    
    openModal('bulkImportModal');
});

function resetScoringModal() {
    document.getElementById('scoringStep1').style.display = 'block';
    document.getElementById('scoringStep2').style.display = 'none';
    document.getElementById('scoringStep3').style.display = 'none';
    document.getElementById('promptStatus').style.display = 'none';
    document.getElementById('parseStatus').style.display = 'none';
    document.getElementById('scoringPrompt').value = '';
    document.getElementById('aiResponse').value = '';
    document.getElementById('rescoreCheckbox').checked = false;
}

// Generate Prompt button
document.getElementById('generatePromptBtn')?.addEventListener('click', async () => {
    const btn = document.getElementById('generatePromptBtn');
    const status = document.getElementById('promptStatus');
    const rescore = document.getElementById('rescoreCheckbox').checked;
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    status.style.display = 'block';
    status.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Fetching Pipeline applications...';
    
    try {
        const response = await fetch(`${API_BASE}/applications/bulk-score`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                status_filter: 'Pipeline', 
                use_api: false,
                rescore: rescore
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate prompt');
        }
        
        const data = await response.json();
        
        document.getElementById('scoringPrompt').value = data.prompt;
        document.getElementById('promptAppCount').textContent = data.application_count;
        
        // Show step 2 and 3
        document.getElementById('scoringStep2').style.display = 'block';
        document.getElementById('scoringStep3').style.display = 'block';
        
        status.innerHTML = `<i class="fas fa-check-circle" style="color: var(--success-color);"></i> Generated prompt for ${data.application_count} applications`;
        
    } catch (error) {
        console.error('Error generating prompt:', error);
        status.innerHTML = `<i class="fas fa-times-circle" style="color: var(--danger-color);"></i> Error: ${error.message}`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-magic"></i> Generate Scoring Prompt';
    }
});

// Copy Prompt button
document.getElementById('copyPromptBtn')?.addEventListener('click', async () => {
    const prompt = document.getElementById('scoringPrompt').value;
    const btn = document.getElementById('copyPromptBtn');
    
    try {
        await navigator.clipboard.writeText(prompt);
        const originalHTML = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        setTimeout(() => {
            btn.innerHTML = originalHTML;
        }, 2000);
    } catch (error) {
        console.error('Failed to copy:', error);
        alert('Failed to copy to clipboard');
    }
});

// Parse Scores button
document.getElementById('parseScoresBtn')?.addEventListener('click', async () => {
    const aiResponse = document.getElementById('aiResponse').value.trim();
    const btn = document.getElementById('parseScoresBtn');
    const status = document.getElementById('parseStatus');
    
    if (!aiResponse) {
        status.style.display = 'block';
        status.innerHTML = '<i class="fas fa-exclamation-triangle" style="color: var(--warning-color);"></i> Please paste the AI response';
        return;
    }
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Parsing...';
    status.style.display = 'block';
    status.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Updating database...';
    
    try {
        const response = await fetch(`${API_BASE}/applications/parse-scores`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ai_response: aiResponse })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to parse scores');
        }
        
        const data = await response.json();
        
        status.innerHTML = `<i class="fas fa-check-circle" style="color: var(--success-color);"></i> Updated ${data.updated} applications` +
            (data.failed > 0 ? ` <span style="color: var(--warning-color);">(${data.failed} failed)</span>` : '');
        
        // Reload applications table
        setTimeout(() => {
            loadApplications();
            closeModal('bulkScoringModal');
        }, 2000);
        
    } catch (error) {
        console.error('Error parsing scores:', error);
        status.innerHTML = `<i class="fas fa-times-circle" style="color: var(--danger-color);"></i> Error: ${error.message}`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-database"></i> Parse & Update Scores';
    }
});

// Render match score badge
function renderMatchScore(app) {
    if (!app.match_score) {
        return '<span class="match-score-none">—</span>';
    }
    
    const score = app.match_score;
    let badgeClass = 'match-score-poor';
    
    if (score >= 80) badgeClass = 'match-score-excellent';
    else if (score >= 70) badgeClass = 'match-score-strong';
    else if (score >= 60) badgeClass = 'match-score-good';
    else if (score >= 50) badgeClass = 'match-score-moderate';
    
    const tooltip = app.match_reasoning ? `data-tooltip="${escapeHtml(app.match_reasoning)}"` : '';
    
    return `<span class="match-score-badge ${badgeClass}" ${tooltip} onclick="showMatchDetails(${app.id})">${score}</span>`;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/"/g, '&quot;');
}

function showMatchDetails(appId) {
    // Find the application
    const app = applications.find(a => a.id === appId);
    if (!app || !app.match_score) return;
    
    // Show details in a simple alert for now (could be a modal later)
    let message = `Match Score: ${app.match_score}\n`;
    message += `Recommendation: ${app.match_recommendation || 'N/A'}\n\n`;
    message += `Reasoning:\n${app.match_reasoning || 'N/A'}\n\n`;
    
    if (app.match_strengths) {
        try {
            const strengths = JSON.parse(app.match_strengths);
            message += `Strengths:\n${strengths.map(s => `• ${s}`).join('\n')}\n\n`;
        } catch (e) {}
    }
    
    if (app.match_gaps) {
        try {
            const gaps = JSON.parse(app.match_gaps);
            message += `Gaps:\n${gaps.map(g => `• ${g}`).join('\n')}`;
        } catch (e) {}
    }
    
    alert(message);
}

// Bulk import form handler
document.getElementById('bulkImportForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const textarea = document.getElementById('bulkImportUrls');
    const progress = document.getElementById('bulkImportProgress');
    const results = document.getElementById('bulkImportResults');
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    // Parse URLs from textarea
    const urls = textarea.value
        .split('\n')
        .map(url => url.trim())
        .filter(url => url.length > 0);
    
    if (urls.length === 0) {
        alert('Please enter at least one URL');
        return;
    }
    
    // Show progress
    progress.style.display = 'block';
    results.style.display = 'none';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/applications/bulk-import`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ urls })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to import applications');
        }
        
        const data = await response.json();
        
        // Hide progress, show results
        progress.style.display = 'none';
        results.style.display = 'block';
        
        // Build results HTML
        let html = '<div style="max-height: 300px; overflow-y: auto;">';
        
        // Summary
        html += `<div style="margin-bottom: 15px; padding: 12px; background: var(--card-bg); border-radius: 6px;">`;
        html += `<strong>Import Summary:</strong><br>`;
        html += `<span style="color: var(--success-color);">✓ Created: ${data.summary.created}</span><br>`;
        html += `<span style="color: var(--warning-color);">⊘ Skipped: ${data.summary.skipped}</span><br>`;
        html += `<span style="color: var(--danger-color);">✗ Failed: ${data.summary.failed}</span>`;
        html += `</div>`;
        
        // Created applications
        if (data.details.created && data.details.created.length > 0) {
            html += `<div style="margin-bottom: 15px;"><strong style="color: var(--success-color);">Created Applications:</strong><ul style="margin-top: 8px;">`;
            data.details.created.forEach(item => {
                html += `<li>${item.company} - ${item.role}</li>`;
            });
            html += `</ul></div>`;
        }
        
        // Skipped URLs
        if (data.details.skipped && data.details.skipped.length > 0) {
            html += `<div style="margin-bottom: 15px;"><strong style="color: var(--warning-color);">Skipped URLs:</strong><ul style="margin-top: 8px;">`;
            data.details.skipped.forEach(item => {
                html += `<li><small>${item.url}</small><br><em style="color: var(--text-secondary); font-size: 0.9em;">${item.reason}</em></li>`;
            });
            html += `</ul></div>`;
        }
        
        // Failed URLs
        if (data.details.failed && data.details.failed.length > 0) {
            html += `<div style="margin-bottom: 15px;"><strong style="color: var(--danger-color);">Failed URLs:</strong><ul style="margin-top: 8px;">`;
            data.details.failed.forEach(item => {
                html += `<li><small>${item.url}</small><br><em style="color: var(--text-secondary); font-size: 0.9em;">${item.error}</em></li>`;
            });
            html += `</ul></div>`;
        }
        
        html += '</div>';
        
        results.innerHTML = html;
        
        // Clear form
        textarea.value = '';
        
        // Change buttons after completion
        const cancelBtn = e.target.querySelector('button.btn-secondary');
        cancelBtn.innerHTML = '<i class="fas fa-check"></i> Close';
        submitBtn.style.display = 'none';
        
        // Reload applications if any were created
        if (data.summary.created > 0) {
            setTimeout(() => {
                loadApplications();
            }, 2000);
        }
        
    } catch (error) {
        console.error('Error importing URLs:', error);
        progress.style.display = 'none';
        results.style.display = 'block';
        results.innerHTML = `<div class="alert alert-danger"><i class="fas fa-times-circle"></i> Error: ${error.message}</div>`;
        
        // Change buttons on error too
        const cancelBtn = e.target.querySelector('button.btn-secondary');
        cancelBtn.innerHTML = '<i class="fas fa-times"></i> Close';
        submitBtn.style.display = 'none';
    } finally {
        submitBtn.disabled = false;
    }
});
