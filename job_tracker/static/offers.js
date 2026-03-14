// Offers management
let offers = [];
let currentOffer = null;

document.addEventListener('DOMContentLoaded', () => {
    const offersTab = document.querySelector('[data-tab="offers"]');
    if (offersTab) {
        offersTab.addEventListener('click', loadOffers);
    }
    
    const compareBtn = document.getElementById('compareOffersBtn');
    if (compareBtn) {
        compareBtn.addEventListener('click', showOfferComparison);
    }
});

async function loadOffers() {
    try {
        const response = await fetch(`${API_BASE}/offers`);
        offers = await response.json();
        displayOffers();
    } catch (error) {
        console.error('Error loading offers:', error);
    }
}

function displayOffers() {
    const container = document.getElementById('offersContainer');
    
    if (offers.length === 0) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-gift"></i><p>No offers yet. Add offers from applications with "Offer" status.</p></div>';
        return;
    }
    
    container.innerHTML = offers.map(offer => {
        const app = applications.find(a => a.id === offer.application_id);
        const company = app ? companies.find(c => c.id === app.company_id) : null;
        const companyName = company ? company.name : 'Unknown';
        const role = app ? app.role : 'Unknown Role';
        
        return `
            <div class="offer-card">
                <div class="offer-header">
                    <div>
                        <h3>${escapeHtml(companyName)} - ${escapeHtml(role)}</h3>
                        <span class="badge badge-${offer.status.toLowerCase()}">${offer.status}</span>
                    </div>
                    <div>
                        <button class="btn btn-secondary btn-sm" onclick="editOffer(${offer.id})">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button class="btn btn-danger btn-sm" onclick="deleteOffer(${offer.id})">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </div>
                
                <div class="offer-details">
                    <div class="offer-section">
                        <h4><i class="fas fa-dollar-sign"></i> Compensation</h4>
                        <div class="offer-grid">
                            <div class="offer-item">
                                <span class="label">Base Salary:</span>
                                <span class="value">${formatMoney(offer.base_salary)}</span>
                            </div>
                            <div class="offer-item">
                                <span class="label">Bonus:</span>
                                <span class="value">${formatMoney(offer.bonus_target)}</span>
                            </div>
                            <div class="offer-item">
                                <span class="label">Signing:</span>
                                <span class="value">${formatMoney(offer.signing_bonus)}</span>
                            </div>
                            <div class="offer-item">
                                <span class="label">Equity (annual):</span>
                                <span class="value">${formatMoney(offer.equity_value)}</span>
                            </div>
                            <div class="offer-item highlight">
                                <span class="label">Total Comp:</span>
                                <span class="value">${formatMoney(offer.total_comp)}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="offer-section">
                        <h4><i class="fas fa-umbrella"></i> Benefits & Time Off</h4>
                        <div class="offer-grid">
                            <div class="offer-item">
                                <span class="label">PTO:</span>
                                <span class="value">${offer.pto_days || 0} days</span>
                            </div>
                            <div class="offer-item">
                                <span class="label">Sick:</span>
                                <span class="value">${offer.sick_days || 0} days</span>
                            </div>
                            <div class="offer-item">
                                <span class="label">Holidays:</span>
                                <span class="value">${offer.holidays || 0} days</span>
                            </div>
                            <div class="offer-item">
                                <span class="label">Total Days Off:</span>
                                <span class="value">${(offer.pto_days || 0) + (offer.sick_days || 0) + (offer.holidays || 0)} days</span>
                            </div>
                        </div>
                        ${offer.health_insurance ? `<p><i class="fas fa-heart"></i> ${offer.health_insurance}</p>` : ''}
                        ${offer.retirement_match ? `<p><i class="fas fa-piggy-bank"></i> ${offer.retirement_match}</p>` : ''}
                    </div>
                    
                    <div class="offer-section">
                        <h4><i class="fas fa-briefcase"></i> Work Details</h4>
                        <p><i class="fas fa-home"></i> ${offer.remote_policy || 'Not specified'}</p>
                        ${offer.relocation_assistance ? `<p><i class="fas fa-truck-moving"></i> ${offer.relocation_assistance}</p>` : ''}
                        ${offer.response_deadline ? `<p><i class="fas fa-calendar-times"></i> Deadline: ${new Date(offer.response_deadline).toLocaleDateString()}</p>` : ''}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

async function showOfferComparison() {
    try {
        const response = await fetch(`${API_BASE}/offers/compare/all`);
        const data = await response.json();
        displayOfferComparison(data);
    } catch (error) {
        console.error('Error loading offer comparison:', error);
    }
}

function displayOfferComparison(data) {
    const container = document.getElementById('offersContainer');
    
    if (data.offers.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No offers to compare yet.</p></div>';
        return;
    }
    
    // Calculate totals for comparison
    const sorted = [...data.offers].sort((a, b) => (b.total_comp || 0) - (a.total_comp || 0));
    
    container.innerHTML = `
        <div class="comparison-view">
            <div class="comparison-header">
                <h3><i class="fas fa-chart-bar"></i> Offer Comparison</h3>
                <button class="btn btn-secondary" onclick="loadOffers()">
                    <i class="fas fa-list"></i> Back to List
                </button>
            </div>
            
            <div class="comparison-table-container">
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Company / Role</th>
                            <th>Base Salary</th>
                            <th>Bonus</th>
                            <th>Equity</th>
                            <th>Total Comp</th>
                            <th>Days Off</th>
                            <th>Remote</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${sorted.map(offer => {
                            const app = applications.find(a => a.id === offer.application_id);
                            const company = app ? companies.find(c => c.id === app.company_id) : null;
                            const totalDaysOff = (offer.pto_days || 0) + (offer.sick_days || 0) + (offer.holidays || 0);
                            
                            return `
                                <tr class="${offer.status === 'Accepted' ? 'row-highlight' : ''}">
                                    <td>
                                        <strong>${company ? company.name : 'Unknown'}</strong><br>
                                        <small>${app ? app.role : 'Unknown'}</small>
                                    </td>
                                    <td>${formatMoney(offer.base_salary)}</td>
                                    <td>${formatMoney(offer.bonus_target)}</td>
                                    <td>${formatMoney(offer.equity_value)}</td>
                                    <td class="highlight">${formatMoney(offer.total_comp)}</td>
                                    <td>${totalDaysOff} days</td>
                                    <td>${offer.remote_policy || '-'}</td>
                                    <td><span class="badge badge-${offer.status.toLowerCase()}">${offer.status}</span></td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            </div>
            
            <div class="comparison-insights">
                <h4><i class="fas fa-lightbulb"></i> Quick Insights</h4>
                <div class="insights-grid">
                    <div class="insight-card">
                        <div class="insight-label">Highest Total Comp</div>
                        <div class="insight-value">${formatMoney(sorted[0]?.total_comp)}</div>
                    </div>
                    <div class="insight-card">
                        <div class="insight-label">Average Total Comp</div>
                        <div class="insight-value">${formatMoney(Math.round(sorted.reduce((sum, o) => sum + (o.total_comp || 0), 0) / sorted.length))}</div>
                    </div>
                    <div class="insight-card">
                        <div class="insight-label">Most Days Off</div>
                        <div class="insight-value">${Math.max(...sorted.map(o => (o.pto_days || 0) + (o.sick_days || 0) + (o.holidays || 0)))} days</div>
                    </div>
                    <div class="insight-card">
                        <div class="insight-label">Pending Offers</div>
                        <div class="insight-value">${sorted.filter(o => o.status === 'Pending' || o.status === 'Negotiating').length}</div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function formatMoney(amount) {
    if (!amount) return '-';
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

function editOffer(offerId) {
    // TODO: Implement offer edit modal
    alert('Offer editing coming soon! Offer ID: ' + offerId);
}

async function deleteOffer(offerId) {
    if (!confirm('Delete this offer?')) return;
    
    try {
        await fetch(`${API_BASE}/offers/${offerId}`, { method: 'DELETE' });
        loadOffers();
    } catch (error) {
        console.error('Error deleting offer:', error);
    }
}
