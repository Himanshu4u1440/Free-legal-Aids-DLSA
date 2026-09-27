"""
Microsoft SQL Server Setup & Migration Utility for DLSA Project
--------------------------------------------------------------
This script tests your MS SQL Server connection, creates the DLSA_DB database if needed,
and provisions all tables, views, and seed data.
"""

import sys
import urllib.parse
from sqlalchemy import create_engine, text
from config import Config
from models import Base
from seed_data import seed_database

def check_and_setup_mssql():
    print("=" * 70)
    print("  DISTRICT LEGAL SERVICES AUTHORITY (DLSA) - MS SQL SETUP WIZARD")
    print("=" * 70)
    print(f"Target Server : {Config.DB_SERVER}")
    print(f"Target Database : {Config.DB_DATABASE}")
    print(f"ODBC Driver   : {Config.DB_DRIVER}")
    print(f"Windows Auth  : {Config.DB_TRUSTED_CONNECTION}")
    if not Config.DB_TRUSTED_CONNECTION:
        print(f"SQL User      : {Config.DB_USER}")
    print("-" * 70)

    # 1. Connect to master database first to check/create target database
    master_params = [
        f"DRIVER={{{Config.DB_DRIVER}}}",
        f"SERVER={Config.DB_SERVER}",
        "DATABASE=master"
    ]
    if Config.DB_TRUSTED_CONNECTION:
        master_params.append("Trusted_Connection=yes")
    else:
        if Config.DB_USER:
            master_params.append(f"UID={Config.DB_USER}")
        if Config.DB_PASSWORD:
            master_params.append(f"PWD={Config.DB_PASSWORD}")
    master_params.append("TrustServerCertificate=yes")

    master_odbc = ";".join(master_params) + ";"
    master_uri = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(master_odbc)}"

    print("[Step 1/3] Connecting to MS SQL Server instance...")
    try:
        master_engine = create_engine(master_uri, isolation_level="AUTOCOMMIT")
        with master_engine.connect() as conn:
            version = conn.execute(text("SELECT @@VERSION")).scalar()
            print(f"[SUCCESS] Connected to MS SQL Server!\n  Version details: {version[:80]}...\n")
            
            # Check/Create Database
            print(f"[Step 2/3] Checking if database '{Config.DB_DATABASE}' exists...")
            check_sql = text(f"SELECT database_id FROM sys.databases WHERE name = '{Config.DB_DATABASE}'")
            exists = conn.execute(check_sql).scalar()
            
            if not exists:
                print(f"  Creating database '{Config.DB_DATABASE}'...")
                conn.execute(text(f"CREATE DATABASE [{Config.DB_DATABASE}]"))
                print(f"  [SUCCESS] Database '{Config.DB_DATABASE}' created.")
            else:
                print(f"  Database '{Config.DB_DATABASE}' already exists.")

    except Exception as e:
        print("\n[ERROR] Could not connect to MS SQL Server.")
        print(f"Details: {e}")
        print("\nTips for setting up MS SQL Server:")
        print("  1. Make sure 'SQL Server (MSSQLSERVER)' or 'SQL Server (SQLEXPRESS)' service is running.")
        print("  2. In SQL Server Configuration Manager, ensure 'TCP/IP' protocol is ENABLED under Network Configuration.")
        print("  3. If your instance is named, set DB_SERVER=localhost\\SQLEXPRESS in .env")
        print("  4. For SQL Server Authentication, set DB_TRUSTED_CONNECTION=no and provide DB_USER and DB_PASSWORD.")
        print("  5. You can also run schema_mssql.sql directly inside SQL Server Management Studio (SSMS).")
        return False

    # 3. Create tables and seed data
    print(f"\n[Step 3/3] Creating tables and seeding initial data in '{Config.DB_DATABASE}'...")
    try:
        from database import init_database
        Config.DB_TYPE = "mssql"
        init_database()
        seed_database()
        print("[SUCCESS] All DLSA tables, members, PLVs, deployments, and schemes are ready in MS SQL Server!")
        print("=" * 70)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create tables or seed data: {e}")
        return False

if __name__ == "__main__":
    success = check_and_setup_mssql()
    sys.exit(0 if success else 1)
