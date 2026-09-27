from datetime import datetime, timezone, date
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Date, Numeric, ForeignKey
)
from sqlalchemy.orm import relationship
from database import Base

class Member(Base):
    __tablename__ = "Members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    designation = Column(String(150), nullable=False)
    rank_order = Column(Integer, nullable=False, default=99)
    category = Column(String(80), nullable=False)  # Judicial Leadership, Administration, Legal Aid Defense Counsel, Panel Advocates
    qualification = Column(String(200), nullable=True)
    office_address = Column(String(300), nullable=True)
    email = Column(String(120), nullable=True)
    phone = Column(String(50), nullable=True)
    bio = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)
    photo_url = Column(String(300), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "designation": self.designation,
            "rank_order": self.rank_order,
            "category": self.category,
            "qualification": self.qualification,
            "email": self.email,
            "phone": self.phone,
            "bio": self.bio,
            "responsibilities": self.responsibilities,
            "photo_url": self.photo_url or "/static/images/avatar_placeholder.png",
            "is_active": self.is_active
        }


class Deployment(Base):
    __tablename__ = "Deployments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    place_name = Column(String(200), nullable=False)
    place_type = Column(String(80), nullable=False)  # Court Front Office, Police Station, Central Jail / Sub-Jail, Legal Aid Clinic, Hospital Desk, Juvenile Justice Board, One Stop Centre (Sakhi)
    address = Column(String(300), nullable=False)
    area_locality = Column(String(100), nullable=False)
    police_jurisdiction = Column(String(120), nullable=True)
    incharge_officer = Column(String(150), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    operating_hours = Column(String(100), default="10:00 AM - 05:00 PM (Mon-Sat)")
    services_offered = Column(Text, nullable=True)
    facilities_available = Column(Text, nullable=True)
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    assignments = relationship("PLVAssignment", back_populates="deployment", cascade="all, delete-orphan", lazy="joined")

    @property
    def active_assignments(self):
        """Returns only assignments where both the assignment AND the assigned PLV are active."""
        return [
            a for a in self.assignments 
            if a.is_active and a.plv and a.plv.is_active and a.plv.status == "Active"
        ]

    def to_dict(self):
        return {
            "id": self.id,
            "place_name": self.place_name,
            "place_type": self.place_type,
            "address": self.address,
            "area_locality": self.area_locality,
            "police_jurisdiction": self.police_jurisdiction,
            "incharge_officer": self.incharge_officer,
            "contact_phone": self.contact_phone,
            "operating_hours": self.operating_hours,
            "services_offered": self.services_offered,
            "facilities_available": self.facilities_available,
            "is_active": self.is_active,
            "assigned_plvs_count": len(self.active_assignments)
        }


class PLV(Base):
    __tablename__ = "PLVs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    registration_no = Column(String(50), unique=True, nullable=False)
    dlsa_sr_no = Column(String(20), nullable=True)  # e.g., "01", "03", "44" from DLSA Porbandar Card
    full_name = Column(String(150), nullable=False)
    gender = Column(String(20), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    qualification = Column(String(150), nullable=True)
    primary_occupation = Column(String(100), nullable=True)
    languages_known = Column(String(200), nullable=True)
    phone = Column(String(50), nullable=False)
    email = Column(String(120), nullable=True)
    residential_address = Column(String(300), nullable=True)
    police_verification_status = Column(String(50), default="Verified")
    training_batch = Column(String(100), nullable=True)
    card_issued_date = Column(String(50), default="20-07-2026")
    validity_date = Column(String(50), default="07-03-2027")
    date_of_enrollment = Column(Date, default=date.today, nullable=False)
    status = Column(String(50), default="Active", nullable=False)  # Active, On-Duty, Leave, Retired
    specialization_area = Column(String(200), nullable=True)
    photo_url = Column(String(300), nullable=True)
    achievements_notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    assignments = relationship("PLVAssignment", back_populates="plv", cascade="all, delete-orphan", lazy="joined")
    applications = relationship("LegalAidApplication", back_populates="assigned_plv")

    @property
    def current_deployment(self):
        """Returns the place name of the currently active deployment or default."""
        if not self.is_active or self.status != "Active":
            return "On Leave / Inactive (General Cadre)"
        active = next((a for a in self.assignments if a.is_active), None)
        if active and active.deployment:
            return active.deployment.place_name
        return "DLSA Porbandar General Cadre"

    @property
    def current_role(self):
        """Returns the active duty role of the volunteer."""
        active = next((a for a in self.assignments if a.is_active), None)
        return active.duty_role if active else "Para Legal Volunteer (PLV)"

    def to_dict(self, include_private=False):
        """Returns dictionary representation of PLV. By default, private details (phone, street address) are omitted for public privacy."""
        active_assignment = next((a for a in self.assignments if a.is_active), None)
        data = {
            "id": self.id,
            "dlsa_sr_no": self.dlsa_sr_no or "",
            "registration_no": self.registration_no,
            "full_name": self.full_name,
            "gender": self.gender,
            "designation": "PLV (Para Legal Volunteer)",
            "status": self.status,
            "photo_url": self.photo_url or "/static/images/avatar_placeholder.svg",
            "training_batch": self.training_batch or "DLSA Porbandar Certified",
            "card_issued_date": self.card_issued_date or "20-07-2026",
            "validity_date": self.validity_date or "07-03-2027",
            "current_deployment": self.current_deployment,
            "current_role": self.current_role,
            "is_active": self.is_active and self.status == "Active",
            "jurisdiction": "Porbandar District, Gujarat"
        }
        if include_private:
            data.update({
                "phone": self.phone,
                "email": self.email,
                "residential_address": self.residential_address,
                "qualification": self.qualification,
                "primary_occupation": self.primary_occupation,
                "languages_known": self.languages_known
            })
        return data

    def to_admin_dict(self):
        """Returns full PLV information including private contact and address for administrative management."""
        return self.to_dict(include_private=True)


class PLVAssignment(Base):
    __tablename__ = "PLVAssignments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    plv_id = Column(Integer, ForeignKey("PLVs.id", ondelete="CASCADE"), nullable=False)
    deployment_id = Column(Integer, ForeignKey("Deployments.id", ondelete="CASCADE"), nullable=False)
    duty_role = Column(String(150), nullable=False)
    days_of_week = Column(String(100), default="Monday to Friday")
    shift_hours = Column(String(80), default="10:00 AM - 04:00 PM")
    assigned_from = Column(Date, default=date.today, nullable=False)
    assigned_to = Column(Date, nullable=True)
    supervisor_remarks = Column(String(300), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    plv = relationship("PLV", back_populates="assignments", lazy="joined")
    deployment = relationship("Deployment", back_populates="assignments", lazy="joined")


class Scheme(Base):
    __tablename__ = "Schemes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scheme_code = Column(String(50), unique=True, nullable=False)
    title = Column(String(250), nullable=False)
    target_group = Column(String(150), nullable=False)
    short_description = Column(String(500), nullable=False)
    detailed_objectives = Column(Text, nullable=False)
    eligibility_criteria = Column(Text, nullable=False)
    benefits = Column(Text, nullable=False)
    required_documents = Column(Text, nullable=False)
    application_process = Column(Text, nullable=False)
    nodal_officer = Column(String(150), nullable=True)
    icon_class = Column(String(80), default="bi-shield-check")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "scheme_code": self.scheme_code,
            "title": self.title,
            "target_group": self.target_group,
            "short_description": self.short_description,
            "detailed_objectives": self.detailed_objectives,
            "eligibility_criteria": self.eligibility_criteria,
            "benefits": self.benefits,
            "required_documents": self.required_documents,
            "application_process": self.application_process,
            "nodal_officer": self.nodal_officer,
            "icon_class": self.icon_class
        }


class LegalAidApplication(Base):
    __tablename__ = "LegalAidApplications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_number = Column(String(50), unique=True, nullable=False)
    applicant_name = Column(String(150), nullable=False)
    gender = Column(String(20), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(120), nullable=True)
    id_proof_type = Column(String(50), nullable=True)
    id_proof_number = Column(String(100), nullable=True)
    residential_address = Column(String(300), nullable=False)
    category = Column(String(80), nullable=False)
    annual_income = Column(Numeric(12, 2), nullable=True)
    case_type = Column(String(80), nullable=False)
    court_jurisdiction = Column(String(150), nullable=True)
    opposing_party_details = Column(String(250), nullable=True)
    case_summary = Column(Text, nullable=False)
    assigned_counsel = Column(String(150), nullable=True)
    assigned_counsel_phone = Column(String(50), nullable=True)
    assigned_plv_id = Column(Integer, ForeignKey("PLVs.id", ondelete="SET NULL"), nullable=True)
    status = Column(String(50), default="Submitted", nullable=False)  # Submitted, Under Scrutiny, Counsel Assigned, Mediation/Lok Adalat, Disposed/Resolved, Rejected
    status_notes = Column(Text, nullable=True)
    last_sms_notification = Column(Text, nullable=True)
    last_sms_sent_at = Column(DateTime, nullable=True)
    submitted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    assigned_plv = relationship("PLV", back_populates="applications", lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "application_number": self.application_number,
            "applicant_name": self.applicant_name,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "category": self.category,
            "annual_income": float(self.annual_income) if self.annual_income is not None else 0.0,
            "case_type": self.case_type,
            "court_jurisdiction": self.court_jurisdiction,
            "case_summary": self.case_summary,
            "assigned_counsel": self.assigned_counsel,
            "assigned_counsel_phone": self.assigned_counsel_phone or "",
            "assigned_plv": self.assigned_plv.full_name if self.assigned_plv else "Unassigned",
            "status": self.status,
            "status_notes": self.status_notes,
            "last_sms_notification": self.last_sms_notification or "",
            "last_sms_sent_at": self.last_sms_sent_at.strftime("%d %b %Y, %I:%M %p") if self.last_sms_sent_at else "",
            "submitted_at": self.submitted_at.strftime("%d %b %Y, %I:%M %p") if self.submitted_at else ""
        }


class LokAdalatEvent(Base):
    __tablename__ = "LokAdalatEvents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    event_type = Column(String(80), nullable=False)
    event_date = Column(Date, nullable=False)
    time_schedule = Column(String(80), default="10:00 AM onwards")
    venue = Column(String(250), nullable=False)
    benches_count = Column(Integer, default=5)
    presiding_officers = Column(Text, nullable=True)
    eligible_matters = Column(Text, nullable=True)
    contact_person = Column(String(150), nullable=True)
    assigned_plvs = Column(Text, nullable=True)  # List or notes of assigned PLVs on duty
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "event_type": self.event_type,
            "event_date": self.event_date.strftime("%Y-%m-%d") if self.event_date else "",
            "time_schedule": self.time_schedule,
            "venue": self.venue,
            "benches_count": self.benches_count,
            "presiding_officers": self.presiding_officers,
            "eligible_matters": self.eligible_matters,
            "contact_person": self.contact_person,
            "assigned_plvs": self.assigned_plvs or "",
            "is_active": self.is_active
        }


class AdminUser(Base):
    __tablename__ = "AdminUsers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    designation = Column(String(120), nullable=False)
    role = Column(String(50), default="Admin", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
