# -*- coding: utf-8 -*-
"""
Migrates Deployments and PLVAssignments tables to official 31 locations
from DLSA Porbandar Office Orders No. 178/2026 and 179/2026.
"""
import sqlite3
from datetime import date, datetime, timezone

def update_database():
    conn = sqlite3.connect('dlsa.db')
    cur = conn.cursor()

    # 1. Update PLV records to match the official order
    plv_updates = [
        (10, 'Anjali B. Rathod', 'Female', '9879566710', 'Bagvadar, Porbandar'),
        (11, 'Rajesh M. Mandera', 'Male', '9974238551', 'Navibandar, Porbandar'),
        (12, 'Nirav B. Pankhaniya', 'Male', '8140429721', 'Shingda, Porbandar'),
        (14, 'Manish M. Modhvadiya', 'Male', '9016831016', 'Advana, Porbandar'),
        (15, 'Kajal B. Khunti', 'Female', '6301965197', 'Porbandar City'),
        (16, 'Rambhai H. Pandavadra', 'Male', '8238086334', 'Godhana, Porbandar'),
        (17, 'Dhara B. Vaja', 'Female', '9574778213', 'Bakharla, Porbandar'),
        (18, 'Ankita Parmar', 'Female', '7433025266', 'Madhavpur, Porbandar'),
        (20, 'Bhumi Parmar', 'Female', '7622865312', 'Visavada, Porbandar'),
        (21, 'Ravi Mokariya', 'Male', '9327532841', 'Ratiya, Porbandar'),
        (24, 'Hiren Mokariya', 'Male', '9574135513', 'Madhavpur, Porbandar'),
        (25, 'Mahek Rafish Sheta', 'Female', '9909341719', 'Porbandar City'),
        (26, 'Dhaval K. Bamaniya', 'Male', '6265487237', 'Porbandar City'),
        (27, 'Chandrika R. Chanchiya', 'Female', '7043388750', 'Porbandar City'),
        (28, 'Madhvi K. Shingrakhiya', 'Female', '9924535601', 'Porbandar City'),
        (29, 'Aarti B. Savaniya', 'Female', '9537221053', 'Garej, Porbandar'),
        (39, 'Mahek B. Kothari', 'Female', '7041111127', 'Porbandar City'),
        (22, 'Hasti V. Pandya', 'Female', '8980937526', 'Porbandar City'),
    ]
    for pid, name, gender, phone, addr in plv_updates:
        cur.execute('UPDATE PLVs SET full_name=?, gender=?, phone=?, residential_address=? WHERE id=?', (name, gender, phone, addr, pid))

    # 2. Clear old assignments and deployments
    cur.execute('DELETE FROM PLVAssignments')
    cur.execute('DELETE FROM Deployments')

    # 3. Insert 31 Official Locations
    deployments_data = [
        # --- 9 POLICE STATIONS (Order No. 179/2026) ---
        (
            1,
            "Kirtimandir Police Station",
            "Police Station",
            "Near Chowpatty / SV Road, Porbandar Urban",
            "Porbandar City",
            "Kirtimandir Police Station",
            "Police Inspector & DLSA Secretary",
            "0286-2242100",
            "24 Hours (3 Shifts: 06:00-14:00, 14:00-22:00, 22:00-06:00)",
            "Assistance for missing children, protection and counseling for child offenses under POCSO Act, 24-hour legal counsel for detainees under D.K. Basu guidelines.",
            "Child-friendly interaction corner, missing children helpdesk, telephone facility to inform relatives.",
            1
        ),
        (
            2,
            "Kamlabaug Police Station",
            "Police Station",
            "Station Road, Kamlabaug Area, Porbandar",
            "Kamlabaug, Porbandar",
            "Kamlabaug Police Station",
            "Police Inspector & DLSA Secretary",
            "0286-2242200",
            "10:00 AM - 06:00 PM (Daily)",
            "Assistance for missing children, child victim legal support, arrest intimation to families, free legal aid defense.",
            "Helpdesk booth, legal literature racks, counseling area.",
            1
        ),
        (
            3,
            "Mahila Police Station, Porbandar",
            "Police Station",
            "Jilla Seva Sadan - 1 Compound, Porbandar",
            "Chhaya / Porbandar",
            "Mahila Police Station",
            "Police Inspector & DLSA Secretary",
            "0286-2245100",
            "10:00 AM - 06:00 PM (Daily)",
            "Women victim support, missing children tracing, domestic violence legal counseling, compensation filing.",
            "Women counseling room, child play corner, victim shelter liaison.",
            1
        ),
        (
            4,
            "Udyognagar Police Station",
            "Police Station",
            "GIDC Industrial Estate, Udyognagar, Porbandar",
            "Udyognagar, Porbandar",
            "Udyognagar Police Station",
            "Police Inspector & DLSA Secretary",
            "0286-2243300",
            "10:00 AM - 06:00 PM (Daily)",
            "Industrial area missing children support, labor rights, juvenile assistance, free legal counsel.",
            "Public guidance desk, legal display board.",
            1
        ),
        (
            5,
            "Harbour Marine Police Station",
            "Police Station",
            "Subhash Nagar Coastal Road, Old Port, Porbandar",
            "Subhash Nagar, Porbandar",
            "Harbour Marine Police Station",
            "Police Inspector & DLSA Secretary",
            "0286-2244100",
            "10:00 AM - 06:00 PM (Daily)",
            "Coastal missing children assistance, maritime community child protection, fisherman rights, arrestee counsel.",
            "Coastal assistance desk, legal leaflets.",
            1
        ),
        (
            6,
            "Miyani Marine Police Station",
            "Police Station",
            "Miyani Coastal Outpost, Miyani, Porbandar District",
            "Miyani, Porbandar",
            "Miyani Marine Police Station",
            "Police Inspector & DLSA Secretary",
            "0286-2281100",
            "10:00 AM - 06:00 PM (Daily)",
            "Vigilance for missing children along coastal belt, juvenile protection, legal counseling for villagers.",
            "Marine police guidance corner.",
            1
        ),
        (
            7,
            "Bagvadar Police Station",
            "Police Station",
            "State Highway, Bagvadar, Porbandar District",
            "Bagvadar, Porbandar",
            "Bagvadar Police Station",
            "Police Sub-Inspector & DLSA Secretary",
            "02801-241200",
            "10:00 AM - 06:00 PM (Daily)",
            "Rural missing children tracking, agricultural laborer protection, juvenile offense prevention.",
            "Rural desk, legal advice center.",
            1
        ),
        (
            8,
            "Navibandar Police Station (TLSC)",
            "Police Station",
            "Coastal Highway, Navibandar, Porbandar District",
            "Navibandar, Porbandar",
            "Navibandar Police Station",
            "Police Sub-Inspector & DLSA Secretary",
            "02804-251200",
            "10:00 AM - 06:00 PM (Daily)",
            "Coastal rural missing children protection, fisherman family aid, free defense lawyer request filing.",
            "Helpdesk counter, brochure rack.",
            1
        ),
        (
            9,
            "Madhavpur Police Station (TLSC)",
            "Police Station",
            "Madhavpur Ghed Main Road, Madhavpur, Porbandar District",
            "Madhavpur Ghed, Porbandar",
            "Madhavpur Police Station",
            "Police Sub-Inspector & DLSA Secretary",
            "02804-272200",
            "10:00 AM - 06:00 PM (Daily)",
            "Pilgrim & child protection, missing children tracing, legal first-aid for arrestee families.",
            "Public guidance counter, complaint assistance booth.",
            1
        ),

        # --- 9 INSTITUTIONAL & COURT CLINICS (Order No. 178/2026) ---
        (
            10,
            "Jilla Panchayat Legal Aid Clinic",
            "Court & Institutional Clinic",
            "Jilla Panchayat Bhawan, Opp. Circuit House, Porbandar",
            "Porbandar Urban",
            "Kamlabaug Police Station",
            "District Development Officer & Secretary DLSA",
            "0286-2244244",
            "10:30 AM - 06:10 PM (Mon, Wed, Fri)",
            "Panchayat grievance conciliation, rural welfare schemes, senior citizen maintenance, widow pension documentation.",
            "Consultation chamber, welfare forms desk.",
            1
        ),
        (
            11,
            "Front Office DLSA Porbandar Legal Aid Clinic",
            "Court & Institutional Clinic",
            "Ground Floor, District Court Complex, Rajmahal Road, Porbandar",
            "Porbandar City",
            "Kirtimandir Police Station",
            "Secretary, DLSA Porbandar & Panel Lawyers",
            "0286-2222024",
            "10:30 AM - 06:10 PM (Daily)",
            "Walk-in legal counseling, Section 12 free legal aid applications, panel advocate assignment, Lok Adalat pre-litigation filing.",
            "Computerized tracking kiosk, legal literature rack, barrier-free access ramp, waiting hall.",
            1
        ),
        (
            12,
            "Family Court Help Desk & Legal Aid Clinic, Porbandar",
            "Court & Institutional Clinic",
            "Family Court Building, District Court Complex, Porbandar",
            "Porbandar City",
            "Kirtimandir Police Station",
            "Principal Judge, Family Court & DLSA Secretary",
            "0286-2244245",
            "10:30 AM - 06:10 PM (Daily)",
            "Matrimonial dispute pre-litigation settlement under GSLSA SOP, maintenance claim advice, child custody conciliation.",
            "Confidential counseling chamber, children play corner.",
            1
        ),
        (
            13,
            "Juvenile Justice Board (JJB) Legal Aid Clinic",
            "Court & Institutional Clinic",
            "Observation Home / JJB Court Complex, Chhaya Road, Porbandar",
            "Chhaya, Porbandar",
            "Kamlabaug Police Station",
            "Principal Magistrate, JJB & DLSA Secretary",
            "0286-2221234",
            "10:30 AM - 06:10 PM (Every Thursday)",
            "Representation for children in conflict with law, child welfare committee coordination, guardian counseling.",
            "Child-friendly inquiry room, counselor chamber.",
            1
        ),
        (
            14,
            "D.D. Kotiyawala Law College Legal Aid Clinic",
            "Court & Institutional Clinic",
            "D.D. Kotiyawala Municipal Law College, SV Road, Porbandar",
            "Porbandar City",
            "Kirtimandir Police Station",
            "Principal, Law College & DLSA Secretary",
            "0286-2242850",
            "09:00 AM - 01:30 PM & 03:30 PM - 05:30 PM (Mon, Wed, Fri)",
            "Student community legal awareness drives, public legal clinic, pro-bono law student assistance, village outreach.",
            "Law college moot court room, legal clinic cabin.",
            1
        ),
        (
            15,
            "Special Sub-Jail Clinic & Visitors Area Helpdesk",
            "Court & Institutional Clinic",
            "Jail Road, Near Old Custom House, Porbandar",
            "Porbandar City",
            "Kamlabaug Police Station",
            "Jail Superintendent & DLSA Visiting Advocate",
            "0286-2242350",
            "Visitors Area: 10:00-12:00 & 15:00-16:00 | Jail Clinic: 16:00-18:00 (Mon to Sat)",
            "Legal aid for undertrial inmates, bail drafting for indigent prisoners, UTRC review collation, visitor family assistance.",
            "Confidential legal consultation booth, visitor area guidance counter.",
            1
        ),
        (
            16,
            "Sakhi One Stop Centre Legal Aid Clinic, Porbandar",
            "Court & Institutional Clinic",
            "Jilla Seva Sadan - 2 Compound, Opp. District Court, Sandipani Road, Porbandar",
            "Chhaya / Porbandar",
            "Mahila Police Station, Porbandar",
            "Centre Administrator & DLSA Secretary",
            "0286-2245181",
            "10:30 AM - 06:10 PM (Mon, Wed, Fri)",
            "Protection of women from domestic violence, emergency shelter facilitation, legal aid lawyer appointment, psycho-social aid.",
            "Counseling cabin, temporary shelter rooms, police desk.",
            1
        ),
        (
            17,
            "Mahanagarpalika / Nagarpalika Porbandar Legal Aid Clinic",
            "Court & Institutional Clinic",
            "Nagarpalika Bhavan, M.G. Road, Porbandar",
            "Porbandar City",
            "Kirtimandir Police Station",
            "Chief Officer, Nagarpalika & DLSA Secretary",
            "0286-2242525",
            "10:30 AM - 06:10 PM (Mon, Wed, Fri)",
            "Civic dispute resolution, street vendor legal rights, urban slum dweller legal assistance, welfare claims.",
            "Civic guidance desk, public grievance counter.",
            1
        ),
        (
            18,
            "Jilla Sainik Board Legal Aid Clinic",
            "Court & Institutional Clinic",
            "Jilla Sainik Welfare Office, Jilla Seva Sadan, Porbandar",
            "Porbandar City",
            "Kamlabaug Police Station",
            "Jilla Sainik Welfare Officer & DLSA Secretary",
            "0286-2244244",
            "10:30 AM - 06:10 PM (Tue, Thu, Sat)",
            "Legal assistance for armed forces veterans, war widows, defense pensioner disputes, and family conciliation.",
            "Sainik consultation desk.",
            1
        ),

        # --- 13 VILLAGE LEGAL AID CLINICS (Order No. 178/2026) ---
        (
            19,
            "Miyani Village Legal Aid Clinic",
            "Village Legal Aid Clinic",
            "Gram Panchayat Office, Miyani, Porbandar District",
            "Miyani Village",
            "Miyani Marine Police Station",
            "Sarpanch / Talati & DLSA Secretary",
            "0286-2281100",
            "11:00 AM - 05:30 PM (Mon, Tue, Fri)",
            "Rural legal advice, land record mutation guidance, coastal dispute conciliation, Lok Adalat pre-litigation.",
            "Panchayat legal desk, Gujarati legal booklets.",
            1
        ),
        (
            20,
            "Visavada Village Legal Aid Clinic",
            "Village Legal Aid Clinic",
            "Gram Panchayat Bhavan, Visavada, Porbandar District",
            "Visavada Village",
            "Kamlabaug Police Station",
            "Sarpanch / Talati & DLSA Secretary",
            "0286-2244244",
            "11:00 AM - 05:30 PM (Tue, Fri)",
            "Farmer rights, rural civic dispute mediation, agricultural worker claims, free legal aid application.",
            "Village mediation corner.",
            1
        ),
        (
            21,
            "Shingda Village Legal Aid Clinic",
            "Village Legal Aid Clinic",
            "Gram Panchayat Bhavan, Shingda, Porbandar District",
            "Shingda Village",
            "Bagvadar Police Station",
            "Sarpanch / Talati & DLSA Secretary",
            "02801-241200",
            "11:00 AM - 05:30 PM (Mon, Wed, Fri)",
            "Village dispute conciliation, land mutation guidance, government scheme awareness, Lok Adalat registration.",
            "Panchayat guidance desk.",
            1
        ),
        (
            22,
            "Bagvadar Village Legal Aid Clinic",
            "Village Legal Aid Clinic",
            "Gram Panchayat Bhavan, Bagvadar, Porbandar District",
            "Bagvadar Village",
            "Bagvadar Police Station",
            "Sarpanch / Talati & DLSA Secretary",
            "02801-241200",
            "11:00 AM - 05:30 PM (Tue, Thu, Sat)",
            "Rural dispute mediation, legal literacy camps, widow and old age pension aid, revenue dispute counseling.",
            "Consultation room, informational posters.",
            1
        ),
        (
            23,
            "Advana Legal Aid Clinic & Legal Assistance Centre",
            "Village Legal Aid Clinic",
            "Panchayat Bhavan & Legal Assistance Centre, Advana, Porbandar District",
            "Advana Village",
            "Bagvadar Police Station",
            "Sarpanch / Talati & DLSA Secretary",
            "02801-242200",
            "11:00 AM - 05:30 PM (Mon, Wed, Fri)",
            "Advana regional legal assistance center, agrarian disputes conciliation, labor rights counseling, pre-litigation filing.",
            "Dedicated legal aid assistance room, brochure rack.",
            1
        ),
        (
            24,
            "Godhana Village Legal Aid Clinic",
            "Village Legal Aid Clinic",
            "Gram Panchayat Office, Godhana, Porbandar District",
            "Godhana Village",
            "Bagvadar Police Station",
            "Sarpanch / Talati & DLSA Secretary",
            "02801-243200",
            "11:00 AM - 05:30 PM (Tue, Fri)",
            "Rural legal guidance, agricultural labor support, family dispute counseling, government welfare claim filing.",
            "Panchayat mediation desk.",
            1
        ),
        (
            25,
            "Bakharla Village Legal Aid Clinic",
            "Village Legal Aid Clinic",
            "Gram Panchayat Bhavan, Bakharla, Porbandar District",
            "Bakharla Village",
            "Bagvadar Police Station",
            "Sarpanch / Talati & DLSA Secretary",
            "02801-244200",
            "11:00 AM - 05:30 PM (Mon, Wed, Fri)",
            "Village community mediation, farm laborer wage dispute guidance, women and child welfare assistance.",
            "Panchayat consultation cabin.",
            1
        ),
        (
            26,
            "Degam Village Legal Aid Clinic",
            "Village Legal Aid Clinic",
            "Gram Panchayat Office, Degam, Porbandar District",
            "Degam Village",
            "Bagvadar Police Station",
            "Sarpanch / Talati & DLSA Secretary",
            "02801-245200",
            "11:00 AM - 05:30 PM (Tue, Thu, Sat)",
            "Rural dispute conciliation, senior citizen maintenance support, Lok Adalat awareness.",
            "Panchayat legal corner.",
            1
        ),
        (
            27,
            "Kuchhadi Village Legal Aid Clinic",
            "Village Legal Aid Clinic",
            "Gram Panchayat Bhavan, Kuchhadi, Porbandar District",
            "Kuchhadi Village",
            "Kamlabaug Police Station",
            "Sarpanch / Talati & DLSA Secretary",
            "0286-2244244",
            "11:00 AM - 05:30 PM (Mon, Wed, Fri)",
            "Local dispute conciliation, unorganised sector worker guidance, women rights counseling, free lawyer application.",
            "Panchayat guidance table.",
            1
        ),
        (
            28,
            "Tukda Gosa Village Legal Aid Clinic",
            "Village Legal Aid Clinic",
            "Gram Panchayat Bhavan, Tukda Gosa, Porbandar District",
            "Tukda Gosa Village",
            "Navibandar Police Station",
            "Sarpanch / Talati & DLSA Secretary",
            "02804-252200",
            "11:00 AM - 05:30 PM (Tue, Thu, Sat)",
            "Rural matrimonial and family dispute counseling, agricultural worker welfare claims, Lok Adalat intake.",
            "Panchayat counseling room.",
            1
        ),
        (
            29,
            "Garej Village Legal Aid Clinic",
            "Village Legal Aid Clinic",
            "Gram Panchayat Bhavan, Garej, Porbandar District",
            "Garej Village",
            "Navibandar Police Station",
            "Sarpanch / Talati & DLSA Secretary",
            "02804-253200",
            "11:00 AM - 05:30 PM (Mon, Tue, Fri)",
            "Rural legal aid clinic, land dispute conciliation, rural social welfare documentation.",
            "Panchayat guidance desk.",
            1
        ),
        (
            30,
            "Ratiya Village Legal Aid Clinic",
            "Village Legal Aid Clinic",
            "Gram Panchayat Bhavan, Ratiya, Porbandar District",
            "Ratiya Village",
            "Navibandar Police Station",
            "Sarpanch / Talati & DLSA Secretary",
            "02804-254200",
            "11:00 AM - 05:30 PM (Tue, Fri)",
            "Agrarian dispute conciliation, farmer legal assistance, rural widow pension paperwork.",
            "Village mediation desk.",
            1
        ),
        (
            31,
            "Madhavpur Village Legal Aid Clinic",
            "Village Legal Aid Clinic",
            "Gram Panchayat Office, Madhavpur Ghed, Porbandar District",
            "Madhavpur Ghed",
            "Madhavpur Police Station",
            "Sarpanch / Talati & DLSA Secretary",
            "02804-272200",
            "11:00 AM - 05:30 PM (Mon, Wed, Fri)",
            "Comprehensive village legal aid, pre-litigation settlement, farmer & coastal worker dispute counseling.",
            "Community consultation center, legal awareness banner wall.",
            1
        )
    ]

    now_iso = datetime.now(timezone.utc).isoformat()
    for row in deployments_data:
        cur.execute('''
            INSERT INTO Deployments (id, place_name, place_type, address, area_locality, police_jurisdiction, incharge_officer, contact_phone, operating_hours, services_offered, facilities_available, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (*row, now_iso))

    # 4. Insert exact PLV assignments
    assignments_data = [
        # Location 1: Kirtimandir PS (3 shifts)
        (26, 1, "Police Station Child Protection & Legal Helpdesk (Morning Shift)", "Daily", "06:00 AM - 02:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),
        (25, 1, "Police Station Child Protection & Legal Helpdesk (Afternoon Shift)", "Daily", "02:00 PM - 10:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),
        (9, 1, "Police Station Child Protection & Legal Helpdesk (Night Shift)", "Daily", "10:00 PM - 06:00 AM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),
        
        # Location 2: Kamlabaug PS
        (28, 2, "Police Station Missing Children & Legal Aid PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

        # Location 3: Mahila PS
        (39, 3, "Women & Child Victim Protection PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

        # Location 4: Udyognagar PS
        (40, 4, "Police Station Missing Children & Legal Helpdesk PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

        # Location 5: Harbour Marine PS
        (41, 5, "Harbour Marine Legal Assistance & Child Protection PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

        # Location 6: Miyani Marine PS
        (44, 6, "Marine Police Child Protection & Legal Helpdesk PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

        # Location 7: Bagvadar PS
        (10, 7, "Rural Police Station Missing Children & Legal Aid PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

        # Location 8: Navibandar PS
        (11, 8, "Navibandar Police Station Child Protection PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

        # Location 9: Madhavpur PS
        (18, 9, "Madhavpur Police Station Child Protection PLV", "Daily", "10:00 AM - 06:00 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 179/2026"),

        # --- 9 INSTITUTIONAL & COURT CLINICS (Order No. 178/2026) ---
        # Location 10: Jilla Panchayat Clinic
        (27, 10, "Jilla Panchayat Legal Aid Clinic PLV", "Monday, Wednesday, Friday", "10:30 AM - 06:10 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 11: Front Office DLSA Porbandar
        (15, 11, "DLSA Front Office Legal Aid Desk Facilitator", "Daily", "10:30 AM - 06:10 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 178/2026"),

        # Location 12: Family Court Help Desk
        (22, 12, "Family Court Helpdesk & Matrimonial Conciliation PLV", "Daily", "10:30 AM - 06:10 PM", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 178/2026"),

        # Location 13: Juvenile Justice Board (JJB)
        (23, 13, "Juvenile Justice Board Child Rights PLV", "Every Thursday", "10:30 AM - 06:10 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 14: Law College Clinic
        (5, 14, "Law College Legal Clinic & DLSA Front Office PLV", "Monday, Wednesday, Friday", "09:00 AM - 01:30 PM & 03:30 PM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 15: Special Sub-Jail Clinic & Visitors Area
        (32, 15, "Sub-Jail Clinic & Visitors Area Helpdesk PLV", "Monday to Saturday", "10:00-12:00 & 15:00-16:00 (Visitors), 16:00-18:00 (Clinic)", date(2026, 10, 1), date(2026, 10, 15), "Office Order No. 178/2026"),

        # Location 16: Sakhi One Stop Centre Clinic
        (19, 16, "Sakhi Women Protection & Legal Aid PLV", "Monday, Wednesday, Friday", "10:30 AM - 06:10 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 17: Mahanagarpalika Clinic
        (2, 17, "Mahanagarpalika Civic Legal Aid Clinic PLV", "Monday, Wednesday, Friday", "10:30 AM - 06:10 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # --- 13 VILLAGE CLINICS (Order No. 178/2026) ---
        # Location 19: Miyani Village Clinic
        (3, 19, "Miyani Village Legal Aid Clinic PLV", "Monday, Tuesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 20: Visavada Village Clinic
        (20, 20, "Visavada Village Legal Aid Clinic PLV", "Tuesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 21: Shingda Village Clinic
        (12, 21, "Shingda Village Legal Aid Clinic PLV", "Monday, Wednesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 22: Bagvadar Village Clinic
        (7, 22, "Bagvadar Village Legal Aid Clinic PLV", "Tuesday, Thursday, Saturday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 23: Advana Village Clinic
        (14, 23, "Advana Village Legal Aid Clinic & Legal Assistance Centre PLV", "Monday, Wednesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 24: Godhana Village Clinic
        (16, 24, "Godhana Village Legal Aid Clinic PLV", "Tuesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 25: Bakharla Village Clinic
        (17, 25, "Bakharla Village Legal Aid Clinic PLV", "Monday, Wednesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 26: Degam Village Clinic
        (43, 26, "Degam Village Legal Aid Clinic PLV", "Tuesday, Thursday, Saturday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 27: Kuchhadi Village Clinic
        (8, 27, "Kuchhadi Village Legal Aid Clinic PLV", "Monday, Wednesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 28: Tukda Gosa Village Clinic
        (13, 28, "Tukda Gosa Village Legal Aid Clinic PLV", "Tuesday, Thursday, Saturday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 29: Garej Village Clinic
        (29, 29, "Garej Village Legal Aid Clinic PLV", "Monday, Tuesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 30: Ratiya Village Clinic
        (21, 30, "Ratiya Village Legal Aid Clinic PLV", "Tuesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026"),

        # Location 31: Madhavpur Village Clinic
        (24, 31, "Madhavpur Village Legal Aid Clinic PLV", "Monday, Wednesday, Friday", "11:00 AM - 05:30 PM", date(2026, 10, 1), date(2026, 10, 31), "Office Order No. 178/2026")
    ]

    for plv_id, dep_id, role, days, hours, from_d, to_d, remarks in assignments_data:
        cur.execute('''
            INSERT INTO PLVAssignments (plv_id, deployment_id, duty_role, days_of_week, shift_hours, assigned_from, assigned_to, supervisor_remarks, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
        ''', (plv_id, dep_id, role, days, hours, from_d.isoformat(), to_d.isoformat(), remarks, now_iso))

    conn.commit()
    conn.close()
    print("Database successfully updated with 31 official DLSA Porbandar locations and assignments!")

if __name__ == "__main__":
    update_database()
