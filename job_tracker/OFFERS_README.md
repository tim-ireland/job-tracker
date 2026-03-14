# Offer Tracking & Comparison Feature

## Overview
Track and compare job offers with comprehensive compensation, benefits, and work details.

## Features

### Offer Management
Each offer includes:

**Compensation:**
- Base Salary
- Bonus Target
- Signing Bonus
- Equity Value (annualized)
- Equity Details (RSUs, stock options, vesting)
- Total Comp (auto-calculated or manual)

**Benefits & Time Off:**
- PTO Days
- Sick Days
- Holidays
- Health Insurance details
- 401k Match
- Other Benefits

**Work Details:**
- Start Date
- Remote Policy (Remote/Hybrid/On-site)
- Relocation Assistance
- Offer Date
- Response Deadline

**Status Tracking:**
- Pending
- Negotiating
- Accepted
- Declined

## API Endpoints

```
GET    /api/offers                  - List all offers
GET    /api/offers/{id}             - Get specific offer
POST   /api/offers                  - Create new offer
PUT    /api/offers/{id}             - Update offer
DELETE /api/offers/{id}             - Delete offer
GET    /api/offers/compare/all      - Get comparison data
```

## Offer Comparison View

The comparison feature provides:

### Comparison Table
- Side-by-side comparison of all offers
- Sortable by total compensation
- Highlights accepted offers
- Shows all key metrics at a glance

### Quick Insights
- **Highest Total Comp** - Best compensation package
- **Average Total Comp** - Market benchmark
- **Most Days Off** - Best work-life balance
- **Pending Offers** - Decisions needed

### Calculated Metrics
- Total Days Off = PTO + Sick + Holidays
- Total Comp comparison ranking
- Visual highlighting of best offers

## Usage

### Adding an Offer
1. Navigate to Applications tab
2. Find application with "Offer" status
3. Click "Add Offer" (coming soon in UI)
4. Or use API directly

### Comparing Offers
1. Go to Offers tab
2. Click "Compare All" button
3. View side-by-side comparison
4. Review insights panel
5. Make informed decision

### Tracking Benefits
- Track both monetary and non-monetary benefits
- Calculate total time off
- Document retirement matching
- Note health insurance details

## Example Offer Entry

```json
{
  "application_id": 1,
  "offer_date": "2026-02-25",
  "response_deadline": "2026-03-08",
  "base_salary": 243000,
  "bonus_target": 50000,
  "signing_bonus": 25000,
  "equity_value": 80000,
  "equity_details": "RSUs, 4-year vest",
  "total_comp": 398000,
  "pto_days": 20,
  "sick_days": 10,
  "holidays": 11,
  "health_insurance": "PPO, $0 premium",
  "retirement_match": "6% match",
  "remote_policy": "Hybrid",
  "status": "Pending"
}
```

## Comparison Criteria

### Compensation
- Base salary (guaranteed)
- Bonus (performance-based)
- Equity (long-term value)
- Total package

### Benefits
- Total days off
- Health coverage
- Retirement matching
- Other perks

### Work-Life
- Remote flexibility
- Commute requirements
- Relocation support

## Best Practices

1. **Enter Complete Data** - More data = better comparison
2. **Update Total Comp** - Keep it current as you negotiate
3. **Track Deadlines** - Don't miss response deadlines
4. **Document Benefits** - Non-salary compensation matters
5. **Compare Regularly** - Review as new offers come in

## Future Enhancements

- [ ] Offer form modal in UI
- [ ] Link offers directly from applications
- [ ] Negotiation history tracking
- [ ] Export comparison to PDF
- [ ] Cost of living adjustments
- [ ] After-tax compensation calculator
- [ ] Benefits value calculator
