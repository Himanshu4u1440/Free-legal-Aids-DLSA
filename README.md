# District Legal Services Authority (DLSA) Portal

An informative, public-facing, and administrative web portal for the **District Legal Services Authority (DLSA)**, built with **Python (Flask, SQLAlchemy, pyodbc)** and **Microsoft SQL Server (T-SQL)**.

This portal is designed to make the legal aid system transparent and accessible to ordinary citizens ("normal peoples"), educating them on their constitutional rights under **Article 39A**, detailing the **leadership hierarchy and high ranks**, explaining the **roles and 12 statutory duties of Para Legal Volunteers (PLVs)**, and mapping out the **places where they are deployed** (police stations, prisons, hospital trauma desks, and rural clinics).

---

## 🌟 Key Features

### 1. Citizen Information & Entitlement
- **Section 12 Eligibility Interactive Checker**: Instant assessment tool for citizens to check if they qualify for 100% free legal aid (Women, Children, SC/ST, Detainees, Industrial Workmen, Persons with Disabilities, Indigent citizens with annual income below ₹3 Lakhs).
- **Public Legal Aid Application Form (`/apply`)**: Direct online submission for civil, criminal, matrimonial, labor, and domestic violence grievances. Generates a unique tracking number (e.g. `DLSA-2026-XXXX`).
- **Live Status Tracking (`/track`)**: Visual multi-step progress stepper showing verification, panel advocate assignment, and DLSA secretary remarks.
- **National Lok Adalat & Camp Schedules**: Notice board of upcoming benches, traffic challan settlements, and rural legal literacy camps.
- **24x7 Emergency Helpline (`15100`)**: Prominently displayed toll-free national legal assistance hotline.

### 2. High Ranks & Leadership Hierarchy (`/leadership`)
- **Apex Judicial Head**: Chairman, DLSA (Principal District & Sessions Judge)
- **Executive Administrator**: Secretary, DLSA (Cadre Senior Civil Judge)
- **Defense System**: Chief Legal Aid Defense Counsel (Chief LADC) & Deputy Chief Counsel
- **Frontline Leadership**: Panel Advocate Conveners and Retainer Counsels
- Detailed profiles covering statutory duties, administrative powers, courtroom jurisdiction, and contact emails/phones.

### 3. Para Legal Volunteers (PLVs) Portal (`/plv-portal`)
- **What is a PLV?**: Comprehensive public explainer on community volunteer selection and training.
- **The 12 Statutory Duties**: Clear breakdown of duties (grassroots first-aid, police station remand monitoring, jail legal aid clinics, domestic violence intervention, child protection, hospital trauma desk, rural dispute mediation, and reporting human rights violations).
- **Public Code of Conduct**: Reassures citizens that all PLV services are strictly **free of cost** and that PLVs cannot accept money or demand fees.
- **Interactive PLV Directory**: Live search by volunteer name, area, occupation, qualification, specialization, and current deployment center.

### 4. Places of Deployment & Legal Aid Clinics (`/deployments`)
- Categorized directory of frontline centers:
  - **Court Front Office Helpdesks**
  - **Police Station Legal Desks** (monitoring D.K. Basu arrest guidelines)
  - **District Jails / Sub-Jails** (undertrial prisoner legal clinics)
  - **Hospital Victim Desks** (road accident & acid attack relief)
  - **Gram Panchayat Legal Aid Clinics** (rural land & welfare mediation)
  - **One Stop Centres (Sakhi)** (women crisis intervention)
- Lists operating hours, address, in-charge officers, and the **specific PLVs assigned to each center**.

### 5. NALSA & DLSA Schemes (`/schemes`)
- Detailed catalogue of national and state legal aid schemes:
  - Drug Abuse Eradication & Victim Rehabilitation Scheme
  - Child Friendly Legal Services Scheme
  - Legal Services to Mentally Ill & Disabled Persons Scheme
  - Victims of Trafficking & Commercial Sexual Exploitation Scheme
  - Unorganised Sector Workers Scheme
  - Senior Citizens Legal Aid & Maintenance Scheme
- Detailed breakdown of objectives, eligibility criteria, benefits, and required documents.

### 6. Administrative Management Portal (`/admin`)
- Secure login for DLSA staff (`admin` / `admin123`).
- **Case Review**: Approve or update legal aid applications, assign free panel lawyers, assign PLVs, and record internal notes.
- **Manage PLVs**: Enroll new volunteers, assign them to deployment centers, and update duty status.
- **Manage Deployments**: Add new police station desks, jail clinics, or hospital centers.
- **Manage Leadership**: Add new judicial officers, defense counsels, and executive ranks.

