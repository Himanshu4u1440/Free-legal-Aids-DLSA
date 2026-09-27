-- ============================================================================
-- DISTRICT LEGAL SERVICES AUTHORITY (DLSA) PORBANDAR (GUJARAT)
-- MS SQL SERVER DATABASE SCHEMA & SEED DATA
-- Compatible with: Microsoft SQL Server 2016, 2019, 2022, Azure SQL, SSMS
-- ============================================================================

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'DLSA_DB')
BEGIN
    CREATE DATABASE DLSA_DB;
END
GO

USE DLSA_DB;
GO

-- Drop tables in reverse order of foreign keys if re-running
IF OBJECT_ID('dbo.PLVAssignments', 'U') IS NOT NULL DROP TABLE dbo.PLVAssignments;
IF OBJECT_ID('dbo.LegalAidApplications', 'U') IS NOT NULL DROP TABLE dbo.LegalAidApplications;
IF OBJECT_ID('dbo.LokAdalatEvents', 'U') IS NOT NULL DROP TABLE dbo.LokAdalatEvents;
IF OBJECT_ID('dbo.PLVs', 'U') IS NOT NULL DROP TABLE dbo.PLVs;
IF OBJECT_ID('dbo.Deployments', 'U') IS NOT NULL DROP TABLE dbo.Deployments;
IF OBJECT_ID('dbo.Members', 'U') IS NOT NULL DROP TABLE dbo.Members;
IF OBJECT_ID('dbo.Schemes', 'U') IS NOT NULL DROP TABLE dbo.Schemes;
IF OBJECT_ID('dbo.AdminUsers', 'U') IS NOT NULL DROP TABLE dbo.AdminUsers;
GO

