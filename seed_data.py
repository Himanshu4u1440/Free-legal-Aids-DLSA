import logging
from datetime import date, datetime, timedelta, timezone
from werkzeug.security import generate_password_hash
from database import SessionLocal, Base, engine
from models import (
    Member, Deployment, PLV, PLVAssignment, Scheme, 
    LegalAidApplication, LokAdalatEvent, AdminUser
)

logger = logging.getLogger("dlsa.seeder")

def seed_database(force_reseed=False):
    """Initializes tables and seeds official DLSA Porbandar (Gujarat) data."""
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if not force_reseed and db.query(PLV).count() >= 40:
            logger.info("Database already seeded with Porbandar PLVs.")
            ev1 = db.query(LokAdalatEvent).filter(LokAdalatEvent.id == 1).first()
            if ev1 and not ev1.assigned_plvs:
                ev1.assigned_plvs = "PLV Nimisha Joshi (Sr. No. 01), PLV Parth Rathod (Sr. No. 03), PLV Nidhi Mashru (Sr. No. 04)"
            ev2 = db.query(LokAdalatEvent).filter(LokAdalatEvent.id == 2).first()
            if ev2 and not ev2.assigned_plvs:
                ev2.assigned_plvs = "PLV Hetvi Dave (Sr. No. 05), PLV Anjali Vaghela (Sr. No. 06)"
            ev3 = db.query(LokAdalatEvent).filter(LokAdalatEvent.id == 3).first()
            if ev3 and not ev3.assigned_plvs:
                ev3.assigned_plvs = "PLV Nimisha Joshi (Sr. No. 01), PLV Himanshu Parmar (Sr. No. 32)"
            db.commit()
            return

        # Clear existing data if reseeding to ensure ONLY Porbandar PLVs exist
        db.query(PLVAssignment).delete()
        db.query(LegalAidApplication).delete()
        db.query(PLV).delete()
        db.query(Deployment).delete()
        db.query(Member).delete()
        db.query(Scheme).delete()
        db.query(LokAdalatEvent).delete()
        db.query(AdminUser).delete()
        db.commit()

        logger.info("Seeding DLSA Porbandar (Gujarat) official data with 44 certified PLVs...")

        # 1. Admin User
        admin_user = AdminUser(
            username="admin",
            password_hash=generate_password_hash("admin123"),
            full_name="Registrar / Administrative Officer",
            designation="Administrative Superintendent, DLSA Porbandar",
            role="SuperAdmin",
            is_active=True
        )
        db.add(admin_user)

        # 2. DLSA Porbandar Leadership & Ranks Directory
        members = [
            Member(
                name="Hon'ble Mr. M. A. Bhatti (Mustaq Ahmed Bhatti)",
                designation="Principal District & Sessions Judge & Ex-Officio Chairman, DLSA Porbandar",
                rank_order=1,
                category="Judicial Head",
                qualification="B.A., LL.M., Gujarat Judicial Service (Higher Judicial Cadre)",
                office_address="Principal District & Sessions Court, Sandipani Road, Opp. Seva Sadan - 2, Porbandar, Gujarat - 360577",
                email="dlsaporbandardc@gmail.com",
                phone="0286-2222024 / 0286-2244244",
                bio="Principal District & Sessions Judge of Porbandar, serving as the Apex Judicial Authority and Ex-Officio Chairman of the District Legal Services Authority (DLSA), Porbandar. Heading judicial administration across Porbandar District, Ranavav, and Kutiyana talukas. Presiding over the District Legal Services Authority, Under Trial Review Committee (UTRC), Special and National Lok Adalats, and determining statutory victim compensation under NALSA & GSLSA guidelines.",
                responsibilities="Apex superintendence of DLSA Porbandar and Taluka Legal Services Committees (Ranavav & Kutiyana); constituting Lok Adalat benches; certifying and authorizing the 44-member Para Legal Volunteer (PLV) cadre; sanctioning victim compensation grants; reviewing undertrial long-detention cases under Section 436A CrPC; and ensuring that no indigent citizen remains unrepresented before any judicial forum.",
                photo_url="/static/images/chairman.svg",
                is_active=True
            ),
            Member(
                name="Full-Time Secretary, DLSA Porbandar (Senior Civil Judge)",
                designation="Full-Time Secretary, DLSA Porbandar & Senior Civil Judge",
                rank_order=2,
                category="Chief Executive",
                qualification="LL.M., Gujarat Judicial Service",
                office_address="DLSA Administrative Office, District Court Complex, Sandipani Road, Opp. Seva Sadan - 2, Porbandar, Gujarat - 360577",
                email="dlsaporbandardc@gmail.com",
                phone="0286-2222024 / 0286-2222026",
                bio="Judicial Officer of the Senior Civil Judge cadre appointed by the High Court of Gujarat as the Full-Time Secretary of DLSA Porbandar. Functioning as the Chief Executive managing whole-time legal aid operations, direct mobilization and tasking of the 44 Para Legal Volunteers, organizing dispute conciliation in Lok Adalats, and supervising legal defense counsel systems.",
                responsibilities="Day-to-day administration of DLSA Porbandar; immediate allocation of active PLVs to incoming citizen requests; scrutinizing indigent legal aid applications; assigning Legal Aid Defense Counsels (LADC) and panel advocates; conducting periodic inspections of police lockups and Special Sub-Jail Porbandar legal clinics; running the Front Office Helpdesk; and organizing legal literacy awareness camps in coastal and rural talukas.",
                photo_url="/static/images/secretary.svg",
                is_active=True
            ),
            Member(
                name="Chief Legal Aid Defense Counsel (Chief LADC)",
                designation="Chief Legal Aid Defense Counsel, Porbandar",
                rank_order=3,
                category="Defense Head",
                qualification="B.A. LL.B. (Special), 20+ Years Criminal Defense Practice",
                office_address="LADCS Office, District Court Complex, Sandipani Road, Porbandar",
                email="chief.ladc.porbandar@gmail.com",
                phone="0286-2244250",
                bio="Leading the specialized Legal Aid Defense Counsel System (LADCS) in Porbandar for criminal defense of marginalized, indigent undertrials and vulnerable accused individuals.",
                responsibilities="Representing indigent accused from remand stage through Sessions trials, bail applications, appeals, and coordinating jail visits for undertrials.",
                photo_url="/static/images/chief_ladc.svg",
                is_active=True
            ),
            Member(
                name="Deputy Chief Legal Aid Defense Counsel",
                designation="Deputy Chief Legal Aid Defense Counsel, Porbandar",
                rank_order=4,
                category="Defense Counsel",
                qualification="LL.B., 12 Years Criminal Law Practice",
                office_address="LADCS Office, District Court Complex, Sandipani Road, Porbandar",
                email="deputy.ladc.porbandar@gmail.com",
                phone="0286-2244251",
                bio="Dedicated defense practitioner assisting in criminal defense before Additional Sessions Courts, Magistrate courts, and juvenile matters.",
                responsibilities="Trial defense, remand representations before Chief Judicial Magistrate (CJM) Porbandar, victim compensation filings.",
                photo_url="/static/images/deputy_ladc.svg",
                is_active=True
            ),
            Member(
                name="Convener, Front Office Legal Services Clinic",
                designation="Senior Panel Advocate & Front Office Convener",
                rank_order=5,
                category="Front Office Convener",
                qualification="B.Com., LL.B., 18 Years Civil & Revenue Practice",
                office_address="DLSA Front Office Helpdesk, District Court Complex, Sandipani Road, Porbandar",
                email="dlsaporbandardc@gmail.com",
                phone="0286-2222024",
                bio="Supervising public walk-ins, free legal advice, dispute pre-litigation drafting, and mediation intake at the Porbandar District Court front office.",
                responsibilities="Providing free consultations to visiting common citizens, screening eligibility under Section 12 of LSA Act, drafting petitions for poor litigants, and coordinating PLV helpdesk duties.",
                photo_url="/static/images/panel_convener.svg",
                is_active=True
            )
        ]
        db.add_all(members)
        db.commit()

        # 3. 31 Official Deployment Places in Porbandar District (Orders 178/2026 & 179/2026)
        deployments = [
            # --- 9 POLICE STATIONS (Order No. 179/2026) ---
            Deployment(
                id=1,
                place_name="Kirtimandir Police Station",
                place_type="Police Station",
                address="Near Chowpatty / SV Road, Porbandar Urban",
                area_locality="Porbandar City",
                police_jurisdiction="Kirtimandir Police Station",
                incharge_officer="Police Inspector & DLSA Secretary",
                contact_phone="0286-2242100",
                operating_hours="24 Hours (3 Shifts: 06:00-14:00, 14:00-22:00, 22:00-06:00)",
                services_offered="Assistance for missing children, protection and counseling for child offenses under POCSO Act, 24-hour legal counsel for detainees under D.K. Basu guidelines.",
                facilities_available="Child-friendly interaction corner, missing children helpdesk, telephone facility to inform relatives.",
                is_active=True
            ),
            Deployment(
                id=2,
                place_name="Kamlabaug Police Station",
                place_type="Police Station",
                address="Station Road, Kamlabaug Area, Porbandar",
                area_locality="Kamlabaug, Porbandar",
                police_jurisdiction="Kamlabaug Police Station",
                incharge_officer="Police Inspector & DLSA Secretary",
                contact_phone="0286-2242200",
                operating_hours="10:00 AM - 06:00 PM (Daily)",
                services_offered="Assistance for missing children, child victim legal support, arrest intimation to families, free legal aid defense.",
                facilities_available="Helpdesk booth, legal literature racks, counseling area.",
                is_active=True
            ),
            Deployment(
                id=3,
                place_name="Mahila Police Station, Porbandar",
                place_type="Police Station",
                address="Jilla Seva Sadan - 1 Compound, Porbandar",
                area_locality="Chhaya / Porbandar",
                police_jurisdiction="Mahila Police Station",
                incharge_officer="Police Inspector & DLSA Secretary",
                contact_phone="0286-2245100",
                operating_hours="10:00 AM - 06:00 PM (Daily)",
                services_offered="Women victim support, missing children tracing, domestic violence legal counseling, compensation filing.",
                facilities_available="Women counseling room, child play corner, victim shelter liaison.",
                is_active=True
            ),
            Deployment(
                id=4,
                place_name="Udyognagar Police Station",
                place_type="Police Station",
                address="GIDC Industrial Estate, Udyognagar, Porbandar",
                area_locality="Udyognagar, Porbandar",
                police_jurisdiction="Udyognagar Police Station",
                incharge_officer="Police Inspector & DLSA Secretary",
                contact_phone="0286-2243300",
                operating_hours="10:00 AM - 06:00 PM (Daily)",
                services_offered="Industrial area missing children support, labor rights, juvenile assistance, free legal counsel.",
                facilities_available="Public guidance desk, legal display board.",
                is_active=True
            ),
            Deployment(
                id=5,
                place_name="Harbour Marine Police Station",
                place_type="Police Station",
                address="Subhash Nagar Coastal Road, Old Port, Porbandar",
                area_locality="Subhash Nagar, Porbandar",
                police_jurisdiction="Harbour Marine Police Station",
                incharge_officer="Police Inspector & DLSA Secretary",
                contact_phone="0286-2244100",
                operating_hours="10:00 AM - 06:00 PM (Daily)",
                services_offered="Coastal missing children assistance, maritime community child protection, fisherman rights, arrestee counsel.",
                facilities_available="Coastal assistance desk, legal leaflets.",
                is_active=True
            ),
            Deployment(
                id=6,
                place_name="Miyani Marine Police Station",
                place_type="Police Station",
                address="Miyani Coastal Outpost, Miyani, Porbandar District",
                area_locality="Miyani, Porbandar",
                police_jurisdiction="Miyani Marine Police Station",
                incharge_officer="Police Inspector & DLSA Secretary",
                contact_phone="0286-2281100",
                operating_hours="10:00 AM - 06:00 PM (Daily)",
                services_offered="Vigilance for missing children along coastal belt, juvenile protection, legal counseling for villagers.",
                facilities_available="Marine police guidance corner.",
                is_active=True
            ),
            Deployment(
                id=7,
                place_name="Bagvadar Police Station",
                place_type="Police Station",
                address="State Highway, Bagvadar, Porbandar District",
                area_locality="Bagvadar, Porbandar",
                police_jurisdiction="Bagvadar Police Station",
                incharge_officer="Police Sub-Inspector & DLSA Secretary",
                contact_phone="02801-241200",
                operating_hours="10:00 AM - 06:00 PM (Daily)",
                services_offered="Rural missing children tracking, agricultural laborer protection, juvenile offense prevention.",
                facilities_available="Rural desk, legal advice center.",
                is_active=True
            ),
            Deployment(
                id=8,
                place_name="Navibandar Police Station (TLSC)",
                place_type="Police Station",
                address="Coastal Highway, Navibandar, Porbandar District",
                area_locality="Navibandar, Porbandar",
                police_jurisdiction="Navibandar Police Station",
                incharge_officer="Police Sub-Inspector & DLSA Secretary",
                contact_phone="02804-251200",
                operating_hours="10:00 AM - 06:00 PM (Daily)",
                services_offered="Coastal rural missing children protection, fisherman family aid, free defense lawyer request filing.",
                facilities_available="Helpdesk counter, brochure rack.",
                is_active=True
            ),
            Deployment(
                id=9,
                place_name="Madhavpur Police Station (TLSC)",
                place_type="Police Station",
                address="Madhavpur Ghed Main Road, Madhavpur, Porbandar District",
                area_locality="Madhavpur Ghed, Porbandar",
                police_jurisdiction="Madhavpur Police Station",
                incharge_officer="Police Sub-Inspector & DLSA Secretary",
                contact_phone="02804-272200",
                operating_hours="10:00 AM - 06:00 PM (Daily)",
                services_offered="Pilgrim & child protection, missing children tracing, legal first-aid for arrestee families.",
                facilities_available="Public guidance counter, complaint assistance booth.",
                is_active=True
            ),

            # --- 9 INSTITUTIONAL & COURT CLINICS (Order No. 178/2026) ---
            Deployment(
                id=10,
                place_name="Jilla Panchayat Legal Aid Clinic",
                place_type="Court & Institutional Clinic",
                address="Jilla Panchayat Bhawan, Opp. Circuit House, Porbandar",
                area_locality="Porbandar Urban",
                police_jurisdiction="Kamlabaug Police Station",
                incharge_officer="District Development Officer & Secretary DLSA",
                contact_phone="0286-2244244",
                operating_hours="10:30 AM - 06:10 PM (Mon, Wed, Fri)",
                services_offered="Panchayat grievance conciliation, rural welfare schemes, senior citizen maintenance, widow pension documentation.",
                facilities_available="Consultation chamber, welfare forms desk.",
                is_active=True
            ),
            Deployment(
                id=11,
                place_name="Front Office DLSA Porbandar Legal Aid Clinic",
                place_type="Court & Institutional Clinic",
                address="Ground Floor, District Court Complex, Rajmahal Road, Porbandar",
                area_locality="Porbandar City",
                police_jurisdiction="Kirtimandir Police Station",
                incharge_officer="Secretary, DLSA Porbandar & Panel Lawyers",
                contact_phone="0286-2222024",
                operating_hours="10:30 AM - 06:10 PM (Daily)",
                services_offered="Walk-in legal counseling, Section 12 free legal aid applications, panel advocate assignment, Lok Adalat pre-litigation filing.",
                facilities_available="Computerized tracking kiosk, legal literature rack, barrier-free access ramp, waiting hall.",
                is_active=True
            ),
            Deployment(
                id=12,
                place_name="Family Court Help Desk & Legal Aid Clinic, Porbandar",
                place_type="Court & Institutional Clinic",
                address="Family Court Building, District Court Complex, Porbandar",
                area_locality="Porbandar City",
                police_jurisdiction="Kirtimandir Police Station",
                incharge_officer="Principal Judge, Family Court & DLSA Secretary",
                contact_phone="0286-2244245",
                operating_hours="10:30 AM - 06:10 PM (Daily)",
                services_offered="Matrimonial dispute pre-litigation settlement under GSLSA SOP, maintenance claim advice, child custody conciliation.",
                facilities_available="Confidential counseling chamber, children play corner.",
                is_active=True
            ),
            Deployment(
                id=13,
                place_name="Juvenile Justice Board (JJB) Legal Aid Clinic",
                place_type="Court & Institutional Clinic",
                address="Observation Home / JJB Court Complex, Chhaya Road, Porbandar",
                area_locality="Chhaya, Porbandar",
                police_jurisdiction="Kamlabaug Police Station",
                incharge_officer="Principal Magistrate, JJB & DLSA Secretary",
                contact_phone="0286-2221234",
                operating_hours="10:30 AM - 06:10 PM (Every Thursday)",
                services_offered="Representation for children in conflict with law, child welfare committee coordination, guardian counseling.",
                facilities_available="Child-friendly inquiry room, counselor chamber.",
                is_active=True
            ),
            Deployment(
                id=14,
                place_name="D.D. Kotiyawala Law College Legal Aid Clinic",
                place_type="Court & Institutional Clinic",
                address="D.D. Kotiyawala Municipal Law College, SV Road, Porbandar",
                area_locality="Porbandar City",
                police_jurisdiction="Kirtimandir Police Station",
                incharge_officer="Principal, Law College & DLSA Secretary",
                contact_phone="0286-2242850",
                operating_hours="09:00 AM - 01:30 PM & 03:30 PM - 05:30 PM (Mon, Wed, Fri)",
                services_offered="Student community legal awareness drives, public legal clinic, pro-bono law student assistance, village outreach.",
                facilities_available="Law college moot court room, legal clinic cabin.",
                is_active=True
            ),
            Deployment(
                id=15,
                place_name="Special Sub-Jail Clinic & Visitors Area Helpdesk",
                place_type="Court & Institutional Clinic",
                address="Jail Road, Near Old Custom House, Porbandar",
                area_locality="Porbandar City",
                police_jurisdiction="Kamlabaug Police Station",
                incharge_officer="Jail Superintendent & DLSA Visiting Advocate",
                contact_phone="0286-2242350",
                operating_hours="Visitors Area: 10:00-12:00 & 15:00-16:00 | Jail Clinic: 16:00-18:00 (Mon to Sat)",
                services_offered="Legal aid for undertrial inmates, bail drafting for indigent prisoners, UTRC review collation, visitor family assistance.",
                facilities_available="Confidential legal consultation booth, visitor area guidance counter.",
                is_active=True
            ),
            Deployment(
                id=16,
                place_name="Sakhi One Stop Centre Legal Aid Clinic, Porbandar",
                place_type="Court & Institutional Clinic",
                address="Jilla Seva Sadan - 2 Compound, Opp. District Court, Sandipani Road, Porbandar",
                area_locality="Chhaya / Porbandar",
                police_jurisdiction="Mahila Police Station, Porbandar",
                incharge_officer="Centre Administrator & DLSA Secretary",
                contact_phone="0286-2245181",
                operating_hours="10:30 AM - 06:10 PM (Mon, Wed, Fri)",
                services_offered="Protection of women from domestic violence, emergency shelter facilitation, legal aid lawyer appointment, psycho-social aid.",
                facilities_available="Counseling cabin, temporary shelter rooms, police desk.",
                is_active=True
            ),
            Deployment(
                id=17,
                place_name="Mahanagarpalika / Nagarpalika Porbandar Legal Aid Clinic",
                place_type="Court & Institutional Clinic",
                address="Nagarpalika Bhavan, M.G. Road, Porbandar",
                area_locality="Porbandar City",
                police_jurisdiction="Kirtimandir Police Station",
                incharge_officer="Chief Officer, Nagarpalika & DLSA Secretary",
                contact_phone="0286-2242525",
                operating_hours="10:30 AM - 06:10 PM (Mon, Wed, Fri)",
                services_offered="Civic dispute resolution, street vendor legal rights, urban slum dweller legal assistance, welfare claims.",
                facilities_available="Civic guidance desk, public grievance counter.",
                is_active=True
            ),
            Deployment(
                id=18,
                place_name="Jilla Sainik Board Legal Aid Clinic",
                place_type="Court & Institutional Clinic",
                address="Jilla Sainik Welfare Office, Jilla Seva Sadan, Porbandar",
                area_locality="Porbandar City",
                police_jurisdiction="Kamlabaug Police Station",
                incharge_officer="Jilla Sainik Welfare Officer & DLSA Secretary",
                contact_phone="0286-2244244",
                operating_hours="10:30 AM - 06:10 PM (Tue, Thu, Sat)",
                services_offered="Legal assistance for armed forces veterans, war widows, defense pensioner disputes, and family conciliation.",
                facilities_available="Sainik consultation desk.",
                is_active=True
            ),

            # --- 13 VILLAGE LEGAL AID CLINICS (Order No. 178/2026) ---
            Deployment(
                id=19,
                place_name="Miyani Village Legal Aid Clinic",
                place_type="Village Legal Aid Clinic",
                address="Gram Panchayat Office, Miyani, Porbandar District",
                area_locality="Miyani Village",
                police_jurisdiction="Miyani Marine Police Station",
                incharge_officer="Sarpanch / Talati & DLSA Secretary",
                contact_phone="0286-2281100",
                operating_hours="11:00 AM - 05:30 PM (Mon, Tue, Fri)",
                services_offered="Rural legal advice, land record mutation guidance, coastal dispute conciliation, Lok Adalat pre-litigation.",
                facilities_available="Panchayat legal desk, Gujarati legal booklets.",
                is_active=True
            ),
            Deployment(
                id=20,
                place_name="Visavada Village Legal Aid Clinic",
                place_type="Village Legal Aid Clinic",
                address="Gram Panchayat Bhavan, Visavada, Porbandar District",
                area_locality="Visavada Village",
                police_jurisdiction="Kamlabaug Police Station",
                incharge_officer="Sarpanch / Talati & DLSA Secretary",
                contact_phone="0286-2244244",
                operating_hours="11:00 AM - 05:30 PM (Tue, Fri)",
                services_offered="Farmer rights, rural civic dispute mediation, agricultural worker claims, free legal aid application.",
                facilities_available="Village mediation corner.",
                is_active=True
            ),
            Deployment(
                id=21,
                place_name="Shingda Village Legal Aid Clinic",
                place_type="Village Legal Aid Clinic",
                address="Gram Panchayat Bhavan, Shingda, Porbandar District",
                area_locality="Shingda Village",
                police_jurisdiction="Bagvadar Police Station",
                incharge_officer="Sarpanch / Talati & DLSA Secretary",
                contact_phone="02801-241200",
                operating_hours="11:00 AM - 05:30 PM (Mon, Wed, Fri)",
                services_offered="Village dispute conciliation, land mutation guidance, government scheme awareness, Lok Adalat registration.",
                facilities_available="Panchayat guidance desk.",
                is_active=True
            ),
            Deployment(
                id=22,
                place_name="Bagvadar Village Legal Aid Clinic",
                place_type="Village Legal Aid Clinic",
                address="Gram Panchayat Bhavan, Bagvadar, Porbandar District",
                area_locality="Bagvadar Village",
                police_jurisdiction="Bagvadar Police Station",
                incharge_officer="Sarpanch / Talati & DLSA Secretary",
                contact_phone="02801-241200",
                operating_hours="11:00 AM - 05:30 PM (Tue, Thu, Sat)",
                services_offered="Rural dispute mediation, legal literacy camps, widow and old age pension aid, revenue dispute counseling.",
                facilities_available="Consultation room, informational posters.",
                is_active=True
            ),
            Deployment(
                id=23,
                place_name="Advana Legal Aid Clinic & Legal Assistance Centre",
                place_type="Village Legal Aid Clinic",
                address="Panchayat Bhavan & Legal Assistance Centre, Advana, Porbandar District",
                area_locality="Advana Village",
                police_jurisdiction="Bagvadar Police Station",
                incharge_officer="Sarpanch / Talati & DLSA Secretary",
                contact_phone="02801-242200",
                operating_hours="11:00 AM - 05:30 PM (Mon, Wed, Fri)",
                services_offered="Advana regional legal assistance center, agrarian disputes conciliation, labor rights counseling, pre-litigation filing.",
                facilities_available="Dedicated legal aid assistance room, brochure rack.",
                is_active=True
            ),
            Deployment(
                id=24,
                place_name="Godhana Village Legal Aid Clinic",
                place_type="Village Legal Aid Clinic",
                address="Gram Panchayat Office, Godhana, Porbandar District",
                area_locality="Godhana Village",
                police_jurisdiction="Bagvadar Police Station",
                incharge_officer="Sarpanch / Talati & DLSA Secretary",
                contact_phone="02801-243200",
                operating_hours="11:00 AM - 05:30 PM (Tue, Fri)",
                services_offered="Rural legal guidance, agricultural labor support, family dispute counseling, government welfare claim filing.",
                facilities_available="Panchayat mediation desk.",
                is_active=True
            ),
            Deployment(
                id=25,
                place_name="Bakharla Village Legal Aid Clinic",
                place_type="Village Legal Aid Clinic",
                address="Gram Panchayat Bhavan, Bakharla, Porbandar District",
                area_locality="Bakharla Village",
                police_jurisdiction="Bagvadar Police Station",
                incharge_officer="Sarpanch / Talati & DLSA Secretary",
                contact_phone="02801-244200",
                operating_hours="11:00 AM - 05:30 PM (Mon, Wed, Fri)",
                services_offered="Village community mediation, farm laborer wage dispute guidance, women and child welfare assistance.",
                facilities_available="Panchayat consultation cabin.",
                is_active=True
            ),
            Deployment(
                id=26,
                place_name="Degam Village Legal Aid Clinic",
                place_type="Village Legal Aid Clinic",
                address="Gram Panchayat Office, Degam, Porbandar District",
                area_locality="Degam Village",
                police_jurisdiction="Bagvadar Police Station",
                incharge_officer="Sarpanch / Talati & DLSA Secretary",
                contact_phone="02801-245200",
                operating_hours="11:00 AM - 05:30 PM (Tue, Thu, Sat)",
                services_offered="Rural dispute conciliation, senior citizen maintenance support, Lok Adalat awareness.",
                facilities_available="Panchayat legal corner.",
                is_active=True
            ),
            Deployment(
                id=27,
                place_name="Kuchhadi Village Legal Aid Clinic",
                place_type="Village Legal Aid Clinic",
                address="Gram Panchayat Bhavan, Kuchhadi, Porbandar District",
                area_locality="Kuchhadi Village",
                police_jurisdiction="Kamlabaug Police Station",
                incharge_officer="Sarpanch / Talati & DLSA Secretary",
                contact_phone="0286-2244244",
                operating_hours="11:00 AM - 05:30 PM (Mon, Wed, Fri)",
                services_offered="Local dispute conciliation, unorganised sector worker guidance, women rights counseling, free lawyer application.",
                facilities_available="Panchayat guidance table.",
                is_active=True
            ),
            Deployment(
                id=28,
                place_name="Tukda Gosa Village Legal Aid Clinic",
                place_type="Village Legal Aid Clinic",
                address="Gram Panchayat Bhavan, Tukda Gosa, Porbandar District",
                area_locality="Tukda Gosa Village",
                police_jurisdiction="Navibandar Police Station",
                incharge_officer="Sarpanch / Talati & DLSA Secretary",
                contact_phone="02804-252200",
                operating_hours="11:00 AM - 05:30 PM (Tue, Thu, Sat)",
                services_offered="Rural matrimonial and family dispute counseling, agricultural worker welfare claims, Lok Adalat intake.",
                facilities_available="Panchayat counseling room.",
                is_active=True
            ),
            Deployment(
                id=29,
                place_name="Garej Village Legal Aid Clinic",
                place_type="Village Legal Aid Clinic",
                address="Gram Panchayat Bhavan, Garej, Porbandar District",
                area_locality="Garej Village",
                police_jurisdiction="Navibandar Police Station",
                incharge_officer="Sarpanch / Talati & DLSA Secretary",
                contact_phone="02804-253200",
                operating_hours="11:00 AM - 05:30 PM (Mon, Tue, Fri)",
                services_offered="Rural legal aid clinic, land dispute conciliation, rural social welfare documentation.",
                facilities_available="Panchayat guidance desk.",
                is_active=True
            ),
            Deployment(
                id=30,
                place_name="Ratiya Village Legal Aid Clinic",
                place_type="Village Legal Aid Clinic",
                address="Gram Panchayat Bhavan, Ratiya, Porbandar District",
                area_locality="Ratiya Village",
                police_jurisdiction="Navibandar Police Station",
                incharge_officer="Sarpanch / Talati & DLSA Secretary",
                contact_phone="02804-254200",
                operating_hours="11:00 AM - 05:30 PM (Tue, Fri)",
                services_offered="Agrarian dispute conciliation, farmer legal assistance, rural widow pension paperwork.",
                facilities_available="Village mediation desk.",
                is_active=True
            ),
            Deployment(
                id=31,
                place_name="Madhavpur Village Legal Aid Clinic",
                place_type="Village Legal Aid Clinic",
                address="Gram Panchayat Office, Madhavpur Ghed, Porbandar District",
                area_locality="Madhavpur Ghed",
                police_jurisdiction="Madhavpur Police Station",
                incharge_officer="Sarpanch / Talati & DLSA Secretary",
                contact_phone="02804-272200",
                operating_hours="11:00 AM - 05:30 PM (Mon, Wed, Fri)",
                services_offered="Comprehensive village legal aid, pre-litigation settlement, farmer & coastal worker dispute counseling.",
                facilities_available="Community consultation center, legal awareness banner wall.",
                is_active=True
            )
        ]
        db.add_all(deployments)
        db.commit()

        # 4. ALL 44 OFFICIAL PARA LEGAL VOLUNTEERS (PLVs) FROM THE CADRE
        # Exact alignment with DLSA Porbandar Office Orders 178/2026 & 179/2026
        raw_plv_data = [
            ("01", "Nimisha A. Joshi", "Female", "B/h Saibaba Temple, Chhaya, Porbandar", "7405245440", "Chhaya Area Legal Assistance & Women Rights"),
            ("03", "Parth B. Rathod", "Male", "R.G.T. College Compound, Rajmahal, Porbandar", "9054980167", "Mahanagarpalika Civic Legal Aid Clinic"),
            ("04", "Nidhi D. Mashru", "Female", "Nr. Bus Stand Road, Jam Raval", "6353564053", "Miyani Village Legal Aid Clinic"),
            ("05", "Tejal L. Gami", "Female", "Jam Raval", "6353760068", "Jam Raval Rural Dispute Facilitation"),
            ("06", "Anjali N. Vaghela", "Female", "Shreeji Duplex, Opp. Madvani College, B/h. S.B.I. Bank, Porbandar", "9510521920", "Law College Legal Clinic & DLSA Front Office"),
            ("07", "Hetvi B. Dave", "Female", "Satyanarayan Mandir, Opp. Bhaveswar Mandir, Porbandar", "9327206531", "Hospital Trauma & Senior Citizens Welfare"),
            ("08", "Meera J. Unadkat", "Female", "Vadi Plot-5, \"Nathkrupa\", Porbandar-360575", "9662856766", "Bagvadar Village Legal Aid Clinic"),
            ("09", "Vibhuti D. Pandavadadra", "Female", "New Vankarvas, Chhaya, Porbandar", "7096191878", "Kuchhadi Village Legal Aid Clinic"),
            ("10", "Vikrantsinh N. Zala", "Male", "249, Sarkari Karmachari Soci., Khapat, Porbandar", "7016209914", "Police Station Child Protection & Legal Helpdesk (Night Shift)"),
            ("11", "Anjali B. Rathod", "Female", "Bagvadar, Porbandar", "9879566710", "Rural Police Station Missing Children & Legal Aid"),
            ("12", "Rajesh M. Mandera", "Male", "Navibandar, Porbandar", "9974238551", "Navibandar Police Station Child Protection"),
            ("14", "Nirav B. Pankhaniya", "Male", "Shingda, Porbandar", "8140429721", "Shingda Village Legal Aid Clinic"),
            ("16", "Manjula S. Chanpa", "Female", "Kadiya Plot, Street No.1, Porbandar", "7069074328", "Tukda Gosa Village Legal Aid Clinic"),
            ("18", "Manish M. Modhvadiya", "Male", "Advana, Porbandar", "9016831016", "Advana Village Legal Aid Clinic & Legal Assistance Centre"),
            ("19", "Kajal B. Khunti", "Female", "Porbandar City", "6301965197", "DLSA Front Office Legal Aid Desk Facilitator"),
            ("21", "Rambhai H. Pandavadra", "Male", "Godhana, Porbandar", "8238086334", "Godhana Village Legal Aid Clinic"),
            ("22", "Dhara B. Vaja", "Female", "Bakharla, Porbandar", "9574778213", "Bakharla Village Legal Aid Clinic"),
            ("24", "Ankita Parmar", "Female", "Madhavpur, Porbandar", "7433025266", "Madhavpur Police Station Child Protection"),
            ("25", "Alpana H. Poriya", "Female", "Near Kedareshwar Temple, Porbandar", "7016440739", "Sakhi Women Protection & Legal Aid"),
            ("27", "Bhumi Parmar", "Female", "Visavada, Porbandar", "7622865312", "Visavada Village Legal Aid Clinic"),
            ("28", "Ravi Mokariya", "Male", "Ratiya, Porbandar", "9327532841", "Ratiya Village Legal Aid Clinic"),
            ("29", "Hasti V. Pandya", "Female", "Porbandar City", "8980937526", "Family Court Helpdesk & Matrimonial Conciliation"),
            ("30", "Muskan V. Cholera", "Female", "\"Gatral Nivas\", Near Vinod Sweet Mart, Porbandar", "8511625554", "Juvenile Justice Board Child Rights PLV"),
            ("31", "Hiren Mokariya", "Male", "Madhavpur, Porbandar", "9574135513", "Madhavpur Village Legal Aid Clinic"),
            ("33", "Mahek Rafish Sheta", "Female", "Porbandar City", "9909341719", "Police Station Child Protection & Legal Helpdesk (Afternoon Shift)"),
            ("34", "Dhaval K. Bamaniya", "Male", "Porbandar City", "6265487237", "Police Station Child Protection & Legal Helpdesk (Morning Shift)"),
            ("35", "Chandrika R. Chanchiya", "Female", "Porbandar City", "7043388750", "Jilla Panchayat Legal Aid Clinic PLV"),
            ("37", "Madhvi K. Shingrakhiya", "Female", "Porbandar City", "9924535601", "Police Station Missing Children & Legal Aid PLV"),
            ("38", "Aarti B. Savaniya", "Female", "Garej, Porbandar", "9537221053", "Garej Village Legal Aid Clinic"),
            ("41", "Hina V. Toraniya", "Female", "Jamat Khana, Chhaya, Porbandar", "9687036597", "Minority Welfare, Women Rights & Chhaya Desk"),
            ("43", "Bharti D. Sida", "Female", "A.C.C. Road, Nr. Maruti Pan, Chhaya, Porbandar", "7069865510", "Industrial & A.C.C. Workers Legal Aid Desk"),
            ("44", "Himanshu V. Parmar", "Male", "Sandipani Road, Wireless Drasti Katlari House, Porbandar", "8980714911", "Sub-Jail Clinic & Visitors Area Helpdesk PLV"),
            ("48", "Hemang R. Solanki", "Male", "Vasant Nagar, Bhanvad, Devbhoomi-Dwarka", "8320032415", "TLSC Ranavav Inter-District Liaison"),
            ("49", "Aman A. Sadiya", "Male", "Ambedkar Nagar, Narsang Tekri, Porbandar", "8511730746", "City B Police Station Youth Guidance Desk"),
            ("50", "Payal R. Vaja", "Female", "Near Kori samaj Vandi, Bokhira, Porbandar", "6351866648", "Bokhira Legal Aid Clinic In-charge & Mediation"),
            ("51", "Sanjana A. Baleja", "Female", "Tumbada, Bokhira, Porbandar", "7778015829", "Bokhira Coastal & Rural Women Welfare"),
            ("52", "Kamlesh R. Parmar", "Male", "Hanuman Dhar, Raval, Devbhoomi-Dwarka", "7228828519", "TLSC Ranavav Rural Legal Literacy Desk"),
            ("53", "Shruti D. Vaghela", "Female", "Tumbda, New Bhoivado, Bokhira, Porbandar", "8238835080", "Bokhira Coastal Fishermen Legal Entitlements"),
            ("54", "Mahek B. Kothari", "Female", "Porbandar City", "7041111127", "Women & Child Victim Protection PLV"),
            ("55", "Chetna G. Parmar", "Female", "Opp. Mahakali Temple, Indiranagar, Porbandar", "9712857973", "Police Station Missing Children & Legal Helpdesk PLV"),
            ("57", "Jivan K. Chauhan", "Male", "Kadiya Plot, Street No. 1, Porbandar", "7069521451", "Harbour Marine Legal Assistance & Child Protection PLV"),
            ("58", "Vrutika N. Kanabar", "Female", "Ram Guest House, Galaxy Apar., Block No. 401, Porbandar", "7779083938", "Hospital Trauma Desk Patient Legal Rights"),
            ("59", "Rekha D. Dafda", "Female", "Kadiya Plot, Street No.2, Porbandar", "7069074329", "Degam Village Legal Aid Clinic PLV"),
            ("60", "Laxmi D. Gosai", "Female", "Khapat, Porbandar", "6352544062", "Marine Police Child Protection & Legal Helpdesk PLV"),
        ]

        created_plvs = []
        for sr_no, name, gender, address, phone, spec in raw_plv_data:
            reg_no = f"DLSA/PBD/PLV/{sr_no}"
            photo = f"/static/images/plv_pbd_{sr_no}.svg"
            
            p = PLV(
                registration_no=reg_no,
                dlsa_sr_no=sr_no,
                full_name=name,
                gender=gender,
                qualification="Certified Para Legal Volunteer",
                primary_occupation="Social Worker / Community Volunteer",
                languages_known="Gujarati, Hindi, English",
                phone=phone,
                email=f"plv.{sr_no}.porbandar@dlsa.gujarat.gov.in",
                residential_address=address,
                police_verification_status="Verified by Porbandar Police",
                training_batch="Batch 2026 (DLSA Porbandar & GSLSA Certified)",
                card_issued_date="20-07-2026",
                validity_date="07-03-2027",
                date_of_enrollment=date(2026, 7, 20),
                status="Active",
                specialization_area=spec,
                photo_url=photo,
                achievements_notes=f"Authorized Para Legal Volunteer (Sr. No. {sr_no}) issued by Chairman, DLSA Porbandar on 20-07-2026. Serving {address.split(',')[-2].strip() if ',' in address else 'Porbandar'} area.",
                is_active=True
            )
            db.add(p)
            created_plvs.append((p, spec))

        db.commit()

        # 5. Official Assignments linking PLVs to Porbandar Deployment Locations
        # (Orders No. 178/2026 & 179/2026 signed by Full Time Secretary, DLSA Porbandar)
        plv_dict = {p.dlsa_sr_no: p for p, _ in created_plvs}
        dep_dict = {d.id: d for d in deployments}

        official_assignments = [
            # Location 1: Kirtimandir PS (3 shifts)
            ("34", 1, "Police Station Child Protection & Legal Helpdesk (Morning Shift)", "Daily", "06:00 AM - 02:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),
            ("33", 1, "Police Station Child Protection & Legal Helpdesk (Afternoon Shift)", "Daily", "02:00 PM - 10:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),
            ("10", 1, "Police Station Child Protection & Legal Helpdesk (Night Shift)", "Daily", "10:00 PM - 06:00 AM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

            # Location 2: Kamlabaug PS
            ("37", 2, "Police Station Missing Children & Legal Aid PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

            # Location 3: Mahila PS
            ("54", 3, "Women & Child Victim Protection PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

            # Location 4: Udyognagar PS
            ("55", 4, "Police Station Missing Children & Legal Helpdesk PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

            # Location 5: Harbour Marine PS
            ("57", 5, "Harbour Marine Legal Assistance & Child Protection PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

            # Location 6: Miyani Marine PS
            ("60", 6, "Marine Police Child Protection & Legal Helpdesk PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

            # Location 7: Bagvadar PS
            ("11", 7, "Rural Police Station Missing Children & Legal Aid PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

            # Location 8: Navibandar PS
            ("12", 8, "Navibandar Police Station Child Protection PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

            # Location 9: Madhavpur PS
            ("24", 9, "Madhavpur Police Station Child Protection PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

            # Location 10: Jilla Panchayat Clinic
            ("35", 10, "Jilla Panchayat Legal Aid Clinic PLV", "Monday, Wednesday, Friday", "10:30 AM - 06:10 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 11: Front Office DLSA Porbandar
            ("19", 11, "DLSA Front Office Legal Aid Desk Facilitator", "Daily", "10:30 AM - 06:10 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 178/2026"),

            # Location 12: Family Court Help Desk
            ("29", 12, "Family Court Helpdesk & Matrimonial Conciliation PLV", "Daily", "10:30 AM - 06:10 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 178/2026"),

            # Location 13: Juvenile Justice Board (JJB)
            ("30", 13, "Juvenile Justice Board Child Rights PLV", "Every Thursday", "10:30 AM - 06:10 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 14: Law College Clinic
            ("06", 14, "Law College Legal Clinic & DLSA Front Office PLV", "Monday, Wednesday, Friday", "09:00 AM - 01:30 PM & 03:30 PM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 15: Special Sub-Jail Clinic & Visitors Area
            ("44", 15, "Sub-Jail Clinic & Visitors Area Helpdesk PLV", "Monday to Saturday", "10:00-12:00 & 15:00-16:00 (Visitors), 16:00-18:00 (Clinic)", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 178/2026"),

            # Location 16: Sakhi One Stop Centre Clinic
            ("25", 16, "Sakhi Women Protection & Legal Aid PLV", "Monday, Wednesday, Friday", "10:30 AM - 06:10 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 17: Mahanagarpalika Clinic
            ("03", 17, "Mahanagarpalika Civic Legal Aid Clinic PLV", "Monday, Wednesday, Friday", "10:30 AM - 06:10 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 19: Miyani Village Clinic
            ("04", 19, "Miyani Village Legal Aid Clinic PLV", "Monday, Tuesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 20: Visavada Village Clinic
            ("27", 20, "Visavada Village Legal Aid Clinic PLV", "Tuesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 21: Shingda Village Clinic
            ("14", 21, "Shingda Village Legal Aid Clinic PLV", "Monday, Wednesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 22: Bagvadar Village Clinic
            ("08", 22, "Bagvadar Village Legal Aid Clinic PLV", "Tuesday, Thursday, Saturday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 23: Advana Village Clinic
            ("18", 23, "Advana Village Legal Aid Clinic & Legal Assistance Centre PLV", "Monday, Wednesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 24: Godhana Village Clinic
            ("21", 24, "Godhana Village Legal Aid Clinic PLV", "Tuesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 25: Bakharla Village Clinic
            ("22", 25, "Bakharla Village Legal Aid Clinic PLV", "Monday, Wednesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 26: Degam Village Clinic
            ("59", 26, "Degam Village Legal Aid Clinic PLV", "Tuesday, Thursday, Saturday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 27: Kuchhadi Village Clinic
            ("09", 27, "Kuchhadi Village Legal Aid Clinic PLV", "Monday, Wednesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 28: Tukda Gosa Village Clinic
            ("16", 28, "Tukda Gosa Village Legal Aid Clinic PLV", "Tuesday, Thursday, Saturday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 29: Garej Village Clinic
            ("38", 29, "Garej Village Legal Aid Clinic PLV", "Monday, Tuesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 30: Ratiya Village Clinic
            ("28", 30, "Ratiya Village Legal Aid Clinic PLV", "Tuesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

            # Location 31: Madhavpur Village Clinic
            ("31", 31, "Madhavpur Village Legal Aid Clinic PLV", "Monday, Wednesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),
        ]

        assignments = []
        for sr_no, dep_id, role, days, hours, from_d, to_d, remarks in official_assignments:
            plv_obj = plv_dict.get(sr_no)
            dep_obj = dep_dict.get(dep_id)
            if plv_obj and dep_obj:
                assignment = PLVAssignment(
                    plv_id=plv_obj.id,
                    deployment_id=dep_obj.id,
                    duty_role=role,
                    days_of_week=days,
                    shift_hours=hours,
                    assigned_from=from_d,
                    assigned_to=to_d,
                    supervisor_remarks=f"{remarks}: Deployed at {dep_obj.place_name} under orders of Secretary, DLSA Porbandar.",
                    is_active=True
                )
                assignments.append(assignment)

        db.add_all(assignments)
        db.commit()

        # 6. Welfare Schemes tailored for Gujarat / Porbandar Public
        schemes = [
            Scheme(
                scheme_code="GSLSA-SCHEME-01",
                title="Gujarat Victim Compensation Scheme & Emergency Relief",
                target_group="Victims of Crime, Acid Attack Survivors & Road Accident Victims",
                short_description="Interim financial assistance and medical legal aid provided directly through DLSA Porbandar.",
                detailed_objectives="To provide expeditious interim and final financial compensation to victims of sexual offenses, acid attacks, motor accidents, and bodily harm under Section 357A CrPC / BNSS in Porbandar district.",
                eligibility_criteria="Any resident of Porbandar district or crime victim within Porbandar jurisdiction who has suffered grievous injury, loss of life, or physical trauma.",
                benefits="Interim relief within 15 days, ex-gratia compensation ranging from ₹1 Lakh to ₹10 Lakhs, free hospital medical coordination at Bhavsinhji Hospital Porbandar.",
                required_documents="FIR Copy, MLC Medical Report from Bhavsinhji Hospital, Aadhaar card, Bank Passbook copy.",
                application_process="Submit compensation petition at DLSA Front Office, District Court Complex, Porbandar or through hospital trauma desk PLV Dhaval Bamaniya.",
                nodal_officer="Secretary, DLSA Porbandar",
                icon_class="bi-heart-pulse",
                is_active=True
            ),
            Scheme(
                scheme_code="GSLSA-SCHEME-02",
                title="Legal Services to Coastal Fishermen & Salt-Pan Workers of Porbandar",
                target_group="Fisherfolk, Boat Laborers & Unorganised Salt Workers",
                short_description="Specialized legal aid for Porbandar's coastal fishing community, boat worker disputes, and social security claims.",
                detailed_objectives="To safeguard the livelihoods and safety of Porbandar and coastal Saurashtra fishermen, protect against illegal wage deduction by boat owners, and facilitate maritime accident claims.",
                eligibility_criteria="Traditional fishermen, Khalasi (boat crew), coastal laborers, and unorganised fisheries workers in Porbandar, Bokhira, and Chhaya.",
                benefits="Free legal representation before Labor Tribunals, assistance with fisheries department subsidies, maritime accident compensation petitions.",
                required_documents="Fishermen Biometric Card / e-Shram Card, Boat registration papers (if applicable), Aadhaar card.",
                application_process="Contact coastal PLVs Shruti Vaghela or Sanjana Baleja at Bokhira Legal Clinic or visit DLSA Porbandar Front Office.",
                nodal_officer="Chief Legal Aid Defense Counsel, Porbandar",
                icon_class="bi-water",
                is_active=True
            ),
            Scheme(
                scheme_code="GSLSA-SCHEME-03",
                title="Child Friendly Legal Services & POCSO Child Welfare Scheme",
                target_group="Children (Below 18 Years)",
                short_description="Free child defense and protection before Juvenile Justice Board (JJB) Porbandar and Child Welfare Committee.",
                detailed_objectives="To ensure that no minor in Porbandar comes into contact with the justice system without child-friendly representation, protective counseling, and rehabilitation.",
                eligibility_criteria="Any child below 18 years residing in Porbandar district in conflict with law or needing care and protection.",
                benefits="100% Free defense representation, psychological counseling, education support coordination.",
                required_documents="Age proof (Birth Certificate/School Record), parent/guardian statement.",
                application_process="Direct referral by Child Welfare Committee (CWC) Porbandar, Mahila Police Station, or PLV Alpana Poriya.",
                nodal_officer="Secretary, DLSA Porbandar",
                icon_class="bi-emoji-smile",
                is_active=True
            ),
            Scheme(
                scheme_code="GSLSA-SCHEME-04",
                title="Senior Citizens Legal Aid & Maintenance Scheme (Porbandar)",
                target_group="Senior Citizens (Aged 60+)",
                short_description="Enforcing elderly parents' rights to dignity, maintenance, and protection from property eviction by relatives.",
                detailed_objectives="To ensure prompt disposal of maintenance petitions under the Maintenance and Welfare of Parents and Senior Citizens Act before the SDM Tribunal, Porbandar.",
                eligibility_criteria="Senior citizens aged 60+ residing in Porbandar, Ranavav, or Kutiyana experiencing neglect or property coercion.",
                benefits="Free legal counsel, priority hearings at Sub-Divisional Magistrate (SDM) Tribunal Porbandar, doorstep PLV verification.",
                required_documents="Age proof (Aadhaar/Voter ID), details of respondent children/relatives.",
                application_process="Priority senior citizen counter at DLSA Front Office or home visit by PLV Hetvi Dave or Mahek Kothari.",
                nodal_officer="Secretary, DLSA Porbandar",
                icon_class="bi-person-heart",
                is_active=True
            ),
            Scheme(
                scheme_code="GSLSA-SCHEME-05",
                title="Women Domestic Violence Protection & Sakhi Centre Support Scheme",
                target_group="Women in Distress & Survivors of Violence",
                short_description="Immediate protection orders, safe shelter, and free court defense under Protection of Women from Domestic Violence Act.",
                detailed_objectives="To provide 360-degree legal, medical, and emotional shelter to women facing marital cruelty, dowry harassment, or abandonment in Porbandar.",
                eligibility_criteria="Any woman residing in Porbandar district irrespective of economic background.",
                benefits="Free lawyer for court cases, interim maintenance orders, residence orders, emergency stay at One Stop Centre (Sakhi) Porbandar.",
                required_documents="Identity card (if available), written complaint statement.",
                application_process="Direct walk-in to One Stop Centre Sakhi, Porbandar or call 0286-2245181; immediate assistance by PLVs Meera Unadkat and Manjula Chanpa.",
                nodal_officer="Secretary, DLSA Porbandar",
                icon_class="bi-shield-shaded",
                is_active=True
            ),
            Scheme(
                scheme_code="GSLSA-SCHEME-06",
                title="Porbandar National Lok Adalat & Pre-Litigation Mediation Scheme",
                target_group="All Litigants & Common Citizens",
                short_description="Amicable dispute settlement with zero court fees, refund of paid fees, and final binding award with no appeal.",
                detailed_objectives="To resolve pending cheque bounce, electricity/water bill, bank recovery, matrimonial, motor accident, and compoundable criminal cases without litigation expense.",
                eligibility_criteria="Any party to a pending dispute in Porbandar District Courts or having a pre-litigation matter.",
                benefits="No court fees; 100% refund of court fees already deposited; final decree; no further appeal; friendly atmosphere.",
                required_documents="Case number / notice details, identification.",
                application_process="Submit pre-litigation application at DLSA Porbandar Front Office or during quarterly National Lok Adalats.",
                nodal_officer="Chairman, DLSA Porbandar",
                icon_class="bi-bank2",
                is_active=True
            )
        ]
        db.add_all(schemes)
        db.commit()

        # 7. Porbandar Lok Adalat & Awareness Events
        events = [
            LokAdalatEvent(
                title="National Lok Adalat - District Court Porbandar",
                event_type="National Lok Adalat",
                event_date=date.today() + timedelta(days=18),
                time_schedule="10:00 AM to 05:00 PM",
                venue="District & Sessions Court Complex, Rajmahal Road, Porbandar",
                benches_count=8,
                presiding_officers="Sitting Judicial Officers of Porbandar, Senior Advocates & Social Mediators",
                eligible_matters="Cheque Bounce (NI Act 138), Motor Accident Claims (MACT), Matrimonial & Family Disputes, Bank Loan Recovery, Compoundable Criminal Cases, Land Acquisition, Labour Disputes, Civil Matters.",
                contact_person="Secretary, DLSA Porbandar (Ph: 0286-2244245)",
                assigned_plvs="PLV Nimisha Joshi (Sr. No. 01), PLV Parth Rathod (Sr. No. 03), PLV Nidhi Mashru (Sr. No. 04)",
                is_active=True
            ),
            LokAdalatEvent(
                title="Special Traffic Challan & Municipal Petty Matters Lok Adalat",
                event_type="Special Lok Adalat",
                event_date=date.today() + timedelta(days=40),
                time_schedule="10:30 AM to 04:30 PM",
                venue="Traffic Court / CJM Court, Porbandar",
                benches_count=4,
                presiding_officers="Judicial Magistrates First Class (JMFC), Porbandar",
                eligible_matters="Pending virtual traffic e-challans, municipal compoundable violations, minor shop & establishment fines.",
                contact_person="DLSA Front Office Porbandar (Ph: 0286-2244255)",
                assigned_plvs="PLV Hetvi Dave (Sr. No. 05), PLV Anjali Vaghela (Sr. No. 06)",
                is_active=True
            ),
            LokAdalatEvent(
                title="Mega Coastal & Rural Legal Literacy Camp - Chhaya & Bokhira",
                event_type="Legal Literacy Camp",
                event_date=date.today() + timedelta(days=8),
                time_schedule="11:00 AM to 03:00 PM",
                venue="Community Hall, Chhaya Nagarpalika, Porbandar",
                benches_count=2,
                presiding_officers="Secretary DLSA Porbandar, Medical Officers & Panel Advocates",
                eligible_matters="Awareness on Free Legal Aid, Rights of Coastal Fishermen, Senior Citizen Maintenance, Cyber Safety for Women, e-Shram Registration.",
                contact_person="DLSA Porbandar Legal Aid Cell (Ph: 0286-2244244)",
                assigned_plvs="PLV Nimisha Joshi (Sr. No. 01), PLV Himanshu Parmar (Sr. No. 32)",
                is_active=True
            )
        ]
        db.add_all(events)
        db.commit()

        # 8. Sample Porbandar Citizen Legal Aid Applications
        applications = [
            LegalAidApplication(
                application_number="DLSA-PBD-2026-101",
                applicant_name="Bhavnaben J. Rathod",
                gender="Female",
                phone="9879012345",
                email="bhavna.pbd@gmail.com",
                id_proof_type="Aadhaar",
                id_proof_number="XXXX-XXXX-8912",
                residential_address="Near Saibaba Mandir, Chhaya, Porbandar",
                category="Woman / Child",
                annual_income=45000.00,
                case_type="Domestic Violence",
                court_jurisdiction="Family Court, District Complex, Porbandar",
                opposing_party_details="Husband and in-laws residing at Chhaya, Porbandar",
                case_summary="Facing persistent domestic cruelty and abandonment. Seeking emergency maintenance order and child education support under PWDV Act.",
                assigned_counsel="Adv. Front Office Panel Lawyer",
                assigned_counsel_phone="98250 87654",
                assigned_plv_id=created_plvs[0][0].id, # Nimisha A. Joshi
                status="Counsel Assigned",
                status_notes="Panel counsel assigned by Secretary DLSA Porbandar; interim maintenance petition listed before Court No. 2.",
                last_sms_notification="[DLSA-SMS] Dear Ramilaben M. Solanki, Free Legal Counsel 'Adv. Front Office Panel Lawyer' (Contact: 98250 87654) has been assigned to your DLSA App #DLSA-PBD-2026-101. DLSA Helpline: 0286-2244222.",
                last_sms_sent_at=datetime.now(timezone.utc)
            ),
            LegalAidApplication(
                application_number="DLSA-PBD-2026-102",
                applicant_name="Kishorbhai M. Koli",
                gender="Male",
                phone="9725123456",
                email="kishor.koli@gmail.com",
                id_proof_type="Aadhaar",
                id_proof_number="XXXX-XXXX-3341",
                residential_address="Fishermen Colony, Bokhira, Porbandar",
                category="Industrial Workman",
                annual_income=72000.00,
                case_type="Labour & Wages",
                court_jurisdiction="Labour Court, Porbandar",
                opposing_party_details="M/s Sagar Trawler Agency, Porbandar Port",
                case_summary="Working as khalasi (boat crew) for 4 years. Unlawfully terminated without notice or settlement of 5 months pending fishing season wages. Seeking arrears.",
                assigned_counsel="Adv. Panel Lawyer",
                assigned_counsel_phone="94272 55667",
                assigned_plv_id=created_plvs[34][0].id, # Payal R. Vaja
                status="Mediation/Lok Adalat",
                status_notes="Notice issued to boat owner; conciliation conference scheduled at upcoming National Lok Adalat.",
                last_sms_notification="[DLSA-SMS] Dear Kishorbhai M. Koli, your case #DLSA-PBD-2026-102 has been referred to MEDIATION / LOK ADALAT for amicable settlement. DLSA Helpline: 0286-2244222.",
                last_sms_sent_at=datetime.now(timezone.utc)
            ),
            LegalAidApplication(
                application_number="DLSA-PBD-2026-103",
                applicant_name="Dhirubhai G. Dave",
                gender="Male",
                phone="9428345678",
                email="dhirubhai.dave@gmail.com",
                id_proof_type="Aadhaar",
                id_proof_number="XXXX-XXXX-6721",
                residential_address="Bhaveshwar Mandir Road, Porbandar",
                category="Senior Citizen (60+)",
                annual_income=30000.00,
                case_type="Senior Citizen Maintenance",
                court_jurisdiction="SDM Maintenance Tribunal, Porbandar",
                opposing_party_details="Elder son residing at Porbandar",
                case_summary="Age 73 years. Experiencing medical infirmities and denial of food and medicines. Seeking maintenance order under Senior Citizens Act.",
                assigned_counsel=None,
                assigned_counsel_phone=None,
                assigned_plv_id=created_plvs[5][0].id, # Hetvi B. Dave
                status="Under Scrutiny",
                status_notes="Application verified by PLV Hetvi Dave; counseling session scheduled at DLSA Porbandar Front Office.",
                last_sms_notification="[DLSA-SMS] Dear Dhirubhai G. Dave, your Legal Aid App #DLSA-PBD-2026-103 is now UNDER SCRUTINY by the DLSA Porbandar Legal Committee. Track online at dlsa-porbandar.gov.in/track?app_no=DLSA-PBD-2026-103",
                last_sms_sent_at=datetime.now(timezone.utc)
            ),
            LegalAidApplication(
                application_number="DLSA-PBD-2026-104",
                applicant_name="Jayshreeben K. Parmar",
                gender="Female",
                phone="9909456789",
                email="jayshree.parmar@gmail.com",
                id_proof_type="Aadhaar",
                id_proof_number="XXXX-XXXX-1122",
                residential_address="Sandipani Road, Porbandar",
                category="Annual Income under Rs 3 Lakh",
                annual_income=50000.00,
                case_type="Civil & Property",
                court_jurisdiction="Principal Senior Civil Judge Court, Porbandar",
                opposing_party_details="Private property dealer, Porbandar",
                case_summary="Illegal dispossession attempt from ancestral small residence on Sandipani Road. Seeking immediate temporary injunction.",
                assigned_counsel=None,
                assigned_counsel_phone=None,
                assigned_plv_id=created_plvs[31][0].id, # Himanshu V. Parmar
                status="Submitted",
                status_notes="Application received online; queued for scrutiny by DLSA Porbandar legal team.",
                last_sms_notification="[DLSA-SMS] Dear Jayshreeben K. Parmar, your Free Legal Aid Application #DLSA-PBD-2026-104 has been submitted successfully to DLSA Porbandar. Awaiting scrutiny.",
                last_sms_sent_at=datetime.now(timezone.utc)
            )
        ]
        db.add_all(applications)
        db.commit()

        logger.info("DLSA Porbandar official database seeding completed successfully with 44 PLVs!")

    except Exception as e:
        db.rollback()
        logger.error(f"Error during seeding: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database(force_reseed=True)