### 7. RESTful API Endpoints (`/api/...`)
- `GET /api/stats`: Key authority metrics (active PLVs, total deployments, cases assisted, database engine).
- `GET /api/plvs`: JSON list of Para Legal Volunteers.
- `GET /api/deployments`: JSON list of deployment locations with assigned personnel.
- `GET /api/schemes`: JSON list of legal aid schemes.

---

## 🛠️ Technology Stack & Architecture

- **Backend**: Python 3.14 + Flask 3.1
- **Database**: Microsoft SQL Server (T-SQL) with native `pyodbc` and `SQLAlchemy 2.0`
- **Frontend**: Responsive HTML5, Bootstrap 5.3, Bootstrap Icons, Vanilla JS
- **Design Aesthetic**: Official Indian Judiciary / Government Portal style (Tricolor accents, clean typography, emblem badges, and accessible layouts).

---

## 🗄️ Microsoft SQL Server Database Configuration

The project is built to run directly with **Microsoft SQL Server**.

### Option A: Automatic Setup using `setup_mssql.py`
If you have Microsoft SQL Server or SQL Server Express running on your machine:
1. Ensure your SQL Server service is running and TCP/IP is enabled.
2. Edit `.env` to specify your SQL Server details:
   ```ini
   DB_TYPE=mssql
   DB_SERVER=localhost       # or localhost\SQLEXPRESS
   DB_DATABASE=DLSA_DB
   DB_TRUSTED_CONNECTION=yes # Windows Authentication
   DB_DRIVER=SQL Server      # or ODBC Driver 17 for SQL Server
   ```
3. Run the automated wizard:
   ```bash
   python setup_mssql.py
   ```
   This will automatically:
   - Connect to SQL Server
   - Create `DLSA_DB` database if not present
   - Create all tables, foreign keys, and indexes
   - Seed all initial official data, PLVs, deployments, and schemes.

### Option B: Execute T-SQL Script in SSMS
You can also open [`schema_mssql.sql`](file:///c:/Users/Himanshu/Documents/Project%201/schema_mssql.sql) directly inside **SQL Server Management Studio (SSMS)** or **Azure Data Studio** and execute it (`F5`). It contains the complete schema, views (`vw_ActivePLVDeployments`), stored procedures (`sp_GetDLSAStats`), and seed data.

### Option C: Instant Local Development / Demo Mode
If you do not have MS SQL Server installed locally right now, the application features an **automatic fallback (`DB_TYPE=auto`)**:
- It attempts to connect to MS SQL Server.
- If MS SQL Server is offline, it seamlessly spins up an identical local SQLite database (`dlsa.db`) so you can run, test, and demonstrate the full portal immediately without any blockers.
- A status badge in the portal header displays the active database engine.

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Web Application
```bash
python app.py
```
Open your browser and navigate to:
**`http://127.0.0.1:5000`**

### 3. Staff / Admin Login Credentials
- **URL**: `http://127.0.0.1:5000/admin/login`
- **Username**: `admin`
- **Password**: `admin123`

### 4. Running Automated Tests
```bash
python test_app.py
```
All 8 test suites verify routing, database operations, citizen application submission, tracking, admin updates, and REST API responses.

---

## 📂 Project Directory Structure

```
Project 1/
├── app.py                     # Main Flask web application & routes
├── config.py                  # Environment & MS SQL database connection logic
├── database.py                # SQLAlchemy engine & session manager
├── models.py                  # SQLAlchemy ORM models matching MS SQL schema
├── seed_data.py               # Realistic DLSA seeder (Officials, PLVs, Centers)
├── schema_mssql.sql           # Pure T-SQL schema, views, procedures & seed data
├── setup_mssql.py             # MS SQL connection tester and migration wizard
├── test_app.py                # Automated unit and integration test suite
├── requirements.txt           # Python package requirements
├── .env                       # Active environment configuration
├── .env.example               # Template for environment configuration
├── static/
│   ├── css/
│   │   └── style.css          # Government portal theme & responsive styles
│   ├── js/
│   │   └── main.js            # Live search, filters, and eligibility checker
│   └── images/                # Official emblems & SVG profile avatars
└── templates/
    ├── base.html              # Base layout with navbar, footer & helpline
    ├── index.html             # Homepage with stats, quick modules & checker
    ├── leadership.html        # High Ranks, hierarchy & duties
    ├── plv.html               # Para Legal Volunteers 12 duties & directory
    ├── deployments.html       # Places of deployment (Police, Jails, Clinics)
    ├── schemes.html           # NALSA/DLSA schemes & eligibility
    ├── apply.html             # Online Citizen Application for Free Legal Aid
    ├── track.html             # Real-time application tracking with stepper
    └── admin/
        ├── login.html         # Staff login
        ├── dashboard.html     # Case review & applications management
        ├── plvs.html          # PLV enrollment & assignment
        ├── deployments.html   # Deployment place management
        └── leadership.html    # Executive ranks management
```