-- ============================================================================
-- TABLE: Members (Leadership, Management & High Ranks of DLSA Porbandar)
-- ============================================================================
CREATE TABLE dbo.Members (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(150) NOT NULL,
    designation NVARCHAR(150) NOT NULL,
    rank_order INT NOT NULL DEFAULT 99,
    category NVARCHAR(80) NOT NULL,
    qualification NVARCHAR(200) NULL,
    office_address NVARCHAR(300) NULL,
    email NVARCHAR(120) NULL,
    phone NVARCHAR(50) NULL,
    bio NVARCHAR(MAX) NULL,
    responsibilities NVARCHAR(MAX) NULL,
    photo_url NVARCHAR(300) NULL,
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO

-- ============================================================================
-- TABLE: Deployments (Places where PLVs & Clinics are Deployed in Porbandar)
-- ============================================================================
CREATE TABLE dbo.Deployments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    place_name NVARCHAR(200) NOT NULL,
    place_type NVARCHAR(80) NOT NULL,
    address NVARCHAR(300) NOT NULL,
    area_locality NVARCHAR(100) NOT NULL,
    police_jurisdiction NVARCHAR(120) NULL,
    incharge_officer NVARCHAR(150) NULL,
    contact_phone NVARCHAR(50) NULL,
    operating_hours NVARCHAR(100) DEFAULT '10:00 AM - 05:00 PM (Mon-Sat)',
    services_offered NVARCHAR(MAX) NULL,
    facilities_available NVARCHAR(MAX) NULL,
    latitude DECIMAL(9,6) NULL,
    longitude DECIMAL(9,6) NULL,
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO

-- ============================================================================
-- TABLE: PLVs (Para Legal Volunteers - DLSA Porbandar Certified Cadre)
-- ============================================================================
CREATE TABLE dbo.PLVs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    registration_no NVARCHAR(50) NOT NULL UNIQUE,
    dlsa_sr_no NVARCHAR(20) NULL,
    full_name NVARCHAR(150) NOT NULL,
    gender NVARCHAR(20) NOT NULL,
    date_of_birth DATE NULL,
    qualification NVARCHAR(150) NULL,
    primary_occupation NVARCHAR(100) NULL,
    languages_known NVARCHAR(200) NULL,
    phone NVARCHAR(50) NOT NULL,
    email NVARCHAR(120) NULL,
    residential_address NVARCHAR(300) NULL,
    police_verification_status NVARCHAR(50) DEFAULT 'Verified',
    training_batch NVARCHAR(100) NULL,
    card_issued_date NVARCHAR(50) DEFAULT '20-07-2026',
    validity_date NVARCHAR(50) DEFAULT '07-03-2027',
    date_of_enrollment DATE NOT NULL DEFAULT GETDATE(),
    status NVARCHAR(50) NOT NULL DEFAULT 'Active',
    specialization_area NVARCHAR(200) NULL,
    photo_url NVARCHAR(300) NULL,
    achievements_notes NVARCHAR(MAX) NULL,
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO

-- ============================================================================
-- TABLE: PLVAssignments (Duty Roster & Place Mapping)
-- ============================================================================
CREATE TABLE dbo.PLVAssignments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    plv_id INT NOT NULL FOREIGN KEY REFERENCES dbo.PLVs(id) ON DELETE CASCADE,
    deployment_id INT NOT NULL FOREIGN KEY REFERENCES dbo.Deployments(id) ON DELETE CASCADE,
    duty_role NVARCHAR(150) NOT NULL,
    days_of_week NVARCHAR(100) DEFAULT 'Monday to Saturday',
    shift_hours NVARCHAR(80) DEFAULT '10:00 AM - 05:00 PM',
    assigned_from DATE NOT NULL,
    assigned_to DATE NULL,
    supervisor_remarks NVARCHAR(300) NULL,
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO

-- ============================================================================
-- TABLE: Schemes (NALSA & GSLSA Welfare & Legal Aid Schemes)
-- ============================================================================
CREATE TABLE dbo.Schemes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    scheme_code NVARCHAR(50) NOT NULL UNIQUE,
    title NVARCHAR(250) NOT NULL,
    target_group NVARCHAR(150) NOT NULL,
    short_description NVARCHAR(500) NOT NULL,
    detailed_objectives NVARCHAR(MAX) NOT NULL,
    eligibility_criteria NVARCHAR(MAX) NOT NULL,
    benefits NVARCHAR(MAX) NOT NULL,
    required_documents NVARCHAR(MAX) NOT NULL,
    application_process NVARCHAR(MAX) NOT NULL,
    nodal_officer NVARCHAR(150) NULL,
    icon_class NVARCHAR(80) DEFAULT 'bi-shield-check',
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO

-- ============================================================================
-- TABLE: LegalAidApplications (Public Online Requests for Free Legal Help)
-- ============================================================================
CREATE TABLE dbo.LegalAidApplications (
    id INT IDENTITY(1,1) PRIMARY KEY,
    application_number NVARCHAR(50) NOT NULL UNIQUE,
    applicant_name NVARCHAR(150) NOT NULL,
    gender NVARCHAR(20) NOT NULL,
    phone NVARCHAR(50) NOT NULL,
    email NVARCHAR(120) NULL,
    id_proof_type NVARCHAR(50) NULL,
    id_proof_number NVARCHAR(100) NULL,
    residential_address NVARCHAR(300) NOT NULL,
    category NVARCHAR(80) NOT NULL,
    annual_income DECIMAL(12,2) NULL,
    case_type NVARCHAR(80) NOT NULL,
    court_jurisdiction NVARCHAR(150) NULL,
    opposing_party_details NVARCHAR(250) NULL,
    case_summary NVARCHAR(MAX) NOT NULL,
    assigned_counsel NVARCHAR(150) NULL,
    assigned_counsel_phone NVARCHAR(50) NULL,
    assigned_plv_id INT NULL FOREIGN KEY REFERENCES dbo.PLVs(id) ON DELETE SET NULL,
    status NVARCHAR(50) NOT NULL DEFAULT 'Submitted',
    status_notes NVARCHAR(MAX) NULL,
    last_sms_notification NVARCHAR(MAX) NULL,
    last_sms_sent_at DATETIME2 NULL,
    submitted_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO

-- ============================================================================
-- TABLE: LokAdalatEvents (Upcoming Lok Adalats in Porbandar)
-- ============================================================================
CREATE TABLE dbo.LokAdalatEvents (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(200) NOT NULL,
    event_type NVARCHAR(80) NOT NULL,
    event_date DATE NOT NULL,
    time_schedule NVARCHAR(80) DEFAULT '10:00 AM onwards',
    venue NVARCHAR(250) NOT NULL,
    benches_count INT DEFAULT 8,
    presiding_officers NVARCHAR(MAX) NULL,
    eligible_matters NVARCHAR(MAX) NULL,
    contact_person NVARCHAR(150) NULL,
    is_active BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO

-- ============================================================================
-- TABLE: AdminUsers (Staff & Management Login)
-- ============================================================================
CREATE TABLE dbo.AdminUsers (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    full_name NVARCHAR(150) NOT NULL,
    designation NVARCHAR(120) NOT NULL,
    role NVARCHAR(50) NOT NULL DEFAULT 'Admin',
    is_active BIT NOT NULL DEFAULT 1,
    last_login DATETIME2 NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO

-- ============================================================================
-- VIEW & STORED PROCEDURES
-- ============================================================================
CREATE OR ALTER VIEW dbo.vw_ActivePLVDeployments AS
SELECT 
    p.id AS plv_id,
    p.dlsa_sr_no,
    p.registration_no,
    p.full_name AS plv_name,
    p.phone AS plv_phone,
    p.gender,
    p.residential_address,
    p.card_issued_date,
    p.validity_date,
    p.specialization_area,
    p.status AS plv_status,
    d.id AS deployment_id,
    d.place_name,
    d.place_type,
    d.area_locality,
    d.address AS deployment_address,
    d.contact_phone AS deployment_contact,
    pa.duty_role,
    pa.days_of_week,
    pa.shift_hours
FROM dbo.PLVs p
INNER JOIN dbo.PLVAssignments pa ON p.id = pa.plv_id AND pa.is_active = 1
INNER JOIN dbo.Deployments d ON pa.deployment_id = d.id AND d.is_active = 1
WHERE p.is_active = 1;
GO

PRINT 'DLSA Porbandar MS SQL Server Schema Created Successfully.';
GO
