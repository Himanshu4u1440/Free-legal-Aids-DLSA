import os
import random
import logging
from datetime import datetime, timezone, date
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for, 
    flash, session, jsonify, g, make_response, send_file
)
from werkzeug.security import check_password_hash

from config import Config
from database import SessionLocal, ACTIVE_DB_TYPE, DB_CONNECTION_INFO, check_and_apply_migrations, engine
from models import (
    Member, Deployment, PLV, PLVAssignment, Scheme, 
    LegalAidApplication, LokAdalatEvent, AdminUser
)
from seed_data import seed_database
from translations import get_translation, TRANSLATIONS_DICT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dlsa.app")

app = Flask(__name__)
app.config.from_object(Config)

# Ensure migrations and tables exist
try:
    check_and_apply_migrations(engine)
    seed_database()
    with app.app_context():
        _init_db = SessionLocal()
        _e1 = _init_db.query(LokAdalatEvent).filter(LokAdalatEvent.id == 1).first()
        if _e1:
            _e1.assigned_plvs = "PLV Nimisha Joshi (Sr. No. 01), PLV Parth Rathod (Sr. No. 03), PLV Nidhi Mashru (Sr. No. 04)"
        _e2 = _init_db.query(LokAdalatEvent).filter(LokAdalatEvent.id == 2).first()
        if _e2:
            _e2.assigned_plvs = "PLV Hetvi Dave (Sr. No. 05), PLV Anjali Vaghela (Sr. No. 06)"
        _e3 = _init_db.query(LokAdalatEvent).filter(LokAdalatEvent.id == 3).first()
        if _e3:
            _e3.assigned_plvs = "PLV Nimisha Joshi (Sr. No. 01), PLV Himanshu Parmar (Sr. No. 32)"
        _init_db.commit()
        _init_db.close()
except Exception as e:
    logger.warning(f"Database initialization warning: {e}")

def get_db():
    """Returns the per-request SQLAlchemy session stored in Flask's g object."""
    if "db" not in g:
        g.db = SessionLocal()
    return g.db

@app.teardown_appcontext
def teardown_db(exception=None):
    """Closes database session after request finishes."""
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Inject active database name and language into all templates
@app.context_processor
def inject_global_data():
    lang = session.get("lang") or request.cookies.get("dlsa_lang") or "en"
    if lang not in ["en", "gu"]:
        lang = "en"
    session["lang"] = lang
    return {
        "active_db": ACTIVE_DB_TYPE,
        "active_db_info": DB_CONNECTION_INFO,
        "current_year": datetime.now(timezone.utc).year,
        "current_lang": lang,
        "t": lambda text: get_translation(text, lang),
        "translations_dict": TRANSLATIONS_DICT
    }

@app.template_filter('t')
def translate_filter(text):
    lang = session.get("lang") or request.cookies.get("dlsa_lang") or "en"
    if lang not in ["en", "gu"]:
        lang = "en"
    return get_translation(text, lang)

@app.route("/set-language/<lang>")
def set_language(lang):
    """Switch portal language between English and Gujarati."""
    target_lang = lang if lang in ["en", "gu"] else "en"
    session["lang"] = target_lang
    referer = request.headers.get("Referer") or url_for("index")
    resp = make_response(redirect(referer))
    resp.set_cookie("dlsa_lang", target_lang, max_age=60*60*24*365, path="/")
    resp.set_cookie("googtrans", f"/en/{target_lang}", max_age=60*60*24*365, path="/")
    return resp


# Admin authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_user"):
            flash("Please log in to access the DLSA administrative portal.", "warning")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function

