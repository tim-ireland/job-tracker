"""
Fix misclassified company names from bulk import.
- Updates company_id on affected applications
- Renames filesystem directories to match
- Cleans up orphaned company records
"""

import sqlite3
import os
import shutil
from pathlib import Path

DB_PATH = "/Users/tim/Development/my-job-search-2026/job_applications.db"
APPS_DIR = Path("/Users/tim/Development/my-job-search-2026/applications")

# app_id → (correct_company_name, clean_role)
FIXES = {
    # Ats → Advisor360
    64: ("Advisor360", "Engineering Manager, Data Streams"),
    65: ("Advisor360", "Engineering Manager, Platform AI"),

    # Careers → various
    31: ("Datadog", "Engineering Manager - Security Incident Response"),
    36: ("IBM", "Unknown Role"),
    50: ("Toast", "Manager II, Software Engineering"),
    55: ("Datadog", "Engineering Manager I - Cyber Threat Intelligence"),
    60: ("Circle", "Manager, Software Engineering"),
    78: ("Formlabs", "Director of Software Product Management"),

    # Explore → Netflix
    45: ("Netflix", "Engineering Manager, Compute Runtime"),
    56: ("Netflix", "Engineering Manager, Cloud Infrastructure Security"),
    72: ("Netflix", "Engineering Manager - OC Foundation Infrastructure Services"),
    75: ("Netflix", "Engineering Manager, Attack Emulation Team"),

    # Githubinc → Github
    42: ("Github", "Principal Engineering Manager"),
    51: ("Github", "Staff Software Engineering Manager"),
    52: ("Github", "Principal Engineering Manager, Git Systems"),

    # Job-Boards → various
    28: ("Figma", "Manager, Software Engineering"),
    38: ("Dragos", "Software Engineering Manager"),
    39: ("Redpanda", "Director of Engineering, Cloud"),
    40: ("Cloudflare", "Engineering Manager, Queues"),
    46: ("Vercel", "Sr. Engineering Manager, Platform"),
    57: ("GitLab", "Engineering Manager, AST: Composition Analysis"),
    58: ("Figma", "Manager, Software Engineering - Collaboration Tools"),
    59: ("Huntress", "Staff Product Manager, Endpoint Security Posture Management"),
    61: ("Iterable", "Manager, Engineering (Nova)"),
    62: ("Figma", "Manager, Software Engineering - Design"),
    63: ("Cloudflare", "Engineering Manager"),
    67: ("Affirm", "Director, Software Engineering - Site Reliability Engineering"),
    68: ("Anthropic", "Engineering Manager, People Products"),
    76: ("Canonical", "Engineering Manager, MAAS"),

    # Jobs → various
    41: ("Super", "Director of Engineering, Core Experience"),
    43: ("UP Labs", "Unknown Role"),
    44: ("1Password", "Senior Director Engineering, Infrastructure & Platform Services"),
    47: ("LangChain", "Senior Fullstack Engineer, AI Observability & Evals Platform"),
    48: ("LangChain", "Python OSS Engineer"),
    66: ("Camunda", "Manager, Engineering"),
    71: ("Teradyne", "Product Software Engineering Manager"),

    # Metacareers → Meta
    73: ("Meta", "Unknown Role"),

    # Pinterestcareers → Pinterest
    49: ("Pinterest", "Sr. Engineering Manager, AI/ML Serving Platform"),
}


def dir_name(company, role):
    return f"{company.replace(' ', '_')}_{role.replace(' ', '_').replace('/', '_')}"


def get_or_create_company(cur, name):
    cur.execute("SELECT id FROM companies WHERE name = ?", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO companies (name) VALUES (?)", (name,))
    return cur.lastrowid


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    renamed = []
    skipped = []
    errors = []

    for app_id, (new_company, new_role) in FIXES.items():
        # Get current application state
        cur.execute(
            "SELECT a.role, c.name FROM applications a JOIN companies c ON a.company_id = c.id WHERE a.id = ?",
            (app_id,)
        )
        row = cur.fetchone()
        if not row:
            errors.append(f"  App {app_id}: not found in DB")
            continue

        old_role, old_company = row
        old_dir = APPS_DIR / dir_name(old_company, old_role)
        new_dir = APPS_DIR / dir_name(new_company, new_role)

        # Get or create the correct company
        company_id = get_or_create_company(cur, new_company)

        # Update application
        cur.execute(
            "UPDATE applications SET company_id = ?, role = ? WHERE id = ?",
            (company_id, new_role, app_id)
        )

        # Rename directory
        if old_dir == new_dir:
            skipped.append(f"  App {app_id}: dir unchanged ({old_dir.name})")
        elif new_dir.exists():
            skipped.append(f"  App {app_id}: target dir already exists, skipping rename ({new_dir.name})")
        elif old_dir.exists():
            old_dir.rename(new_dir)
            renamed.append(f"  App {app_id}: {old_dir.name}\n            → {new_dir.name}")
        else:
            skipped.append(f"  App {app_id}: old dir not found ({old_dir.name}), DB updated only")

    con.commit()

    # Clean up companies that no longer have any applications
    cur.execute("""
        DELETE FROM companies
        WHERE id NOT IN (SELECT DISTINCT company_id FROM applications)
        AND name IN ('Ats','Careers','Explore','Job-Boards','Jobs','Metacareers','Pinterestcareers','Githubinc')
    """)
    removed_companies = cur.rowcount
    con.commit()
    con.close()

    print(f"\n✅ Renamed {len(renamed)} directories:")
    for r in renamed:
        print(r)

    if skipped:
        print(f"\n⚠️  Skipped {len(skipped)}:")
        for s in skipped:
            print(s)

    if errors:
        print(f"\n❌ Errors {len(errors)}:")
        for e in errors:
            print(e)

    print(f"\n🗑️  Removed {removed_companies} orphaned company record(s)")
    print("\nDone.")


if __name__ == "__main__":
    main()
