// Interviews management
let interviews = [];
let currentInterview = null;
let calendarView = false;

document.addEventListener('DOMContentLoaded', () => {
    const interviewsTab = document.querySelector('[data-tab="interviews"]');
    if (interviewsTab) {
        interviewsTab.addEventListener('click', () => {
            calendarView = false;
            loadInterviews();
        });
    }
    
    const addBtn = document.getElementById('addInterviewBtn');
    if (addBtn) {
        addBtn.addEventListener('click', () => openInterviewModal());
    }
    
    const calendarBtn = document.getElementById('viewCalendarBtn');
    if (calendarBtn) {
        calendarBtn.addEventListener('click', toggleCalendarView);
    }
    
    const form = document.getElementById('interviewForm');
    if (form) {
        form.addEventListener('submit', handleInterviewSubmit);
    }
    
    document.querySelectorAll('.close-modal').forEach(btn => {
        btn.addEventListener('click', () => {
            closeModal(btn.closest('.modal').id);
        });
    });
});

async function loadInterviews() {
    try {
        // Load all interviews across all applications
        const appIds = applications.map(a => a.id);
        const allInterviews = [];
        
        for (const appId of appIds) {
            const response = await fetch(`${API_BASE}/applications/${appId}/interviews`);
            if (response.ok) {
                const data = await response.json();
                allInterviews.push(...data);
            }
        }
        
        interviews = allInterviews;
        
        if (calendarView) {
            displayCalendarView();
        } else {
            displayInterviewsList();
        }
    } catch (error) {
        console.error('Error loading interviews:', error);
    }
}

