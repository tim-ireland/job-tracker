#!/usr/bin/env python3
"""
Script to export weekly job search activity for Massachusetts DUA reporting.

Usage:
    # Export last week (text format)
    python scripts/export_weekly_activity.py
    
    # Export specific week (text format)
    python scripts/export_weekly_activity.py --week-start 2026-03-09
    
    # Export as CSV
    python scripts/export_weekly_activity.py --format csv
    
    # Export date range
    python scripts/export_weekly_activity.py --start-date 2026-02-01 --end-date 2026-03-31
    
    # Export date range as CSV
    python scripts/export_weekly_activity.py --start-date 2026-02-01 --end-date 2026-03-31 --format csv
"""
import argparse
import requests
import sys
from datetime import datetime, timedelta


def get_last_sunday(date=None):
    """Get the date of the most recent Sunday before the given date."""
    if date is None:
        date = datetime.now()
    days_since_sunday = (date.weekday() + 1) % 7
    if days_since_sunday == 0:
        days_since_sunday = 7  # Get previous Sunday, not today
    return date - timedelta(days=days_since_sunday)


def export_weekly(base_url, week_start=None, format='text', output_file=None):
    """Export weekly activity report."""
    if format == 'csv':
        endpoint = f"{base_url}/api/reports/dua-weekly-csv"
    else:
        endpoint = f"{base_url}/api/reports/dua-weekly"
    
    params = {}
    if week_start:
        params['week_start'] = week_start
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(response.text)
            print(f"Report saved to {output_file}")
        else:
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching report: {e}", file=sys.stderr)
        sys.exit(1)


def export_range(base_url, start_date, end_date, format='text', output_file=None):
    """Export date range activity report."""
    if format == 'csv':
        endpoint = f"{base_url}/api/reports/dua-range-csv"
    else:
        endpoint = f"{base_url}/api/reports/dua-range"
    
    params = {
        'start_date': start_date,
        'end_date': end_date
    }
    
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(response.text)
            print(f"Report saved to {output_file}")
        else:
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching report: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Export job search activity for Massachusetts DUA reporting',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--base-url',
        default='http://localhost:8000',
        help='Base URL of the job tracker API (default: http://localhost:8000)'
    )
    
    parser.add_argument(
        '--week-start',
        help='Start date for weekly report (YYYY-MM-DD format, should be a Sunday)'
    )
    
    parser.add_argument(
        '--start-date',
        help='Start date for range report (YYYY-MM-DD format)'
    )
    
    parser.add_argument(
        '--end-date',
        help='End date for range report (YYYY-MM-DD format)'
    )
    
    parser.add_argument(
        '--format',
        choices=['text', 'csv'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path (default: print to stdout)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.start_date or args.end_date:
        if not (args.start_date and args.end_date):
            parser.error("--start-date and --end-date must be used together")
        
        export_range(
            args.base_url,
            args.start_date,
            args.end_date,
            args.format,
            args.output
        )
    else:
        # Weekly export
        if args.week_start:
            week_start = args.week_start
        else:
            # Default to previous week
            last_sunday = get_last_sunday()
            week_start = last_sunday.strftime('%Y-%m-%d')
            print(f"Exporting week starting {week_start}", file=sys.stderr)
        
        export_weekly(
            args.base_url,
            week_start,
            args.format,
            args.output
        )


if __name__ == '__main__':
    main()