def send_live_sms(phone, message_text):
    """
    Attempts to dispatch real SMS through Fast2SMS Gateway if FAST2SMS_API_KEY is configured.
    Falls back gracefully without throwing errors if no key is configured or offline.
    """
    api_key = os.getenv("FAST2SMS_API_KEY")
    if not api_key:
        return False, "No FAST2SMS_API_KEY configured"

    import re
    import urllib.request
    import json
    
    # Strip any formatting, non-digit characters, and Indian +91 / 0 prefix
    digits_only = re.sub(r"\D", "", phone or "")
    if digits_only.startswith("91") and len(digits_only) == 12:
        clean_phone = digits_only[2:]
    elif digits_only.startswith("0") and len(digits_only) == 11:
        clean_phone = digits_only[1:]
    else:
        clean_phone = digits_only

    if len(clean_phone) != 10:
        return False, f"Not a valid 10-digit Indian phone number ({phone})"

    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = json.dumps({
        "route": "q",
        "message": message_text[:155],
        "language": "english",
        "flash": 0,
        "numbers": clean_phone
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "authorization": api_key,
            "Content-Type": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("return") is True:
                logger.info(f"[LIVE SMS DELIVERED] Successfully sent SMS to {clean_phone} via Fast2SMS: {data}")
                return True, "SMS delivered to mobile via Fast2SMS Gateway"
            else:
                logger.warning(f"[FAST2SMS GATEWAY NOTICE] {data}")
                return False, data.get("message", "Fast2SMS error")
    except Exception as ex:
        logger.warning(f"[FAST2SMS EXCEPTION] Failed to dispatch live SMS: {ex}")
        return False, str(ex)

def dispatch_status_sms(app_record):
    """
    Dispatches SMS to citizen mobile number for:
    - Submission
    - Under Scrutiny
    - Counsel Assigned (with counsel name & counsel contact phone)
    - Disposed / Resolved
    - Mediation / Lok Adalat
    - Rejection
    Saves the notification text and sent timestamp into the database.
    Attempts live telecom delivery via SMS gateway (Fast2SMS) if API key is provided.
    """
    name = app_record.applicant_name or "Applicant"
    app_no = app_record.application_number
    status = app_record.status
    phone = app_record.phone

    if status == "Under Scrutiny":
        msg = (
            f"[DLSA-SMS] Dear {name}, your Legal Aid App #{app_no} is now UNDER SCRUTINY by the DLSA Porbandar Legal Committee. "
            f"Verification of documents is underway. You can track status at dlsa-porbandar.gov.in/track?app_no={app_no}"
        )
    elif status == "Counsel Assigned":
        counsel_name = app_record.assigned_counsel or "Legal Aid Defense Counsel"
        counsel_contact = f" | Contact: {app_record.assigned_counsel_phone}" if app_record.assigned_counsel_phone else ""
        msg = (
            f"[DLSA-SMS] Dear {name}, Free Legal Counsel '{counsel_name}'{counsel_contact} has been assigned to represent your case #{app_no}. "
            f"You may contact your counsel for defense. DLSA Helpline: 0286-2244222."
        )
    elif status == "Disposed/Resolved":
        msg = (
            f"[DLSA-SMS] Dear {name}, your Legal Aid Application #{app_no} has been DISPOSED / RESOLVED by DLSA Porbandar. "
            f"Please visit DLSA Front Office to collect the final order copy and case closure certificate."
        )
    elif status == "Mediation/Lok Adalat":
        msg = (
            f"[DLSA-SMS] Dear {name}, your case #{app_no} has been referred to MEDIATION / LOK ADALAT for amicable settlement. "
            f"Formal summons/hearing schedule will follow. DLSA Helpline: 0286-2244222."
        )
    elif status == "Rejected":
        msg = (
            f"[DLSA-SMS] Dear {name}, your Legal Aid App #{app_no} status has been updated: Application could not be admitted under NALSA Section 12 criteria. "
            f"Contact DLSA Porbandar Front Office for clarification."
        )
    else:  # Submitted
        msg = (
            f"[DLSA-SMS] Dear {name}, your Free Legal Aid Application #{app_no} has been submitted successfully to DLSA Porbandar. "
            f"Awaiting scrutiny. Track anytime online: dlsa-porbandar.gov.in/track?app_no={app_no}"
        )

    app_record.last_sms_notification = msg
    app_record.last_sms_sent_at = datetime.now(timezone.utc)
    logger.info(f"[SMS DISPATCH] Sent to {phone}: {msg}")

    # Dispatch to live cellular gateway if key configured
    sent, note = send_live_sms(phone, msg)
    if sent:
        logger.info(f"[GATEWAY DISPATCH] Live SMS successfully delivered to {phone}")
    else:
        logger.info(f"[IN-APP LOG] SMS notification queued ({note})")

    return msg

# ============================================================================
# PUBLIC ROUTES
# ============================================================================

@app.route("/")
def index():
    """Homepage of DLSA portal with live stats, high ranks, PLVs, and schemes."""
    db = get_db()
    members = db.query(Member).filter(Member.is_active == True).order_by(Member.rank_order.asc()).all()
    plvs = db.query(PLV).filter(PLV.is_active == True).all()
    deployments = db.query(Deployment).filter(Deployment.is_active == True).all()
    schemes = db.query(Scheme).filter(Scheme.is_active == True).all()
    events = db.query(LokAdalatEvent).filter(LokAdalatEvent.is_active == True).order_by(LokAdalatEvent.event_date.asc()).all()
    applications_count = db.query(LegalAidApplication).count()
    resolved_count = db.query(LegalAidApplication).filter(LegalAidApplication.status.in_(["Counsel Assigned", "Disposed/Resolved"])).count()

    stats = {
        "total_plvs": len(plvs),
        "active_plvs": len([p for p in plvs if p.status in ("Active", "On-Duty")]),
        "total_deployments": len(deployments),
        "total_schemes": len(schemes),
        "total_applications": applications_count,
        "resolved_cases": resolved_count
    }

    return render_template(
        "index.html",
        active_page="home",
        stats=stats,
        members=members,
        plvs=plvs,
        deployments=deployments,
        schemes=schemes,
        events=events
    )

@app.route("/leadership")
def leadership():
    """Top High Ranks & Management Hierarchy of DLSA."""
    db = get_db()
    members = db.query(Member).filter(Member.is_active == True).order_by(Member.rank_order.asc()).all()
    return render_template("leadership.html", active_page="leadership", members=members)

@app.route("/plv-portal")
def plv_portal():
    """Para Legal Volunteers portal with 12 duties and active directory."""
    db = get_db()
    plvs = db.query(PLV).filter(PLV.is_active == True).order_by(PLV.full_name.asc()).all()
    return render_template("plv.html", active_page="plv", plvs=plvs)

@app.route("/deployments")
def deployments():
    """Places where PLVs and Legal Aid Clinics are deployed."""
    db = get_db()
    deployments_list = db.query(Deployment).filter(Deployment.is_active == True).order_by(Deployment.place_type.asc()).all()
    return render_template("deployments.html", active_page="deployments", deployments=deployments_list)

@app.route("/schemes")
def schemes():
    """Welfare and legal aid schemes."""
    db = get_db()
    schemes_list = db.query(Scheme).filter(Scheme.is_active == True).order_by(Scheme.id.asc()).all()
    return render_template("schemes.html", active_page="schemes", schemes=schemes_list)

@app.route("/apply", methods=["GET", "POST"])
def apply_legal_aid():
    """Citizen application form for 100% Free Legal Aid."""
    db = get_db()
    if request.method == "POST":
        current_year = datetime.now(timezone.utc).year
        random_num = random.randint(1000, 9999)
        app_no = f"DLSA-{current_year}-{random_num}"

        # Ensure uniqueness
        while db.query(LegalAidApplication).filter(LegalAidApplication.application_number == app_no).first():
            random_num = random.randint(1000, 9999)
            app_no = f"DLSA-{current_year}-{random_num}"

        applicant_name = request.form.get("applicant_name", "").strip()
        gender = request.form.get("gender", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip() or None
        id_proof_type = request.form.get("id_proof_type", "").strip() or None
        id_proof_number = request.form.get("id_proof_number", "").strip() or None
        residential_address = request.form.get("residential_address", "").strip()
        category = request.form.get("category", "").strip()
        annual_income_str = request.form.get("annual_income", "0").strip()
        case_type = request.form.get("case_type", "").strip()
        court_jurisdiction = request.form.get("court_jurisdiction", "").strip() or None
        opposing_party_details = request.form.get("opposing_party_details", "").strip() or None
        case_summary = request.form.get("case_summary", "").strip()
        assigned_plv_id = request.form.get("assigned_plv_id", "").strip()
        assigned_plv_id = int(assigned_plv_id) if assigned_plv_id and assigned_plv_id.isdigit() else None

        try:
            annual_income = float(annual_income_str)
        except ValueError:
            annual_income = 0.0

        new_application = LegalAidApplication(
            application_number=app_no,
            applicant_name=applicant_name,
            gender=gender,
            phone=phone,
            email=email,
            id_proof_type=id_proof_type,
            id_proof_number=id_proof_number,
            residential_address=residential_address,
            category=category,
            annual_income=annual_income,
            case_type=case_type,
            court_jurisdiction=court_jurisdiction,
            opposing_party_details=opposing_party_details,
            case_summary=case_summary,
            assigned_plv_id=assigned_plv_id,
            status="Submitted",
            status_notes="Application submitted successfully via online citizen portal. Awaiting scrutiny by DLSA Front Office team."
        )

        dispatch_status_sms(new_application)
        db.add(new_application)
        db.commit()

        flash(f"Your Legal Aid Application has been submitted! Your Tracking Number is: {app_no}. An acknowledgment SMS has been dispatched to {phone}.", "success")
        return redirect(url_for("track_application", app_no=app_no))

    # GET request - only list currently active PLVs for citizen assignment
    plvs = db.query(PLV).filter(PLV.is_active == True, PLV.status == "Active").all()
    plvs.sort(key=lambda x: int(x.dlsa_sr_no) if x.dlsa_sr_no and x.dlsa_sr_no.isdigit() else 999)
    selected_plv_id = request.args.get("plv_id", "")
    return render_template("apply.html", active_page="apply", plvs=plvs, selected_plv_id=selected_plv_id)

@app.route("/track")
def track_application():
    """Track legal aid application by tracking number."""
    app_no = request.args.get("app_no", "").strip()
    application = None
    if app_no:
        db = get_db()
        application = db.query(LegalAidApplication).filter(
            LegalAidApplication.application_number == app_no
        ).first()

    return render_template(
        "track.html",
        active_page="track",
        search_query=app_no,
        application=application
    )

# ============================================================================
# ADMINISTRATIVE & STAFF ROUTES
# ============================================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Admin and staff authentication."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        db = get_db()
        user = db.query(AdminUser).filter(AdminUser.username == username, AdminUser.is_active == True).first()
        if user and check_password_hash(user.password_hash, password):
            session["admin_user"] = user.username
            session["admin_name"] = user.full_name
            session["admin_role"] = user.role
            user.last_login = datetime.now(timezone.utc)
            db.commit()
            flash(f"Welcome back, {user.full_name}!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid username or password. Please check your credentials.", "danger")

    return render_template("admin/login.html")

@app.route("/admin/logout")
def admin_logout():
    """Admin logout."""
    session.clear()
    flash("You have been securely logged out.", "info")
    return redirect(url_for("index"))

@app.route("/admin")
@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    """Admin overview and applications management."""
    db = get_db()
    applications = db.query(LegalAidApplication).order_by(LegalAidApplication.submitted_at.desc()).all()
    plvs_count = db.query(PLV).count()
    deployments_count = db.query(Deployment).count()
    all_plvs = db.query(PLV).filter(PLV.is_active == True, PLV.status == "Active").all()
    all_plvs.sort(key=lambda x: int(x.dlsa_sr_no) if x.dlsa_sr_no and x.dlsa_sr_no.isdigit() else 999)

    return render_template(
        "admin/dashboard.html",
        applications=applications,
        plvs_count=plvs_count,
        deployments_count=deployments_count,
        all_plvs=all_plvs
    )

@app.route("/admin/applications/<int:app_id>/update", methods=["POST"])
@login_required
def admin_update_application(app_id):
    """Update status, assigned lawyer, counsel phone, and notes for an application with automated SMS dispatch."""
    db = get_db()
    app_record = db.query(LegalAidApplication).filter(LegalAidApplication.id == app_id).first()
    if not app_record:
        flash("Application record not found.", "danger")
        return redirect(url_for("admin_dashboard"))

    old_status = app_record.status
    old_counsel = app_record.assigned_counsel
    old_counsel_phone = app_record.assigned_counsel_phone

    new_status = request.form.get("status", app_record.status)
    new_counsel = request.form.get("assigned_counsel", "").strip() or None
    new_counsel_phone = request.form.get("assigned_counsel_phone", "").strip() or None
    assigned_plv = request.form.get("assigned_plv_id", "").strip()

    app_record.status = new_status
    app_record.assigned_counsel = new_counsel
    app_record.assigned_counsel_phone = new_counsel_phone
    app_record.assigned_plv_id = int(assigned_plv) if assigned_plv and assigned_plv.isdigit() else None
    app_record.status_notes = request.form.get("status_notes", "").strip()
    app_record.updated_at = datetime.now(timezone.utc)

    # Check if SMS dispatch should occur
    status_changed = (old_status != new_status)
    counsel_updated = (new_counsel != old_counsel) or (new_counsel_phone != old_counsel_phone)
    target_sms_status = new_status in ["Under Scrutiny", "Counsel Assigned", "Disposed/Resolved"]

    sms_dispatched = False
    if status_changed or target_sms_status or counsel_updated:
        dispatch_status_sms(app_record)
        sms_dispatched = True

    db.commit()

    if sms_dispatched:
        flash(f"Application {app_record.application_number} updated & status SMS successfully dispatched to {app_record.phone} (Status: {app_record.status}).", "success")
    else:
        flash(f"Application {app_record.application_number} updated successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/plvs")
@login_required
def admin_plvs():
    """Manage Para Legal Volunteers with full private info and column categorization."""
    db = get_db()
    plvs = db.query(PLV).all()
    # Sort numerically by dlsa_sr_no if present
    plvs.sort(key=lambda x: int(x.dlsa_sr_no) if x.dlsa_sr_no and x.dlsa_sr_no.isdigit() else 999)
    active_plvs = [p for p in plvs if p.status == "Active"]
    inactive_plvs = [p for p in plvs if p.status != "Active"]
    deployments_list = db.query(Deployment).filter(Deployment.is_active == True).all()
    return render_template(
        "admin/plvs.html", 
        plvs=plvs, 
        active_plvs=active_plvs,
        inactive_plvs=inactive_plvs,
        deployments=deployments_list
    )

@app.route("/admin/plvs/add", methods=["POST"])
@login_required
def admin_add_plv():
    """Enroll a new PLV."""
    db = get_db()
    registration_no = request.form.get("registration_no", "").strip()
    full_name = request.form.get("full_name", "").strip()
    gender = request.form.get("gender", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip() or None
    primary_occupation = request.form.get("primary_occupation", "").strip()
    qualification = request.form.get("qualification", "").strip() or None
    languages_known = request.form.get("languages_known", "").strip() or None
    specialization_area = request.form.get("specialization_area", "").strip() or None
    achievements_notes = request.form.get("achievements_notes", "").strip() or None

    photo_url = "/static/images/plv_m1.svg" if gender == "Male" else "/static/images/plv_f1.svg"

    new_plv = PLV(
        registration_no=registration_no,
        full_name=full_name,
        gender=gender,
        phone=phone,
        email=email,
        primary_occupation=primary_occupation,
        qualification=qualification,
        languages_known=languages_known,
        specialization_area=specialization_area,
        achievements_notes=achievements_notes,
        photo_url=photo_url,
        status="Active"
    )
    db.add(new_plv)
    db.commit()

    deployment_id = request.form.get("deployment_id", "").strip()
    duty_role = request.form.get("duty_role", "").strip() or "Helpdesk Assistant"
    if deployment_id and deployment_id.isdigit():
        assignment = PLVAssignment(
            plv_id=new_plv.id,
            deployment_id=int(deployment_id),
            duty_role=duty_role,
            assigned_from=date.today(),
            is_active=True
        )
        db.add(assignment)
        db.commit()

    flash(f"Para Legal Volunteer {full_name} enrolled successfully.", "success")
    return redirect(url_for("admin_plvs"))

@app.route("/admin/plvs/<int:plv_id>/toggle-status", methods=["POST"])
@login_required
def admin_toggle_plv_status(plv_id):
    """Toggles PLV status between Active and Inactive."""
    db = get_db()
    plv = db.query(PLV).filter(PLV.id == plv_id).first()
    if not plv:
        flash("PLV record not found.", "danger")
        return redirect(url_for("admin_plvs"))

    new_status = "Inactive" if plv.status == "Active" else "Active"
    plv.status = new_status
    plv.is_active = (new_status == "Active")
    for a in plv.assignments:
        a.is_active = plv.is_active
    db.commit()
    flash(f"Status of PLV {plv.full_name} (Sr. No. {plv.dlsa_sr_no or plv.id}) set to {new_status}. Clinic deployments updated.", "success")
    return redirect(url_for("admin_plvs"))

@app.route("/admin/plvs/mark-all-inactive", methods=["POST"])
@login_required
def admin_mark_all_plvs_inactive():
    """Mark all active PLVs as Inactive."""
    db = get_db()
    active_plvs = db.query(PLV).filter(PLV.status == "Active").all()
    count = len(active_plvs)
    for p in active_plvs:
        p.status = "Inactive"
        p.is_active = False
        for a in p.assignments:
            a.is_active = False
    db.commit()
    flash(f"Successfully marked all {count} active PLVs as Inactive.", "warning")
    return redirect(url_for("admin_plvs"))

@app.route("/admin/plvs/mark-all-active", methods=["POST"])
@login_required
def admin_mark_all_plvs_active():
    """Mark all inactive PLVs as Active."""
    db = get_db()
    inactive_plvs = db.query(PLV).filter(PLV.status != "Active").all()
    count = len(inactive_plvs)
    for p in inactive_plvs:
        p.status = "Active"
        p.is_active = True
        for a in p.assignments:
            a.is_active = True
    db.commit()
    flash(f"Successfully activated all {count} PLVs.", "success")
    return redirect(url_for("admin_plvs"))

@app.route("/admin/plvs/<int:plv_id>/update", methods=["POST"])
@login_required
def admin_update_plv(plv_id):
    """Update complete details of a PLV (including private address and phone)."""
    db = get_db()
    plv = db.query(PLV).filter(PLV.id == plv_id).first()
    if not plv:
        flash("PLV record not found.", "danger")
        return redirect(url_for("admin_plvs"))

    plv.full_name = request.form.get("full_name", plv.full_name).strip()
    plv.phone = request.form.get("phone", plv.phone).strip()
    plv.residential_address = request.form.get("residential_address", plv.residential_address).strip()
    plv.email = request.form.get("email", "").strip() or None
    plv.primary_occupation = request.form.get("primary_occupation", "").strip() or plv.primary_occupation
    plv.qualification = request.form.get("qualification", "").strip() or plv.qualification
    plv.status = request.form.get("status", plv.status).strip()
    plv.is_active = (plv.status == "Active")

    deployment_id = request.form.get("deployment_id", "").strip()
    duty_role = request.form.get("duty_role", "PLV Desk Facilitator").strip()

    # Reset old assignments
    for a in plv.assignments:
        a.is_active = False

    if deployment_id and deployment_id.isdigit():
        new_assignment = PLVAssignment(
            plv_id=plv.id,
            deployment_id=int(deployment_id),
            duty_role=duty_role,
            assigned_from=date.today(),
            is_active=plv.is_active
        )
        db.add(new_assignment)

    db.commit()
    flash(f"PLV {plv.full_name} (Sr. No. {plv.dlsa_sr_no or plv.id}) details updated successfully. Deployments synchronized.", "success")
    return redirect(url_for("admin_plvs"))

@app.route("/admin/plvs/<int:plv_id>/delete", methods=["POST"])
@login_required
def admin_delete_plv(plv_id):
    """Deletes / un-enrolls a PLV from DLSA roster."""
    db = get_db()
    plv = db.query(PLV).filter(PLV.id == plv_id).first()
    if not plv:
        flash("PLV record not found.", "danger")
        return redirect(url_for("admin_plvs"))

    name = plv.full_name
    db.delete(plv)
    db.commit()
    flash(f"PLV {name} has been removed from the DLSA roster.", "info")
    return redirect(url_for("admin_plvs"))

@app.route("/admin/deployments")
@login_required
def admin_deployments():
    """Manage Places of Deployment."""
    db = get_db()
    deployments_list = db.query(Deployment).order_by(Deployment.place_type.asc()).all()
    all_active_plvs = db.query(PLV).filter(PLV.is_active == True, PLV.status == "Active").all()
    all_active_plvs.sort(key=lambda x: int(x.dlsa_sr_no) if x.dlsa_sr_no and x.dlsa_sr_no.isdigit() else 999)
    return render_template("admin/deployments.html", deployments=deployments_list, all_active_plvs=all_active_plvs)

@app.route("/admin/deployments/<int:deployment_id>/assign", methods=["POST"])
@login_required
def admin_assign_plv_to_deployment(deployment_id):
    """Assigns an active PLV to a deployment center."""
    db = get_db()
    dep = db.query(Deployment).filter(Deployment.id == deployment_id).first()
    plv_id = request.form.get("plv_id")
    if not dep or not plv_id or not plv_id.isdigit():
        flash("Invalid deployment or PLV selection.", "danger")
        return redirect(url_for("admin_deployments"))

    plv = db.query(PLV).filter(PLV.id == int(plv_id)).first()
    if not plv:
        flash("PLV not found.", "danger")
        return redirect(url_for("admin_deployments"))

    # Deactivate existing assignments for this PLV
    for a in plv.assignments:
        a.is_active = False

    duty_role = request.form.get("duty_role", f"{dep.place_name} PLV").strip()
    new_assign = PLVAssignment(
        plv_id=plv.id,
        deployment_id=dep.id,
        duty_role=duty_role,
        assigned_from=date.today(),
        is_active=plv.is_active and (plv.status == "Active")
    )
    db.add(new_assign)
    db.commit()
    flash(f"PLV {plv.full_name} assigned to '{dep.place_name}' successfully.", "success")
    return redirect(url_for("admin_deployments"))

@app.route("/admin/deployments/<int:deployment_id>/unassign/<int:plv_id>", methods=["POST"])
@login_required
def admin_unassign_plv_from_deployment(deployment_id, plv_id):
    """Unassigns a PLV from a deployment center."""
    db = get_db()
    assignment = db.query(PLVAssignment).filter(
        PLVAssignment.deployment_id == deployment_id,
        PLVAssignment.plv_id == plv_id,
        PLVAssignment.is_active == True
    ).first()
    if assignment:
        assignment.is_active = False
        db.commit()
        flash(f"PLV unassigned from this deployment center successfully.", "info")
    else:
        flash("Assignment record not found.", "warning")
    return redirect(url_for("admin_deployments"))

@app.route("/admin/deployments/add", methods=["POST"])
@login_required
def admin_add_deployment():
    """Create a new deployment place."""
    db = get_db()
    new_place = Deployment(
        place_name=request.form.get("place_name", "").strip(),
        place_type=request.form.get("place_type", "").strip(),
        address=request.form.get("address", "").strip(),
        area_locality=request.form.get("area_locality", "").strip(),
        police_jurisdiction=request.form.get("police_jurisdiction", "").strip() or None,
        incharge_officer=request.form.get("incharge_officer", "").strip() or None,
        contact_phone=request.form.get("contact_phone", "").strip() or None,
        operating_hours=request.form.get("operating_hours", "10:00 AM - 05:00 PM (Mon-Sat)").strip(),
        services_offered=request.form.get("services_offered", "").strip()
    )
    db.add(new_place)
    db.commit()
    flash(f"Deployment place '{new_place.place_name}' added successfully.", "success")
    return redirect(url_for("admin_deployments"))

@app.route("/admin/leadership")
@login_required
def admin_leadership():
    """Manage High Ranks & Officials."""
    db = get_db()
    members = db.query(Member).order_by(Member.rank_order.asc()).all()
    return render_template("admin/leadership.html", members=members)

@app.route("/admin/leadership/add", methods=["POST"])
@login_required
def admin_add_member():
    """Add a new official / rank."""
    db = get_db()
    rank_order = int(request.form.get("rank_order", "99"))
    new_member = Member(
        name=request.form.get("name", "").strip(),
        designation=request.form.get("designation", "").strip(),
        rank_order=rank_order,
        category=request.form.get("category", "").strip(),
        qualification=request.form.get("qualification", "").strip() or None,
        office_address=request.form.get("office_address", "").strip() or None,
        email=request.form.get("email", "").strip() or None,
        phone=request.form.get("phone", "").strip() or None,
        bio=request.form.get("bio", "").strip() or None,
        responsibilities=request.form.get("responsibilities", "").strip(),
        photo_url="/static/images/avatar_placeholder.svg"
    )
    db.add(new_member)
    db.commit()
    flash(f"Official '{new_member.name}' added successfully.", "success")
    return redirect(url_for("admin_leadership"))

@app.route("/admin/camps")
@login_required
def admin_camps():
    """Manage Camps, Lok Adalats, and Schedules with PLV duty assignment."""
    db = get_db()
    events = db.query(LokAdalatEvent).order_by(LokAdalatEvent.event_date.asc()).all()
    plvs = db.query(PLV).filter(PLV.is_active == True).all()
    plvs.sort(key=lambda x: int(x.dlsa_sr_no) if x.dlsa_sr_no and x.dlsa_sr_no.isdigit() else 999)
    deployments = db.query(Deployment).filter(Deployment.is_active == True).order_by(Deployment.place_name.asc()).all()
    
    today = date.today()
    upcoming_events = [e for e in events if e.event_date >= today and e.is_active]
    past_events = [e for e in events if e.event_date < today or not e.is_active]
    
    return render_template(
        "admin/camps.html",
        events=events,
        upcoming_events=upcoming_events,
        past_events=past_events,
        plvs=plvs,
        deployments=deployments,
        today=today
    )

@app.route("/admin/camps/add", methods=["POST"])
@login_required
def admin_add_camp():
    """Schedule a new Legal Aid / Literacy Camp or Lok Adalat Event with PLV Duty Allocation."""
    db = get_db()
    title = request.form.get("title", "").strip()
    event_type = request.form.get("event_type", "").strip()
    custom_type = request.form.get("custom_event_type", "").strip()
    if event_type == "Other" and custom_type:
        event_type = custom_type
    elif not event_type:
        event_type = "Legal Literacy Camp"

    date_str = request.form.get("event_date", "").strip()
    try:
        event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        event_date = date.today()

    time_schedule = request.form.get("time_schedule", "10:00 AM to 04:00 PM").strip()
    venue = request.form.get("venue", "").strip()
    eligible_matters = request.form.get("eligible_matters", "").strip()
    presiding_officers = request.form.get("presiding_officers", "").strip()
    contact_person = request.form.get("contact_person", "").strip() or "Secretary, DLSA Porbandar (Ph: 0286-2244244)"
    benches_count = int(request.form.get("benches_count", "2") or 2)

    # Process PLV Duty Assignments
    selected_plvs = request.form.getlist("assigned_plvs")
    manual_plvs = request.form.get("assigned_plvs_manual", "").strip()
    
    combined_plvs = []
    if selected_plvs:
        combined_plvs.extend(selected_plvs)
    if manual_plvs:
        combined_plvs.append(manual_plvs)
    
    assigned_plvs_str = ", ".join(combined_plvs) if combined_plvs else None

    new_event = LokAdalatEvent(
        title=title,
        event_type=event_type,
        event_date=event_date,
        time_schedule=time_schedule,
        venue=venue,
        benches_count=benches_count,
        presiding_officers=presiding_officers,
        eligible_matters=eligible_matters,
        contact_person=contact_person,
        assigned_plvs=assigned_plvs_str,
        is_active=True
    )
    db.add(new_event)
    db.commit()

    flash(f"Camp / Event '{title}' scheduled successfully for {event_date.strftime('%d %b %Y')}.", "success")
    return redirect(url_for("admin_camps"))

@app.route("/admin/camps/<int:event_id>/update", methods=["POST"])
@login_required
def admin_update_camp(event_id):
    """Update details and assigned PLV duties for an existing camp or event."""
    db = get_db()
    event = db.query(LokAdalatEvent).filter(LokAdalatEvent.id == event_id).first()
    if not event:
        flash("Camp or Event record not found.", "danger")
        return redirect(url_for("admin_camps"))

    event.title = request.form.get("title", event.title).strip()
    event_type = request.form.get("event_type", event.event_type).strip()
    custom_type = request.form.get("custom_event_type", "").strip()
    if event_type == "Other" and custom_type:
        event_type = custom_type
    event.event_type = event_type

    date_str = request.form.get("event_date", "").strip()
    if date_str:
        try:
            event.event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            pass

    event.time_schedule = request.form.get("time_schedule", event.time_schedule).strip()
    event.venue = request.form.get("venue", event.venue).strip()
    event.eligible_matters = request.form.get("eligible_matters", event.eligible_matters).strip()
    event.presiding_officers = request.form.get("presiding_officers", event.presiding_officers).strip()
    event.contact_person = request.form.get("contact_person", event.contact_person).strip()
    event.benches_count = int(request.form.get("benches_count", str(event.benches_count)) or 1)
    
    # Process updated PLV assignments
    selected_plvs = request.form.getlist("assigned_plvs")
    manual_plvs = request.form.get("assigned_plvs_manual", "").strip()
    
    combined_plvs = []
    if selected_plvs:
        combined_plvs.extend(selected_plvs)
    if manual_plvs:
        combined_plvs.append(manual_plvs)
        
    if combined_plvs:
        event.assigned_plvs = ", ".join(combined_plvs)
    elif request.form.get("assigned_plvs_text"):
        event.assigned_plvs = request.form.get("assigned_plvs_text", "").strip()
    
    db.commit()
    flash(f"Camp / Event '{event.title}' updated successfully.", "success")
    return redirect(url_for("admin_camps"))

@app.route("/admin/camps/<int:event_id>/toggle-status", methods=["POST"])
@login_required
def admin_toggle_camp_status(event_id):
    """Toggle camp status between Active (Upcoming) and Completed/Archived."""
    db = get_db()
    event = db.query(LokAdalatEvent).filter(LokAdalatEvent.id == event_id).first()
    if not event:
        flash("Camp / Event not found.", "danger")
        return redirect(url_for("admin_camps"))

    event.is_active = not event.is_active
    db.commit()
    status_label = "Active / Scheduled" if event.is_active else "Completed / Archived"
    flash(f"Status of '{event.title}' changed to {status_label}.", "success")
    return redirect(url_for("admin_camps"))

@app.route("/admin/camps/<int:event_id>/delete", methods=["POST"])
@login_required
def admin_delete_camp(event_id):
    """Delete a scheduled camp or event."""
    db = get_db()
    event = db.query(LokAdalatEvent).filter(LokAdalatEvent.id == event_id).first()
    if not event:
        flash("Camp / Event not found.", "danger")
        return redirect(url_for("admin_camps"))

    name = event.title
    db.delete(event)
    db.commit()
    flash(f"Camp / Event '{name}' has been deleted.", "info")
    return redirect(url_for("admin_camps"))

# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@app.route("/api/stats")
def api_stats():
    """Returns DLSA statistics."""
    db = get_db()
    return jsonify({
        "total_plvs": db.query(PLV).filter(PLV.is_active == True).count(),
        "active_plvs": db.query(PLV).filter(PLV.status.in_(["Active", "On-Duty"])).count(),
        "total_deployments": db.query(Deployment).filter(Deployment.is_active == True).count(),
        "total_schemes": db.query(Scheme).filter(Scheme.is_active == True).count(),
        "total_applications": db.query(LegalAidApplication).count(),
        "database_engine": ACTIVE_DB_TYPE
    })

@app.route("/api/plvs")
def api_plvs():
    """Returns list of PLVs."""
    db = get_db()
    plvs = db.query(PLV).filter(PLV.is_active == True).all()
    return jsonify([p.to_dict() for p in plvs])

@app.route("/api/deployments")
def api_deployments():
    """Returns list of deployment locations."""
    db = get_db()
    deployments_list = db.query(Deployment).filter(Deployment.is_active == True).all()
    return jsonify([d.to_dict() for d in deployments_list])

@app.route("/api/schemes")
def api_schemes():
    """Returns list of schemes."""
    db = get_db()
    schemes_list = db.query(Scheme).filter(Scheme.is_active == True).all()
    return jsonify([s.to_dict() for s in schemes_list])

@app.route("/api/events")
def api_events():
    """Returns list of camps and events."""
    db = get_db()
    events = db.query(LokAdalatEvent).filter(LokAdalatEvent.is_active == True).order_by(LokAdalatEvent.event_date.asc()).all()
    return jsonify([e.to_dict() for e in events])

@app.route("/report")
def view_project_report():
    """Serves the printable/downloadable Project Report directly in the browser."""
    return send_file(os.path.join(app.root_path, "PROJECT_REPORT.html"))

@app.route("/report/pdf")
@app.route("/download-report")
def download_project_report_pdf():
    """Serves the generated PDF version of the Project Report."""
    pdf_path = os.path.join(app.root_path, "PROJECT_REPORT.pdf")
    if os.path.exists(pdf_path):
        return send_file(
            pdf_path, 
            mimetype="application/pdf", 
            as_attachment=False, 
            download_name="DLSA_Porbandar_Project_Report_Himanshu_Parmar.pdf"
        )
    return redirect(url_for("view_project_report"))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=True)