function displayInterviewsList() {
    const container = document.getElementById('interviewsContainer');
    
    if (interviews.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-calendar-times"></i>
                <p>No interviews scheduled yet. Add your first interview!</p>
            </div>
        `;
        return;
    }
    
    // Sort by date
    const sorted = [...interviews].sort((a, b) => {
        const dateA = a.scheduled_date ? new Date(a.scheduled_date) : new Date(0);
        const dateB = b.scheduled_date ? new Date(b.scheduled_date) : new Date(0);
        return dateA - dateB;
    });
    
    // Group by upcoming vs past
    const now = new Date();
    const upcoming = sorted.filter(i => !i.scheduled_date || new Date(i.scheduled_date) >= now);
    const past = sorted.filter(i => i.scheduled_date && new Date(i.scheduled_date) < now);
    
    container.innerHTML = `
        ${upcoming.length > 0 ? `
            <div class="interview-section">
                <h3><i class="fas fa-arrow-right"></i> Upcoming Interviews & Meetings</h3>
                ${upcoming.map(interview => renderInterviewCard(interview)).join('')}
            </div>
        ` : ''}
        
        ${past.length > 0 ? `
            <div class="interview-section">
                <h3><i class="fas fa-history"></i> Past Interviews</h3>
                ${past.map(interview => renderInterviewCard(interview)).join('')}
            </div>
        ` : ''}
    `;
}

function renderInterviewCard(interview) {
    const app = applications.find(a => a.id === interview.application_id);
    const company = app ? companies.find(c => c.id === app.company_id) : null;
    const companyName = company ? company.name : 'Unknown';
    const role = app ? app.role : 'Unknown Role';
    
    const date = interview.scheduled_date ? new Date(interview.scheduled_date) : null;
    const dateStr = date ? date.toLocaleDateString('en-US', { 
        weekday: 'short', 
        month: 'short', 
        day: 'numeric', 
        year: 'numeric' 
    }) : 'Not scheduled';
    const timeStr = date ? date.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit' 
    }) : '';
    
    const isPast = date && date < new Date();
    const isToday = date && date.toDateString() === new Date().toDateString();
    const isTomorrow = date && date.toDateString() === new Date(Date.now() + 86400000).toDateString();
    
    let dateLabel = dateStr;
    if (isToday) dateLabel = '🔴 Today - ' + dateStr;
    if (isTomorrow) dateLabel = '🟡 Tomorrow - ' + dateStr;
    
    return `
        <div class="interview-card ${isPast ? 'interview-past' : ''} ${isToday ? 'interview-today' : ''}">
            <div class="interview-header">
                <div>
                    <h4>${escapeHtml(companyName)} - ${escapeHtml(role)}</h4>
                    <span class="interview-type">${interview.interview_type || 'Interview'}</span>
                    ${interview.completed === 'Yes' ? '<span class="badge badge-accepted">Completed</span>' : ''}
                </div>
                <div>
                    <button class="btn btn-secondary btn-sm" onclick="editInterview(${interview.id})">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="deleteInterview(${interview.id})">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </div>
            
            <div class="interview-details">
                <div class="interview-detail">
                    <i class="fas fa-calendar"></i>
                    <strong>${dateLabel}</strong>
                </div>
                
                ${timeStr ? `
                    <div class="interview-detail">
                        <i class="fas fa-clock"></i>
                        ${timeStr}
                    </div>
                ` : ''}
                
                ${interview.interviewer_name ? `
                    <div class="interview-detail">
                        <i class="fas fa-user"></i>
                        ${escapeHtml(interview.interviewer_name)}
                        ${interview.interviewer_title ? ` - ${escapeHtml(interview.interviewer_title)}` : ''}
                    </div>
                ` : ''}
                
                ${interview.interviewer_email ? `
                    <div class="interview-detail">
                        <i class="fas fa-envelope"></i>
                        <a href="mailto:${interview.interviewer_email}">${interview.interviewer_email}</a>
                    </div>
                ` : ''}
                
                ${interview.location ? `
                    <div class="interview-detail">
                        <i class="fas fa-map-marker-alt"></i>
                        ${escapeHtml(interview.location)}
                    </div>
                ` : ''}
                
                ${interview.meeting_link ? `
                    <div class="interview-detail">
                        <i class="fas fa-video"></i>
                        <a href="${interview.meeting_link}" target="_blank">Join Meeting</a>
                    </div>
                ` : ''}
                
                ${interview.notes ? `
                    <div class="interview-notes">
                        <i class="fas fa-sticky-note"></i>
                        <div>${escapeHtml(interview.notes).replace(/\n/g, '<br>')}</div>
                    </div>
                ` : ''}
            </div>
        </div>
    `;
}

function displayCalendarView() {
    const container = document.getElementById('interviewsContainer');
    
    if (interviews.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-calendar-times"></i>
                <p>No interviews to display in calendar.</p>
            </div>
        `;
        return;
    }
    
    // Simple week view - show last 2 weeks and next 3 weeks
    const today = new Date();
    const startOfWeek = new Date(today);
    startOfWeek.setDate(today.getDate() - today.getDay());
    // Go back 2 weeks from the current week
    startOfWeek.setDate(startOfWeek.getDate() - (2 * 7));
    
    const weeks = [];
    for (let w = 0; w < 5; w++) {
        const week = [];
        for (let d = 0; d < 7; d++) {
            const date = new Date(startOfWeek);
            date.setDate(startOfWeek.getDate() + (w * 7) + d);
            
            const dayInterviews = interviews.filter(i => {
                if (!i.scheduled_date) return false;
                const iDate = new Date(i.scheduled_date);
                return iDate.toDateString() === date.toDateString();
            });
            
            week.push({ date, interviews: dayInterviews });
        }
        weeks.push(week);
    }
    
    container.innerHTML = `
        <div class="calendar-view">
            <div class="calendar-header">
                <h3>Last 2 Weeks & Next 3 Weeks</h3>
            </div>
            
            <div class="calendar-grid">
                <div class="calendar-day-header">Sun</div>
                <div class="calendar-day-header">Mon</div>
                <div class="calendar-day-header">Tue</div>
                <div class="calendar-day-header">Wed</div>
                <div class="calendar-day-header">Thu</div>
                <div class="calendar-day-header">Fri</div>
                <div class="calendar-day-header">Sat</div>
                
                ${weeks.map(week => week.map(day => {
                    const isToday = day.date.toDateString() === today.toDateString();
                    const isPast = day.date < today && !isToday;
                    
                    return `
                        <div class="calendar-day ${isToday ? 'calendar-today' : ''} ${isPast ? 'calendar-past' : ''}">
                            <div class="calendar-day-number">${day.date.getDate()}</div>
                            ${day.interviews.length > 0 ? `
                                <div class="calendar-interviews">
                                    ${day.interviews.map(i => {
                                        const app = applications.find(a => a.id === i.application_id);
                                        const company = app ? companies.find(c => c.id === app.company_id) : null;
                                        const time = new Date(i.scheduled_date).toLocaleTimeString('en-US', { 
                                            hour: 'numeric', 
                                            minute: '2-digit' 
                                        });
                                        return `
                                            <div class="calendar-interview" onclick="editInterview(${i.id})">
                                                <div class="calendar-interview-time">${time}</div>
                                                <div class="calendar-interview-company">${company ? company.name : 'Unknown'}</div>
                                            </div>
                                        `;
                                    }).join('')}
                                </div>
                            ` : ''}
                        </div>
                    `;
                }).join('')).join('')}
            </div>
        </div>
    `;
}

