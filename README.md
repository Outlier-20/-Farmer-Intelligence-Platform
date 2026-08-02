# Farmer-Intelligence-Platform

# 🌾 Farmer Intelligence Platform (OSINT & Analytics Platform)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active--Development-orange.svg)]()
[![Data Coverage](https://img.shields.io/badge/Data-2016%20--%202026-brightgreen.svg)]()

---

## 📌 Overview

**Farmer Intelligence Platform** is an interactive, OSINT-driven visualization and analytics dashboard designed to monitor US agricultural assistance programs, farm locations, individual recipients, and temporary agricultural labor forces (H-2A workers).

---

## 🔥 Key Features

### 🗺️ Interactive US Map & Timeline
* **Interactive Map Navigation:** Explore data geographically across all US states.
* **Yearly Timeline Selector:** Filter intelligence data seamlessly from **2016 to 2026**.

### 👤 Individual Profiles
* Detailed recipient breakdown:
  * Profile Photo & Name
  * Dollar Amount Received
  * Program Type & Associated Farm
  * Year and additional contextual information
* **Totals Aggregation:** Real-time aggregation of total funds dispersed to individuals.

### 🚜 Farm Intelligence
* Comprehensive farm analysis:
  * Farm Photo & Name
  * Geographic Coordinates (Latitude / Longitude)
  * Active Programs & Number of Associated Farmers
  * Total Funds Received & Year-over-Year tracking

### 👷 Temporary Agricultural Workers & H-2A Labor
* Deep dive into temporary labor metrics:
  * Worker/Contractor Profile (Photo, Name, Job Role)
  * Contract Duration, Start Date, and End Date
  * Paginated navigation (`Next` / `Previous` controls) to review worker registries
  * Real-time labor capacity totals per region or farm

---

## 🗂️ Data Structure & Tracking Metrics

| Entity Category | Key Parameters Captured | Aggregations |
| :--- | :--- | :--- |
| **Individual** | Name, Photo, Dollar Amount, Program Name, Farm Link, Year | Total Individual Grants |
| **Farm** | Name, Location Coordinates, Farmers Count, Program Type, Funds | Total Farm Funding |
| **Worker** | Name, Job Title, Contract Start/End Date, Duration, Photo | Total Labor Force |
| **Timeline** | 2016 – 2026 Yearly Datasets | Yearly Comparative Totals |

---

## 🚀 Quick Start

### Prerequisites
* Python 3.10+
* Modern Web Browser (Chrome, Firefox, Edge)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Outlier-20/-Farmer-Intelligence-Platform.git](https://github.com/Outlier-20/-Farmer-Intelligence-Platform.git)
   cd -Farmer-Intelligence-Platform

🛡️ Data Privacy & Ethical OSINT Guidelines
All data visualized in this platform is sourced strictly from public transparency repositories (USDA, Department of Labor, and open-source government records).

No private personal information (PII) beyond official public records is stored or exposed.

📜 License
Distributed under the MIT License. 
---
<ElicitationsGroup message="What would you like to do next?">
<Elicitation label="Format side-by-side comparison tables in Markdown" query="Format side-by-side comparison tables in Markdown" query_intent="CLICKABLE_SUGGESTION" />
<Elicitation label="Add custom styling to Markdown tables in GitHub" query="Add custom styling to Markdown tables in GitHub" query_intent="CLICKABLE_SUGGESTION" />
<Elicitation label="Embed dynamic GitHub badges in README.md" query="Embed dynamic GitHub badges in README.md" query_intent="CLICKABLE_SUGGESTION" />
</ElicitationsGroup>
