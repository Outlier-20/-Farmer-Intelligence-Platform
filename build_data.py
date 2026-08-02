"""
Process real USDA subsidy data (OpenSubsidies.org) and DOL H-2A disclosure data
into a single JSON structure for the interactive HTML map.
"""
import json
import os
from datetime import datetime

DATA_DIR = "C:/Users/User/Desktop/farms/data"

# ============ LOAD SUBSIDY DATA ============
print("Loading subsidy data...")

with open(os.path.join(DATA_DIR, "states.json"), "r") as f:
    states_raw = json.load(f)

with open(os.path.join(DATA_DIR, "state-yearly.json"), "r") as f:
    state_yearly_raw = json.load(f)

with open(os.path.join(DATA_DIR, "top-recipients.json"), "r") as f:
    top_recipients_raw = json.load(f)

with open(os.path.join(DATA_DIR, "counties.json"), "r") as f:
    counties_raw = json.load(f)

with open(os.path.join(DATA_DIR, "programs.json"), "r") as f:
    programs_raw = json.load(f)

with open(os.path.join(DATA_DIR, "yearly.json"), "r") as f:
    yearly_raw = json.load(f)

# US state abbreviations to filter
US_STATES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
    "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
    "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
    "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
}

# Build state summary lookup
state_info = {}
for s in states_raw:
    if s["abbr"] in US_STATES:
        state_info[s["abbr"]] = {
            "name": s["name"],
            "totalPayments": s["payments"],
            "totalAmount": s["amount"],
            "topPrograms": s["topPrograms"][:5]
        }

# Build state-yearly lookup: {state: {year: {payments, amount}}}
state_yearly = {}
for row in state_yearly_raw:
    st = row["state"]
    yr = row["year"]
    if st in US_STATES and 2016 <= yr <= 2026:
        if st not in state_yearly:
            state_yearly[st] = {}
        state_yearly[st][str(yr)] = {
            "payments": row["payments"],
            "amount": round(row["amount"], 2)
        }

# Build top recipients by state
recipients_by_state = {}
for r in top_recipients_raw:
    st = r["state"]
    if st in US_STATES:
        if st not in recipients_by_state:
            recipients_by_state[st] = []
        recipients_by_state[st].append({
            "name": r["name"],
            "city": r["city"],
            "amount": round(r["amount"], 2),
            "payments": r["payments"],
            "topProgram": r["topProgram"]
        })

# Build counties by state
counties_by_state = {}
for c in counties_raw:
    st = c["state"]
    if st in US_STATES:
        if st not in counties_by_state:
            counties_by_state[st] = []
        if len(counties_by_state[st]) < 30:  # top 30 per state
            counties_by_state[st].append({
                "county": c["county"],
                "fips": c["fips"],
                "payments": c["payments"],
                "amount": round(c["amount"], 2)
            })

# ============ LOAD H-2A DATA ============
print("Loading H-2A data (this may take a minute)...")
import openpyxl

h2a_by_state = {}  # {state: [records]}

wb = openpyxl.load_workbook(os.path.join(DATA_DIR, "h2a_fy2024.xlsx"), read_only=True)
ws = wb.active