function toggleCalendarView() {
    calendarView = !calendarView;
    const btn = document.getElementById('viewCalendarBtn');
    
    if (calendarView) {
        btn.innerHTML = '<i class="fas fa-list"></i> List View';
        displayCalendarView();
    } else {
        btn.innerHTML = '<i class="fas fa-calendar"></i> Calendar View';
        displayInterviewsList();
    }
}

function openInterviewModal(interviewId = null) {
    currentInterview = interviewId;
    const modal = document.getElementById('interviewModal');
    const form = document.getElementById('interviewForm');
    
    // Populate company dropdown
    const select = document.getElementById('interviewCompany');
    select.innerHTML = '<option value="">Select...</option>' +
        applications.map(app => {
            const company = companies.find(c => c.id === app.company_id);
            return `<option value="${app.id}">${company ? company.name : 'Unknown'} - ${app.role}</option>`;
        }).join('');
    
    if (interviewId) {
        const interview = interviews.find(i => i.id === interviewId);
        if (interview) {
            document.getElementById('interviewCompany').value = interview.application_id;
            document.getElementById('interviewType').value = interview.interview_type || '';
            
            if (interview.scheduled_date) {
                const date = new Date(interview.scheduled_date);
                document.getElementById('scheduledDate').value = date.toISOString().split('T')[0];
                document.getElementById('scheduledTime').value = date.toTimeString().slice(0, 5);
            }
            
            document.getElementById('interviewerName').value = interview.interviewer_name || '';
            document.getElementById('interviewerTitle').value = interview.interviewer_title || '';
            document.getElementById('interviewerEmail').value = interview.interviewer_email || '';
            document.getElementById('interviewLocation').value = interview.location || '';
            document.getElementById('meetingLink').value = interview.meeting_link || '';
            document.getElementById('interviewNotes').value = interview.notes || '';
            document.getElementById('completed').value = interview.completed || 'No';
        }
        document.getElementById('interviewModalTitle').textContent = 'Edit Interview/Meeting';
    } else {
        form.reset();
        // Populate dropdown again after reset
        select.innerHTML = '<option value="">Select...</option>' +
            applications.map(app => {
                const company = companies.find(c => c.id === app.company_id);
                return `<option value="${app.id}">${company ? company.name : 'Unknown'} - ${app.role}</option>`;
            }).join('');
        document.getElementById('interviewModalTitle').textContent = 'Add Interview/Meeting';
    }
    
    modal.classList.add('active');
}

async function handleInterviewSubmit(e) {
    e.preventDefault();
    
    const dateStr = document.getElementById('scheduledDate').value;
    const timeStr = document.getElementById('scheduledTime').value;
    const scheduledDate = dateStr && timeStr ? `${dateStr}T${timeStr}:00` : null;
    
    const data = {
        application_id: parseInt(document.getElementById('interviewCompany').value),
        interview_type: document.getElementById('interviewType').value,
        scheduled_date: scheduledDate,
        interviewer_name: document.getElementById('interviewerName').value || null,
        interviewer_title: document.getElementById('interviewerTitle').value || null,
        interviewer_email: document.getElementById('interviewerEmail').value || null,
        location: document.getElementById('interviewLocation').value || null,
        meeting_link: document.getElementById('meetingLink').value || null,
        notes: document.getElementById('interviewNotes').value || null,
        completed: document.getElementById('completed').value
    };
    
    try {
        const url = currentInterview 
            ? `${API_BASE}/interviews/${currentInterview}`
            : `${API_BASE}/interviews`;
        
        const method = currentInterview ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            closeModal('interviewModal');
            loadInterviews();
        } else {
            alert('Error saving interview');
        }
    } catch (error) {
        console.error('Error saving interview:', error);
        alert('Error saving interview');
    }
}

function editInterview(id) {
    openInterviewModal(id);
}

async function deleteInterview(id) {
    if (!confirm('Delete this interview?')) return;
    
    try {
        await fetch(`${API_BASE}/interviews/${id}`, { method: 'DELETE' });
        loadInterviews();
    } catch (error) {
        console.error('Error deleting interview:', error);
    }
}
