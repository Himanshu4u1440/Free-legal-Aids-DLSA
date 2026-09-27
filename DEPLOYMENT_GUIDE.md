# DLSA Porbandar Portal — 24/7 Cloud Deployment Guide

This guide explains how to host the **District Legal Services Authority (DLSA) Porbandar Legal Aid Portal** online 24/7 on free cloud hosting platforms.

---

## Pre-Packaged Deployment Bundle
A clean, lightweight deployment zip file has already been generated in the project root:
- **File**: `dlsa_porbandar_deploy.zip` (~480 KB)
- **Includes**: All templates, static files, SQLite database (`dlsa.db`), translations, report files, WSGI configurations, and requirements.

---

## Method 1: PythonAnywhere (Recommended — 100% Free & Persistent SQLite)
*PythonAnywhere is specifically built for Python/Flask applications. It offers persistent disk storage for your SQLite database, so all data submitted through legal aid forms and admin panel remains permanently saved.*

### Step 1: Create a Free Account
1. Visit [https://www.pythonanywhere.com](https://www.pythonanywhere.com).
2. Click **Pricing & signup** and create a **Free Beginner Account** (no credit card required).

### Step 2: Upload Project Files
1. In your PythonAnywhere dashboard, click the **Files** tab.
2. In the home directory (`/home/<username>/`), click **Upload a file** and select `dlsa_porbandar_deploy.zip`.

### Step 3: Extract and Install Dependencies
1. Open a **Bash Console** from the **Consoles** tab.
2. Run the following commands:
   ```bash
   unzip dlsa_porbandar_deploy.zip -d dlsa_project
   cd dlsa_project
   pip install --user -r requirements.txt
   ```

### Step 4: Configure Web App
1. Go to the **Web** tab in your dashboard.
2. Click **Add a new web app**.
3. Choose **Manual configuration** -> Select **Python 3.11** (or 3.10).
4. Under the **Code** section:
   - **Source code**: `/home/<username>/dlsa_project`
   - **Working directory**: `/home/<username>/dlsa_project`
5. Under **WSGI configuration file**, click the link (`/var/www/<username>_pythonanywhere_com_wsgi.py`).
6. Replace the entire content with:
   ```python
   import sys
   import os

   project_home = '/home/<username>/dlsa_project'
   if project_home not in sys.path:
       sys.path.insert(0, project_home)

   os.environ["DB_TYPE"] = "sqlite"

   from app import app as application
   ```
   *(Replace `<username>` with your actual PythonAnywhere username)*.
7. Click **Save** (top right).
8. Go back to the **Web** tab and click the big green **Reload <username>.pythonanywhere.com** button.

### Your Live URL:
`https://<your-username>.pythonanywhere.com`

---

## Method 2: Render.com (Modern Git/GitHub Deployment)

### Step 1: Push Code to GitHub
1. Create a new repository on [GitHub](https://github.com/new) named `dlsa-porbandar`.
2. Push your project files to the repository (or upload the project files using the web interface).

### Step 2: Deploy on Render
1. Visit [https://render.com](https://render.com) and sign in with GitHub.
2. Click **New +** -> **Web Service**.
3. Select your `dlsa-porbandar` repository.
4. Fill in the details:
   - **Name**: `dlsa-porbandar`
   - **Language**: `Python 3`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
5. In **Environment Variables**:
   - `DB_TYPE` = `sqlite`
   - `SECRET_KEY` = `dlsa_portal_production_2026_secure`
6. Click **Deploy Web Service**.

### Your Live URL:
`https://dlsa-porbandar.onrender.com`

---

## Verification Checklist After Deployment
- [ ] Visit home page `/` to verify banner, 44 PLV counters, and bilingual switch (English/Gujarati).
- [ ] Test legal aid application submission on `/apply` and note the tracking number.
- [ ] Check `/track?app_no=...` to ensure tracking works.
- [ ] Log in to Admin panel `/admin/login` (`admin` / `admin123` or your configured credentials).
- [ ] Verify `/report` and `/download-report` to view Himanshu Parmar's Project Report PDF.
