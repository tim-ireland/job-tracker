"""
LinkedIn job URL parser
Extracts job information from public LinkedIn job postings
"""
import re
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
from urllib.parse import urlparse


def is_linkedin_job_url(url: str) -> bool:
    """Check if URL is a LinkedIn job posting"""
    try:
        parsed = urlparse(url)
        return 'linkedin.com' in parsed.netloc and '/jobs/view/' in parsed.path
    except:
        return False


def extract_job_id(url: str) -> Optional[str]:
    """Extract job ID from LinkedIn URL"""
    try:
        match = re.search(r'/jobs/view/(\d+)', url)
        if match:
            return match.group(1)
    except:
        pass
    return None


def fetch_linkedin_job(url: str) -> Optional[Dict]:
    """
    Fetch and parse LinkedIn job posting from public URL
    
    Returns dict with: company, title, location, description, url
    """
    if not is_linkedin_job_url(url):
        return None
    
    job_id = extract_job_id(url)
    if not job_id:
        return None
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        job_data = {
            'url': url,
            'job_id': job_id,
            'company': None,
            'title': None,
            'location': None,
            'description': None,
        }
        
        # Try to get title from meta tags or page elements
        title_meta = soup.find('meta', property='og:title')
        if title_meta:
            job_data['title'] = title_meta.get('content', '').strip()
        else:
            h1 = soup.find('h1')
            if h1:
                job_data['title'] = h1.get_text().strip()
        
        # Try to get company name
        company_elem = soup.find('a', class_=re.compile(r'topcard__org-name-link'))
        if company_elem:
            job_data['company'] = company_elem.get_text().strip()
        else:
            company_meta = soup.find('meta', property='og:description')
            if company_meta:
                desc = company_meta.get('content', '')
                if ' at ' in desc:
                    job_data['company'] = desc.split(' at ', 1)[1].split('.')[0].strip()
        
        # Try to get location
        location_elem = soup.find('span', class_=re.compile(r'topcard__flavor'))
        if location_elem:
            job_data['location'] = location_elem.get_text().strip()
        
        # Try to get description
        desc_elem = soup.find('div', class_=re.compile(r'description__text'))
        if desc_elem:
            description = desc_elem.get_text(separator='\n').strip()
            if len(description) > 5000:
                description = description[:5000] + '...'
            job_data['description'] = description
        
        if job_data['title']:
            return job_data
        
        return None
        
    except requests.RequestException as e:
        print(f"Error fetching LinkedIn job {url}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing LinkedIn job {url}: {e}")
        return None


def parse_job_urls(urls_text: str) -> list:
    """
    Parse multiple URLs from text (one per line)
    Returns list of job data dicts
    """
    lines = urls_text.strip().split('\n')
    urls = [line.strip() for line in lines if line.strip()]
    
    results = []
    for url in urls:
        if is_linkedin_job_url(url):
            job_data = fetch_linkedin_job(url)
            if job_data:
                results.append(job_data)
            else:
                job_id = extract_job_id(url)
                results.append({
                    'url': url,
                    'job_id': job_id,
                    'company': None,
                    'title': f'Job {job_id}',
                    'location': None,
                    'description': 'Failed to fetch details. Please update manually.',
                    'error': True
                })
    
    return results
