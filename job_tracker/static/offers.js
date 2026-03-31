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

    const offerForm = document.getElementById('offerForm');
    if (offerForm) {
        offerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const offerId = document.getElementById('offerEditId').value;
            const ptoDays = document.getElementById('offerPtoDays').value;
            const payload = {
                base_salary: document.getElementById('offerBaseSalary').value ? parseInt(document.getElementById('offerBaseSalary').value) : null,
                bonus_target: document.getElementById('offerBonusTarget').value ? parseInt(document.getElementById('offerBonusTarget').value) : null,
                signing_bonus: document.getElementById('offerSigningBonus').value ? parseInt(document.getElementById('offerSigningBonus').value) : null,
                equity_value: document.getElementById('offerEquityValue').value ? parseInt(document.getElementById('offerEquityValue').value) : null,
                equity_details: document.getElementById('offerEquityDetails').value || null,
                vesting_schedule: document.getElementById('offerVestingSchedule').value || null,
                total_comp: document.getElementById('offerTotalComp').value ? parseInt(document.getElementById('offerTotalComp').value) : null,
                retirement_match: document.getElementById('offerRetirementMatch').value || null,
                pto_days: ptoDays ? parseInt(ptoDays) : null,
                pto_unlimited: document.getElementById('offerPtoUnlimited').checked,
                sick_days: document.getElementById('offerSickDays').value ? parseInt(document.getElementById('offerSickDays').value) : null,
                holidays: document.getElementById('offerHolidays').value ? parseInt(document.getElementById('offerHolidays').value) : null,
                health_insurance: document.getElementById('offerHealthInsurance').value || null,
                remote_policy: document.getElementById('offerRemotePolicy').value || null,
                start_date: document.getElementById('offerStartDate').value || null,
                offer_date: document.getElementById('offerDate').value || null,
                response_deadline: document.getElementById('offerDeadline').value || null,
                relocation_assistance: document.getElementById('offerRelocation').value || null,
                status: document.getElementById('offerStatus').value,
                notes: document.getElementById('offerNotes').value || null,
            };

            try {
                const response = await fetch(`${API_BASE}/offers/${offerId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
                if (response.ok) {
                    closeModal('offerModal');
                    loadOffers();
                } else {
                    const err = await response.text();
                    alert(`Failed to save offer: ${err}`);
                }
            } catch (error) {
                alert(`Error saving offer: ${error.message}`);
            }
        });
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
                            ${offer.retirement_match ? `
                            <div class="offer-item">
                                <span class="label">401k Match:</span>
                                <span class="value">${escapeHtml(offer.retirement_match)}</span>
                            </div>` : ''}
                        </div>
                        ${offer.equity_details ? `<p style="margin-top:8px;font-size:0.875rem;color:var(--text-secondary)"><i class="fas fa-layer-group"></i> ${escapeHtml(offer.equity_details)}</p>` : ''}
                        ${offer.vesting_schedule ? `<p style="margin-top:4px;font-size:0.875rem;color:var(--text-secondary)"><i class="fas fa-clock"></i> ${escapeHtml(offer.vesting_schedule)}</p>` : ''}
                    </div>

                    <div class="offer-section">
                        <h4><i class="fas fa-umbrella"></i> Benefits & Time Off</h4>
                        <div class="offer-grid">
                            <div class="offer-item">
                                <span class="label">PTO:</span>
                                <span class="value">${offer.pto_unlimited ? 'Unlimited' : (offer.pto_days != null ? `${offer.pto_days} days` : '-')}</span>
                            </div>
                            <div class="offer-item">
                                <span class="label">Sick:</span>
                                <span class="value">${offer.sick_days != null ? `${offer.sick_days} days` : '-'}</span>
                            </div>
                            <div class="offer-item">
                                <span class="label">Holidays:</span>
                                <span class="value">${offer.holidays != null ? `${offer.holidays} days` : '-'}</span>
                            </div>
                            <div class="offer-item">
                                <span class="label">Total Days Off:</span>
                                <span class="value">${offer.pto_unlimited ? `Unlimited + ${(offer.sick_days || 0) + (offer.holidays || 0)} days` : `${(offer.pto_days || 0) + (offer.sick_days || 0) + (offer.holidays || 0)} days`}</span>
                            </div>
                        </div>
                        ${offer.health_insurance ? `<p style="margin-top:8px;font-size:0.875rem;"><i class="fas fa-heart"></i> ${escapeHtml(offer.health_insurance)}</p>` : ''}
                    </div>

                    <div class="offer-section">
                        <h4><i class="fas fa-briefcase"></i> Work Details</h4>
                        <div class="offer-grid">
                            <div class="offer-item">
                                <span class="label">Remote Policy:</span>
                                <span class="value">${offer.remote_policy ? escapeHtml(offer.remote_policy) : 'Not specified'}</span>
                            </div>
                            ${offer.start_date ? `
                            <div class="offer-item">
                                <span class="label">Start Date:</span>
                                <span class="value">${new Date(offer.start_date).toLocaleDateString()}</span>
                            </div>` : ''}
                            ${offer.response_deadline ? `
                            <div class="offer-item">
                                <span class="label">Response Deadline:</span>
                                <span class="value">${new Date(offer.response_deadline).toLocaleDateString()}</span>
                            </div>` : ''}
                            ${offer.relocation_assistance ? `
                            <div class="offer-item">
                                <span class="label">Relocation:</span>
                                <span class="value">${escapeHtml(offer.relocation_assistance)}</span>
                            </div>` : ''}
                        </div>
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
                            const fixedDaysOff = (offer.sick_days || 0) + (offer.holidays || 0);
                            const daysOffDisplay = offer.pto_unlimited
                                ? `Unlimited + ${fixedDaysOff}`
                                : `${(offer.pto_days || 0) + fixedDaysOff} days`;

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
                                    <td>${daysOffDisplay}</td>
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
                        <div class="insight-value">${sorted.some(o => o.pto_unlimited) ? 'Unlimited' : `${Math.max(...sorted.map(o => (o.pto_days || 0) + (o.sick_days || 0) + (o.holidays || 0)))} days`}</div>
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
    const offer = offers.find(o => o.id === offerId);
    if (!offer) return;

    document.getElementById('offerEditId').value = offer.id;
    document.getElementById('offerBaseSalary').value = offer.base_salary || '';
    document.getElementById('offerBonusTarget').value = offer.bonus_target || '';
    document.getElementById('offerSigningBonus').value = offer.signing_bonus || '';
    document.getElementById('offerEquityValue').value = offer.equity_value || '';
    document.getElementById('offerEquityDetails').value = offer.equity_details || '';
    document.getElementById('offerVestingSchedule').value = offer.vesting_schedule || '';
    document.getElementById('offerTotalComp').value = offer.total_comp || '';
    document.getElementById('offerRetirementMatch').value = offer.retirement_match || '';
    document.getElementById('offerPtoDays').value = offer.pto_days || '';
    document.getElementById('offerPtoUnlimited').checked = !!offer.pto_unlimited;
    document.getElementById('offerSickDays').value = offer.sick_days || '';
    document.getElementById('offerHolidays').value = offer.holidays || '';
    document.getElementById('offerHealthInsurance').value = offer.health_insurance || '';
    document.getElementById('offerRemotePolicy').value = offer.remote_policy || '';
    document.getElementById('offerStartDate').value = offer.start_date ? offer.start_date.split('T')[0] : '';
    document.getElementById('offerDate').value = offer.offer_date ? offer.offer_date.split('T')[0] : '';
    document.getElementById('offerDeadline').value = offer.response_deadline ? offer.response_deadline.split('T')[0] : '';
    document.getElementById('offerRelocation').value = offer.relocation_assistance || '';
    document.getElementById('offerStatus').value = offer.status || 'Pending';
    document.getElementById('offerNotes').value = offer.notes || '';

    document.getElementById('offerModal').classList.add('active');
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