# Get header row
headers = None
row_count = 0
for row in ws.iter_rows(values_only=True):
    if headers is None:
        headers = list(row)
        continue
    row_count += 1

    # Key columns
    try:
        employer_name = row[headers.index("EMPLOYER_NAME")] or ""
        employer_state = row[headers.index("EMPLOYER_STATE")] or ""
        employer_city = row[headers.index("EMPLOYER_CITY")] or ""
        case_status = row[headers.index("CASE_STATUS")] or ""
        job_title = row[headers.index("JOB_TITLE")] or ""
        workers_needed = row[headers.index("TOTAL_WORKERS_NEEDED")]
        workers_certified = row[headers.index("TOTAL_WORKERS_H2A_CERTIFIED")]
        begin_date = row[headers.index("EMPLOYMENT_BEGIN_DATE")]
        end_date = row[headers.index("EMPLOYMENT_END_DATE")]
        wage = row[headers.index("WAGE_OFFER")]
        worksite_state = row[headers.index("WORKSITE_STATE")] or employer_state
        worksite_city = row[headers.index("WORKSITE_CITY")] or ""
        worksite_county = row[headers.index("WORKSITE_COUNTY")] or ""
        soc_title = row[headers.index("SOC_TITLE")] or ""
        case_number = row[headers.index("CASE_NUMBER")] or ""
    except (ValueError, IndexError):
        continue

    st = worksite_state.strip().upper() if worksite_state else employer_state.strip().upper() if employer_state else ""
    if st not in US_STATES:
        continue

    # Format dates
    begin_str = ""
    end_str = ""
    duration = ""
    if begin_date:
        if isinstance(begin_date, datetime):
            begin_str = begin_date.strftime("%Y-%m-%d")
        else:
            begin_str = str(begin_date)[:10]
    if end_date:
        if isinstance(end_date, datetime):
            end_str = end_date.strftime("%Y-%m-%d")
        else:
            end_str = str(end_date)[:10]

    if begin_date and end_date:
        try:
            if isinstance(begin_date, datetime) and isinstance(end_date, datetime):
                days = (end_date - begin_date).days
                months = round(days / 30.44)
                duration = f"{months} months" if months > 0 else f"{days} days"
        except:
            duration = ""

    wage_str = ""
    if wage:
        try:
            wage_str = f"${float(wage):.2f}/hr"
        except:
            wage_str = str(wage)

    record = {
        "employer": employer_name.strip(),
        "city": (worksite_city or employer_city).strip(),
        "county": worksite_county.strip(),
        "caseStatus": case_status.strip(),
        "jobTitle": job_title.strip(),
        "socTitle": soc_title.strip(),
        "workersNeeded": int(workers_needed) if workers_needed else 0,
        "workersCertified": int(workers_certified) if workers_certified else 0,
        "dateStart": begin_str,
        "dateEnd": end_str,
        "duration": duration,
        "wage": wage_str,
        "caseNumber": case_number.strip()
    }

    if st not in h2a_by_state:
        h2a_by_state[st] = []
    h2a_by_state[st].append(record)

wb.close()
print(f"  Processed {row_count} H-2A records")

# Compute H-2A totals by state
h2a_totals = {}
for st, records in h2a_by_state.items():
    total_workers = sum(r["workersCertified"] for r in records)
    total_cases = len(records)
    h2a_totals[st] = {
        "totalCases": total_cases,
        "totalWorkersCertified": total_workers,
        "totalWorkersNeeded": sum(r["workersNeeded"] for r in records)
    }

# Limit records per state for HTML size (top 50 per state by workers certified)
h2a_trimmed = {}
for st, records in h2a_by_state.items():
    sorted_recs = sorted(records, key=lambda x: x["workersCertified"], reverse=True)
    h2a_trimmed[st] = sorted_recs[:50]

# ============ BUILD FINAL JSON ============
print("Building final data structure...")

final_data = {
    "subsidyByState": state_info,
    "subsidyByStateYear": state_yearly,
    "recipientsByState": recipients_by_state,
    "countiesByState": counties_by_state,
    "h2aByState": h2a_trimmed,
    "h2aTotalsByState": h2a_totals,
    "yearlyTotals": {str(y["year"]): {"payments": y["payments"], "amount": round(y["amount"], 2)} for y in yearly_raw if 2016 <= y["year"] <= 2026},
    "programs": [{"program": p["program"], "payments": p["payments"], "amount": round(p["amount"], 2)} for p in programs_raw[:30]]
}

output_path = os.path.join(DATA_DIR, "combined_data.json")
with open(output_path, "w") as f:
    json.dump(final_data, f, separators=(',', ':'))

file_size = os.path.getsize(output_path)
print(f"Output: {output_path} ({file_size:,} bytes)")

# Print summary
print(f"\n=== DATA SUMMARY ===")
print(f"States with subsidy data: {len(state_info)}")
print(f"States with yearly data: {len(state_yearly)}")
print(f"States with recipients: {len(recipients_by_state)}")
print(f"Total recipients: {sum(len(v) for v in recipients_by_state.values())}")
print(f"States with county data: {len(counties_by_state)}")
print(f"States with H-2A data: {len(h2a_by_state)}")
print(f"Total H-2A records: {sum(len(v) for v in h2a_by_state.values())}")
print(f"H-2A records in output: {sum(len(v) for v in h2a_trimmed.values())}")
for st in sorted(h2a_totals.keys()):
    t = h2a_totals[st]
    print(f"  {st}: {t['totalCases']} cases, {t['totalWorkersCertified']} workers certified")
