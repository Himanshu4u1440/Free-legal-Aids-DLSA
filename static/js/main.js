// DLSA Interactive Functionality & Bilingual Engine
document.addEventListener('DOMContentLoaded', function () {
    // ------------------------------------------------------------------------
    // 1. DLSA Official Bilingual Translation Dictionary (English -> Gujarati)
    // ------------------------------------------------------------------------
    const DLSA_TRANSLATIONS = {
        // Navigation & Topbar
        "24x7 HELPLINE": "૨૪x૭ હેલ્પલાઇન",
        "National Legal Aid:": "રાષ્ટ્રીય કાનૂની સહાય:",
        "National Legal Aid": "રાષ્ટ્રીય કાનૂની સહાય",
        "DLSA Porbandar Office:": "ડીએલએસએ પોરબંદર કાર્યાલય:",
        "DLSA Porbandar Office: 0286-2244244": "ડીએલએસએ પોરબંદર કાર્યાલય: ૦૨૮૬-૨૨૪૪૨૪૪",
        "Mon-Sat: 10:00 AM - 05:30 PM": "સોમ-શનિ: સવારે ૧૦:૦૦ થી સાંજે ૦૫:૩૦",
        "Porbandar, Gujarat": "પોરબંદર, ગુજરાત",
        "DLSA Staff Portal": "ડીએલએસએ સ્ટાફ પોર્ટલ",
        "Admin Panel": "એડમિન પેનલ",
        "Logout": "લૉગઆઉટ",
        "Home": "મુખપૃષ્ઠ",
        "Rank": "ન્યાયિક પદ અને અધિકારીઓ",
        "High Ranks": "ન્યાયિક પદ અને અધિકારીઓ",
        "Leadership Hierarchy": "ન્યાયિક પદ અને અધિકારીઓ",
        "Porbandar PLVs (44)": "પોરબંદર પીએલવી (૪૪)",
        "Deployments & Clinics": "નિમણૂક કેન્દ્રો & ક્લિનિક્સ",
        "Schemes": "કાનૂની યોજનાઓ",
        "Track Status": "અરજી સ્થિતિ",
        "Apply Free Legal Aid": "મફત કાનૂની સહાય મેળવો",
        "Apply for Free Legal Aid": "મફત કાનૂની સહાય માટે અરજી કરો",
        "Meet Our 44 Porbandar PLVs": "અમારા ૪૪ પોરબંદર પીએલવીને મળો",
        "Porbandar Clinics & Desks": "પોરબંદર ક્લિનિક્સ અને હેલ્પડેસ્ક",
        "Porbandar Clinics & Helpdesks": "પોરબંદર ક્લિનિક્સ અને હેલ્પડેસ્ક",
        
        // Brand & Helpline
        "DISTRICT LEGAL SERVICES AUTHORITY, PORBANDAR": "જિલ્લા કાનૂની સેવા સત્તા મંડળ, પોરબંદર",
        "Porbandar District Citizen Legal Aid Helpline": "પોરબંદર જિલ્લા નાગરિક મફત કાનૂની સહાય હેલ્પલાઇન",
        "Serving residents of Porbandar, Chhaya, Bokhira, Ranavav, Kutiyana, and Jam Raval.": "પોરબંદર, છાયા, બોખીરા, રાણાવાવ, કુતિયાણા અને જામ રાવલના નાગરિકોની સેવામાં સમર્પિત.",
        "Toll-Free Helpline:": "ટોલ-ફ્રી હેલ્પલાઇન:",

        // Homepage & Eligibility Checker
        "Free Legal Aid Checker": "મફત કાનૂની સહાય પાત્રતા તપાસો",
        "Section 12 Entitlement (પોરબંદર)": "કલમ ૧૨ કાનૂની પાત્રતા (પોરબંદર)",
        "Check if you qualify for free defense lawyers, free court filing, and exemption from litigation fees in Porbandar Courts.": "પોરબંદર અદાલતોમાં મફત સરકારી વકીલ, મફત અરજી ડ્રાફ્ટિંગ અને કોર્ટ ફી માફી માટે તમારી પાત્રતા ચકાસો.",
        "Woman or Child (Below 18)": "મહિલા અથવા બાળક (૧૮ વર્ષથી નીચે)",
        "Member of SC / ST Community": "અનુસૂચિત જાતિ (SC) / અનુસૂચિત જનજાતિ (ST) સભ્ય",
        "Person in Custody / Sub-Jail Porbandar": "કસ્ટડી / ખાસ સબ-જેલ પોરબંદરમાં રહેલ વ્યક્તિ",
        "Coastal Fisherman / Salt Worker / Workman": "સાગરખેડૂ માછીમાર / અગરીયા / ઔદ્યોગિક શ્રમિક",
        "Person with Disability / Mental Illness": "દિવ્યાંગ વ્યક્તિ / માનસિક રીતે અસ્વસ્થ",
        "Annual Family Income (₹):": "વાર્ષિક કૌટુંબિક આવક (₹):",
        "General threshold: Up to ₹3,00,000 / year": "સામાન્ય મર્યાદા: વાર્ષિક ₹૩,૦૦,૦૦૦ સુધી",
        "Check My Eligibility Now": "મારી પાત્રતા અત્યારે જ તપાસો",
        "Certified Porbandar PLVs": "પ્રમાણિત પોરબંદર પીએલવી",
        "Official ID Cards Issued": "સત્તાવાર ઓળખપત્ર જારી",
        "Deployed Centers & Clinics": "કાર્યરત કેન્દ્રો અને ક્લિનિક્સ",
        "Police Stations, Jail & Hospital": "પોલીસ સ્ટેશનો, જેલ અને હોસ્પિટલ",
        "Special Welfare Schemes": "વિશેષ કલ્યાણકારી યોજનાઓ",
        "Victims, Fishermen & Children": "પીડિતો, માછીમારો અને બાળકો માટે",
        "Victim Relief, Fishermen, Children": "પીડિતો, માછીમારો અને બાળકો માટે",
        "District Legal Aid Applications": "જિલ્લા કાનૂની સહાય અરજીઓ",
        "100% Free Defense Provided": "૧૦૦% મફત કાનૂની બચાવ પૂરો પડાયો",
        "Citizen Cases Assisted": "નાગરિક કેસોમાં સહાય આપી",
        "Active In Porbandar Courts": "પોરબંદર અદાલતોમાં સક્રિય",
        "Porbandar Public Legal Services": "પોરબંદર જાહેર કાનૂની સેવાઓ",
        "How DLSA Porbandar Serves Common Citizens": "ડીએલએસએ પોરબંદર સામાન્ય નાગરિકોની સેવા કેવી રીતે કરે છે",
        "No resident of Porbandar district shall be denied justice due to poverty or lack of legal awareness. All our services are 100% free of cost.": "ગરીબી કે કાનૂની અજ્ઞાનતાને કારણે પોરબંદર જિલ્લાના કોઈપણ નાગરિકને ન્યાયથી વંચિત રહેવું પડશે નહીં. અમારી તમામ સેવાઓ ૧૦૦% નિઃશુલ્ક છે.",
        "Free Panel Lawyers": "મફત પેનલ વકીલો",
        "Free defense advocates and legal aid counsel appointed to contest your civil, criminal, matrimonial, or revenue cases in Porbandar Courts.": "પોરબંદરની અદાલતોમાં તમારા દીવાની, ફોજદારી, પારિવારિક કે મહેસૂલી કેસો લડવા માટે મફત બચાવ વકીલ અને સહાય કાઉન્સેલની નિમણૂક કરવામાં આવે છે.",
        "Request Free Counsel →": "મફત વકીલ મેળવો →",
        "Request Free Counsel": "મફત વકીલ મેળવો",
        "44 Para Legal Volunteers": "૪૪ પેરા લીગલ વોલેન્ટિયર્સ",
        "Our officially certified cadre of 44 PLVs deployed across Porbandar, Chhaya, Bokhira, Ranavav, and Kutiyana to bridge citizens with justice.": "નાગરિકો અને ન્યાયતંત્ર વચ્ચે સેતુ બનવા માટે પોરબંદર, છાયા, બોખીરા, રાણાવાવ અને કુતિયાણામાં તૈનાત ૪૪ પ્રમાણિત પીએલવીનો સત્તાવાર સંવર્ગ.",
        "Explore PLVs & ID Cards →": "પીએલવી અને આઈડી કાર્ડ જુઓ →",
        "Explore PLVs & ID Cards": "પીએલવી અને આઈડી કાર્ડ જુઓ",
        "10 Deployment Centers": "૧૦ નિમણૂક કેન્દ્રો",
        "Visit DLSA helpdesks at District Court Front Office, 'A' & 'B' Division Police Stations, Sub-Jail, Bhavsinhji Hospital, or Chhaya & Bokhira Clinics.": "જિલ્લા અદાલત ફ્રન્ટ ઓફિસ, 'એ' અને 'બી' ડિવિઝન પોલીસ સ્ટેશન, સબ-જેલ, ભાવસિંહજી હોસ્પિટલ અથવા છાયા અને બોખીરા ક્લિનિક્સ ખાતે ડીએલએસએ હેલ્પડેસ્કની મુલાકાત લો.",
        "View Porbandar Centers →": "પોરબંદર કેન્દ્રો જુઓ →",
        "View Porbandar Centers": "પોરબંદર કેન્દ્રો જુઓ",
        "National Lok Adalat": "રાષ્ટ્રીય લોક અદાલત",
        "Expeditious, friendly settlement of pending disputes and pre-litigation claims with zero court fees and complete refund of fees already paid.": "શૂન્ય કોર્ટ ફી અને ભરેલી કોર્ટ ફીના ૧૦૦% પરત રિફંડ સાથે પેન્ડિંગ વિવાદો અને પ્રી-લિટિગેશન દાવાઓનું ઝડપી અને મૈત્રીપૂર્ણ સમાધાન.",
        "Lok Adalat Notice →": "લોક અદાલત વિગત →",
        "Lok Adalat Notice": "લોક અદાલત વિગત",
        "Authority Management": "સત્તા મંડળ વહીવટ",
        "Top High Ranks Managing DLSA Porbandar": "ડીએલએસએ પોરબંદરનું સંચાલન કરતા ઉચ્ચ હોદ્દાઓ",
        "Executive Council": "કાર્યકારી પરિષદ",
        "Full Leadership & Structure Directory": "સંપૂર્ણ નેતૃત્વ અને સંગઠનાત્મક માળખું",
        "View Full Hierarchy & Ranks": "સંપૂર્ણ માળખું અને હોદ્દાઓ જુઓ",
        "Full Profile & Legal Powers →": "સંપૂર્ણ પરિચય અને કાનૂની સત્તા →",
        "Full Profile & Legal Powers": "સંપૂર્ણ પરિચય અને કાનૂની સત્તા",
        "Meet All 44 Porbandar PLVs": "પોરબંદરના તમામ ૪૪ પીએલવીને મળો",
        "Certified Para Legal Volunteers of DLSA Porbandar": "ડીએલએસએ પોરબંદરના પ્રમાણિત પેરા લીગલ વોલેન્ટિયર્સ",
        "View All 44 PLVs & ID Cards": "તમામ ૪૪ પીએલવી અને આઈડી કાર્ડ જુઓ",
        "View All 44 PLV Cards & Roles →": "તમામ ૪૪ પીએલવી કાર્ડ અને ફરજો જુઓ →",
        "Scheduled National Lok Adalat Events in Porbandar": "પોરબંદરમાં આયોજિત રાષ્ટ્રીય લોક અદાલત કાર્યક્રમો",
        "National Lok Adalat & Legal Literacy Camps": "રાષ્ટ્રીય લોક અદાલત અને કાનૂની સાક્ષરતા શિબિરો",
        "Settlement of court cases and public awareness drives in Porbandar District": "પોરબંદર જિલ્લામાં પેન્ડિંગ કોર્ટ કેસોનું સમાધાન અને જાહેર જાગૃતિ ઝુંબેશ",

        // Deployments & Clinics
        "Places of Deployment & Legal Aid Clinics | DLSA": "નિમણૂક કેન્દ્રો અને લીગલ એઇડ ક્લિનિક્સ | ડીએલએસએ પોરબંદર",
        "Places Where PLVs & Legal Aid Clinics are Deployed": "પીએલવી અને કાનૂની સહાય ક્લિનિક્સ કાર્યરત હોય તેવા સ્થળો",
        "Locate official DLSA assistance desks across courts, police stations, prisons, hospitals, and rural clinics": "અદાલતો, પોલીસ સ્ટેશનો, જેલ, હોસ્પિટલો અને ગ્રામીણ ક્લિનિક્સમાં ડીએલએસએ સહાય ડેસ્ક શોધો",
        "Why Are DLSA Helpdesks Located Here?": "ડીએલએસએ હેલ્પડેસ્ક અહીં શા માટે ઉપલબ્ધ છે?",
        "All Locations": "તમામ સ્થાનો",
        "All Locations (31)": "તમામ સ્થાનો (૩૧)",
        "Police Stations (9)": "પોલીસ સ્ટેશનો (૯)",
        "Courts & Institutional Clinics (9)": "અદાલત અને સંસ્થાકીય ક્લિનિક્સ (૯)",
        "Village Legal Aid Clinics (13)": "ગ્રામીણ લીગલ એઇડ ક્લિનિક્સ (૧૩)",
        "Police Stations": "પોલીસ સ્ટેશનો",
        "Courts & Institutional Clinics": "અદાલત અને સંસ્થાકીય ક્લિનિક્સ",
        "Village Legal Aid Clinics": "ગ્રામીણ લીગલ એઇડ ક્લિનિક્સ",
        "Court Front Offices": "અદાલત ફ્રન્ટ ઓફિસો",
        "Court Front Office": "અદાલત ફ્રન્ટ ઓફિસ",
        "Police Station": "પોલીસ સ્ટેશન",
        "Court & Institutional Clinic": "અદાલત અને સંસ્થાકીય ક્લિનિક",
        "Village Legal Aid Clinic": "ગ્રામીણ લીગલ એઇડ ક્લિનિક",
        "Jail Clinics": "જેલ ક્લિનિક્સ",
        "Central Jail / Sub-Jail": "ખાસ સબ-જેલ ક્લિનિક",
        "Hospital Desks": "હોસ્પિટલ ડેસ્ક",
        "Hospital Desk": "હોસ્પિટલ સહાય ડેસ્ક",
        "Gram Panchayat Clinics": "ગ્રામ પંચાયત ક્લિનિક્સ",
        "Legal Aid Clinic": "કાનૂની સહાય ક્લિનિક",
        "Sakhi Centers": "સખી કેન્દ્રો (મહિલા સહાય)",
        "One Stop Centre (Sakhi)": "વન સ્ટોપ સેન્ટર (સખી)",
        "Services Available to the Public:": "નાગરિકો માટે ઉપલબ્ધ સેવાઓ:",
        "Services Available to the Public": "નાગરિકો માટે ઉપલબ્ધ સેવાઓ",
        "Facilities on Site:": "સ્થળ પર ઉપલબ્ધ સુવિધાઓ:",
        "Facilities on Site": "સ્થળ પર ઉપલબ્ધ સુવિધાઓ",
        "Assigned Para Legal Volunteers (PLVs):": "ફાળવેલ પેરા લીગલ વોલેન્ટિયર્સ (PLVs):",
        "Assigned Para Legal Volunteers (PLVs)": "ફાળવેલ પેરા લીગલ વોલેન્ટિયર્સ (PLVs)",
        "Duty Volunteer": "ફરજ પરના સ્વયંસેવક",
        "In-charge:": "ઇન્ચાર્જ:",
        "In-charge": "ઇન્ચાર્જ",
        "Helpline:": "હેલ્પલાઇન:",
        "Helpline": "હેલ્પલાઇન",
        "Jurisdiction:": "અધિકારક્ષેત્ર:",
        "Jurisdiction": "અધિકારક્ષેત્ર",
        "Active PLVs": "સક્રિય સ્વયંસેવકો",
        "Deployed PLVs": "હાજર પીએલવી",
        "Deployed Volunteers": "હાજર સ્વયંસેવકો",
        "Deployment Places": "નિમણૂક સ્થાનો",
        "Managed by DLSA Roster Panel Advocates on Duty": "ડીએલએસએ રોસ્ટર પેનલ એડવોકેટ્સ દ્વારા સંચાલિત",
        "10:00 AM - 05:00 PM (Mon-Sat)": "સવારે ૧૦:૦૦ થી સાંજે ૦૫:૦૦ (સોમ-શનિ)",
        "10:00 AM - 05:30 PM (Mon-Sat)": "સવારે ૧૦:૦૦ થી સાંજે ૦૫:૩૦ (સોમ-શનિ)",
        "Monday to Saturday": "સોમવાર થી શનિવાર",
        "Monday to Friday": "સોમવાર થી શુક્રવાર",
        "Daily": "દરરોજ",
        "Every Thursday": "દર ગુરુવારે",
        "Monday, Wednesday, Friday": "સોમવાર, બુધવાર, શુક્રવાર",
        "Tuesday, Friday": "મંગળવાર, શુક્રવાર",
        "Monday, Tuesday, Friday": "સોમવાર, મંગળવાર, શુક્રવાર",
        "Tuesday, Thursday, Saturday": "મંગળવાર, ગુરુવાર, શનિવાર",

        // 31 Official Deployment Locations
        "Kirtimandir Police Station": "કીર્તિમંદિર પોલીસ સ્ટેશન",
        "Kamlabaug Police Station": "કમલાબાગ પોલીસ સ્ટેશન",
        "Mahila Police Station, Porbandar": "મહિલા પોલીસ સ્ટેશન, પોરબંદર",
        "Udyognagar Police Station": "ઉદ્યોગનગર પોલીસ સ્ટેશન",
        "Harbour Marine Police Station": "હાર્બર મરીન પોલીસ સ્ટેશન",
        "Miyani Marine Police Station": "મિયાણી મરીન પોલીસ સ્ટેશન",
        "Bagvadar Police Station": "બગવદર પોલીસ સ્ટેશન",
        "Navibandar Police Station (TLSC)": "નવીબંદર પોલીસ સ્ટેશન (TLSC)",
        "Navibandar Police Station": "નવીબંદર પોલીસ સ્ટેશન",
        "Madhavpur Police Station (TLSC)": "માધવપુર પોલીસ સ્ટેશન (TLSC)",
        "Madhavpur Police Station": "માધવપુર પોલીસ સ્ટેશન",
        "Jilla Panchayat Legal Aid Clinic": "જિલ્લા પંચાયત લીગલ એઇડ ક્લિનિક",
        "Front Office DLSA Porbandar Legal Aid Clinic": "ફ્રન્ટ ઓફિસ ડીએલએસએ પોરબંદર લીગલ એઇડ ક્લિનિક",
        "Family Court Help Desk & Legal Aid Clinic, Porbandar": "ફેમિલી કોર્ટ હેલ્પ ડેસ્ક & લીગલ એઇડ ક્લિનિક, પોરબંદર",
        "Juvenile Justice Board (JJB) Legal Aid Clinic": "જુવેનાઈલ જસ્ટિસ બોર્ડ (JJB) લીગલ એઇડ ક્લિનિક",
        "D.D. Kotiyawala Law College Legal Aid Clinic": "ડી.ડી. કોટીયાવાલા લૉ કોલેજ લીગલ એઇડ ક્લિનિક",
        "Special Sub-Jail Clinic & Visitors Area Helpdesk": "ખાસ સબ-જેલ ક્લિનિક & મુલાકાતી વિસ્તાર હેલ્પડેસ્ક",
        "Sakhi One Stop Centre Legal Aid Clinic, Porbandar": "સખી વન સ્ટોપ સેન્ટર લીગલ એઇડ ક્લિનિક, પોરબંદર",
        "Mahanagarpalika / Nagarpalika Porbandar Legal Aid Clinic": "મહાનગરપાલિકા / નગરપાલિકા પોરબંદર લીગલ એઇડ ક્લિનિક",
        "Jilla Sainik Board Legal Aid Clinic": "જિલ્લા સૈનિક બોર્ડ લીગલ એઇડ ક્લિનિક",
        "Miyani Village Legal Aid Clinic": "મિયાણી ગ્રામીણ લીગલ એઇડ ક્લિનિક",
        "Visavada Village Legal Aid Clinic": "વિસાવડા ગ્રામીણ લીગલ એઇડ ક્લિનિક",
        "Shingda Village Legal Aid Clinic": "શિંગડા ગ્રામીણ લીગલ એઇડ ક્લિનિક",
        "Bagvadar Village Legal Aid Clinic": "બગવદર ગ્રામીણ લીગલ એઇડ ક્લિનિક",
        "Advana Legal Aid Clinic & Legal Assistance Centre": "અડવાણા લીગલ એઇડ ક્લિનિક & કાનૂની સહાય કેન્દ્ર",
        "Godhana Village Legal Aid Clinic": "ગોઢાણા ગ્રામીણ લીગલ એઇડ ક્લિનિક",
        "Bakharla Village Legal Aid Clinic": "બાખરલા ગ્રામીણ લીગલ એઇડ ક્લિનિક",
        "Degam Village Legal Aid Clinic": "દેગામ ગ્રામીણ લીગલ એઇડ ક્લિનિક",
        "Kuchhadi Village Legal Aid Clinic": "કુછડી ગ્રામીણ લીગલ એઇડ ક્લિનિક",
        "Tukda Gosa Village Legal Aid Clinic": "ટુકડા ગોસા ગ્રામીણ લીગલ એઇડ ક્લિનિક",
        "Garej Village Legal Aid Clinic": "ગરેજ ગ્રામીણ લીગલ એઇડ ક્લિનિક",
        "Ratiya Village Legal Aid Clinic": "રતિયા ગ્રામીણ લીગલ એઇડ ક્લિનિક",
        "Madhavpur Village Legal Aid Clinic": "માધવપુર ગ્રામીણ લીગલ એઇડ ક્લિનિક",

        // Leadership & Rank Hierarchy
        "Leadership & Management Hierarchy | District Legal Services Authority": "ન્યાયિક પદ અને નેતૃત્વ | જિલ્લા કાનૂની સેવા સત્તા મંડળ, પોરબંદર",
        "Rank & Judicial Leadership | District Legal Services Authority, Porbandar": "ન્યાયિક પદ અને નેતૃત્વ | જિલ્લા કાનૂની સેવા સત્તા મંડળ, પોરબંદર",
        "DLSA Judicial Officers & Leadership Hierarchy": "ડીએલએસએ ન્યાયિક અધિકારીઓ અને હોદ્દાઓ",
        "The judicial officers, defense counsels, and legal administrators managing District Legal Services Authority": "જિલ્લા કાનૂની સેવા સત્તા મંડળનું સંચાલન કરતા ન્યાયિક અધિકારીઓ, બચાવ પક્ષના વકીલો અને વહીવટી વડાઓ",
        "Statutory Organisational Hierarchy": "કાયદાકીય સંગઠનાત્મક માળખું",
        "Judicial Head": "ન્યાયિક વડા",
        "Chief Executive": "મુખ્ય કાર્યકારી અધિકારી",
        "Defense Head": "બચાવ પક્ષના વડા",
        "Defense Counsel": "કાનૂની સંરક્ષણ કાઉન્સેલ",
        "Front Office Convener": "ફ્રન્ટ ઓફિસ કન્વીનર",
        "Community Legal Assistance": "સામુદાયિક કાનૂની સહાય",
        "Chairman, DLSA": "ચેરમેનશ્રી, ડીએલએસએ",
        "Principal District & Sessions Judge": "પ્રિન્સિપાલ ડિસ્ટ્રિક્ટ એન્ડ સેશન્સ જજ",
        "Secretary, DLSA": "સેક્રેટરીશ્રી, ડીએલએસએ",
        "Senior Civil Judge Cadre": "સિનિયર સિવિલ જજ કેડર",
        "Chief LADC": "ચીફ એલ.એ.ડી.સી. (મુખ્ય કાનૂની બચાવ કાઉન્સેલ)",
        "Legal Aid Defense Counsel": "લીગલ એઇડ ડિફેન્સ કાઉન્સેલ",
        "PLVs & Panel Advocates": "પીએલવી અને પેનલ એડવોકેટ્સ",
        "Field Volunteers & Advocates": "ફીલ્ડ વોલેન્ટિયર્સ અને પેનલ વકીલો",
        "Executive Council & Judicial Officers Directory": "કાર્યકારી પરિષદ અને ન્યાયિક અધિકારીઓની ડિરેક્ટરી",
        "Profile Overview:": "અધિકારી પરિચય:",
        "Statutory Duties & Key Powers:": "કાયદાકીય સત્તા અને મુખ્ય ફરજો:",
        "Statutory Powers & Accountability": "કાયદાકીય સત્તા અને લોકજવાબદારી",
        "Office:": "કચેરીનું સરનામું:",
        "Phone:": "સંપર્ક નંબર:",
        "Official Email:": "સત્તાવાર ઇમેઇલ:",
        "Rank & Leadership": "ન્યાયિક પદ અને નેતૃત્વ",
        
        // PLV Portal
        "District Legal Service Authority, Porbandar": "જિલ્લા કાનૂની સેવા સત્તા મંડળ, પોરબંદર",
        "Official 2026-2027 Cadre": "સત્તાવાર ૨૦૨૬-૨૦૨૭ સંવર્ગ",
        "Official Volunteer Allocation & Citizen Assistance Protocol:": "સત્તાવાર પેરા લીગલ વોલેન્ટિયર ફાળવણી અને નાગરિક સહાય પ્રોટોકોલ:",
        "Who are the PLVs of DLSA Porbandar?": "ડીએલએસએ પોરબંદરના પીએલવી (PLV) કોણ છે?",
        "Zero Charges for Common People:": "સામાન્ય નાગરિકો માટે ૧૦૦% મફત સેવા:",
        "Official Identity Card Rules": "સત્તાવાર ઓળખપત્રના કાયદાકીય નિયમો",
        "12 Statutory Duties of Porbandar PLVs": "પોરબંદર પીએલવીની ૧૨ બંધારણીય અને કાનૂની ફરજો",
        "All Statuses": "તમામ સ્થિતિ",
        "Active": "સક્રિય",
        "Inactive": "નિષ્ક્રિય",
        "All Genders": "તમામ જાતિ",
        "Male": "પુરુષ",
        "Female": "મહિલા",
        "Other": "અન્ય",
        "Request This PLV": "આ પીએલવીની સહાય મેળવો",
        "View Official Card": "સત્તાવાર કાર્ડ જુઓ",
        "DLSA Sr. No.": "ડીએલએસએ ક્રમ નં.",
        "Designation:": "હોદ્દો:",
        "PLV (Para Legal Volunteer)": "પીએલવી (પેરા લીગલ વોલેન્ટિયર)",
        "Porbandar District, Gujarat": "પોરબંદર જિલ્લો, ગુજરાત",
        "Card Issued Dt.": "કાર્ડ ઈશ્યુ તારીખ",
        "Validity Dt.": "માન્યતા તારીખ",
        "Assigned to indigent citizens by DLSA Secretary": "ડીએલએસએ સેક્રેટરીશ્રી દ્વારા નાગરિકોને ફાળવવામાં આવે છે",
        "Chairman, DLSA Porbandar": "ચેરમેનશ્રી, ડીએલએસએ પોરબંદર",
        "PLV Signature": "પીએલવી સહી",
        "Close": "બંધ કરો",
        "Assigned Center:": "ફાળવેલ કેન્દ્ર:",

        // Schemes Page
        "Legal Services & Welfare Schemes": "કાનૂની સેવાઓ અને કલ્યાણકારી યોજનાઓ",
        "Statutory NALSA & DLSA schemes ensuring protection, legal defense, and rehabilitation": "સંરક્ષણ, કાનૂની બચાવ અને પુનર્વસન સુનિશ્ચિત કરતી કાયદાકીય નાલસા (NALSA) અને ડીએલએસએ યોજનાઓ",
        "Explore Public Schemes": "જાહેર કલ્યાણ યોજનાઓ શોધો",
        "Type keywords to filter schemes by target group, legal benefit, or category": "લક્ષિત જૂથ, કાનૂની લાભ અથવા શ્રેણી અનુસાર યોજનાઓ ફિલ્ટર કરવા કીવર્ડ્સ લખો",
        "Objectives & Legal Mandate": "ઉદ્દેશ્યો અને કાનૂની આદેશ",
        "Eligibility Criteria": "પાત્રતાના માપદંડ",
        "Benefits & Assistance": "લાભ અને મળવાપાત્ર સહાય",
        "Required Documents": "જરૂરી દસ્તાવેજો",
        "Application Process": "અરજી કરવાની પ્રક્રિયા",
        "Apply for Scheme Benefits": "આ યોજના હેઠળ સહાય મેળવવા અરજી કરો",
        "Nodal Officer:": "નોડલ અધિકારી:",

        // Footer
        "Navigation": "મુખ્ય મેનુ",
        "Rank & Officers": "ન્યાયિક પદ અને અધિકારીઓ",
        "Clinics & Centers": "ક્લિનિક્સ & કેન્દ્રો",
        "Welfare Schemes": "કલ્યાણકારી યોજનાઓ",
        "Apply Online": "ઓનલાઇન અરજી",
        "Official Portals": "સત્તાવાર સરકારી પોર્ટલ્સ",
        "Technology & Architecture": "સિસ્ટમ આર્કિટેક્ચર",
        "Architecture Stack": "ટેકનોલોજી સ્ટેક",
        "All Rights Reserved.": "સર્વાધિકાર સુરક્ષિત.",
        "Designed for Porbandar Public Legal Literacy & Citizen Assistance.": "પોરબંદર લોક કાનૂની જાગૃતિ અને નાગરિક સહાય માટે નિર્મિત.",

        // Application Form & Tracking
        "Apply for 100% Free Legal Aid": "૧૦૦% મફત કાનૂની સહાય માટે અરજી",
        "Applicant Full Name": "અરજદારનું પૂરું નામ",
        "Gender": "જાતિ / લિંગ",
        "Mobile Number": "મોબાઇલ નંબર",
        "Email Address (Optional)": "ઇમેઇલ એડ્રેસ (જો હોય તો)",
        "Identity Proof Type": "ઓળખના પુરાવાનો પ્રકાર",
        "ID Proof Number": "ઓળખ પુરાવા નંબર",
        "Residential Address (in Porbandar District)": "રહેઠાણનું સરનામું (પોરબંદર જિલ્લો)",
        "Section 12 Entitlement Category": "કલમ ૧૨ મફત સહાય પાત્રતા શ્રેણી",
        "Annual Family Income": "વાર્ષિક કૌટુંબિક આવક",
        "Type of Legal Matter / Case": "કાનૂની કેસનો પ્રકાર",
        "Court / Police Jurisdiction": "અદાલત / પોલીસ અધિકારક્ષેત્ર",
        "Summary of Legal Problem": "કાનૂની સમસ્યાનો ટૂંકસાર",
        "Submit Application for Free Legal Aid": "મફત કાનૂની સહાય મેળવવા અરજી સબમિટ કરો",
        "Track Legal Aid Application Status": "કાનૂની સહાય અરજીની સ્થિતિ તપાસો",
        "Track Application": "સ્થિતિ તપાસો",
        "Application Tracking Details": "અરજી સ્થિતિ અને વિગતો",
        "Application Details": "અરજીની વિગતો",
        "Current Status:": "હાલની સ્થિતિ:",
        "Assigned Counsel:": "ફાળવેલ સરકારી વકીલશ્રી:",
        "Counsel Contact:": "વકીલશ્રીનો સંપર્ક નંબર:",
        "Official DLSA SMS Updates Sent to Registered Mobile": "નોંધાયેલ મોબાઇલ પર મોકલેલ સત્તાવાર એસએમએસ"
    };

    // ------------------------------------------------------------------------
    // Dynamic Text Replacement Engine via TreeWalker (Preserves Icons & HTML)
    // ------------------------------------------------------------------------
    function walkAndTranslateTextNodes(root) {
        if (!root) return;
        const walker = document.createTreeWalker(
            root,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function (node) {
                    if (!node || !node.nodeValue) return NodeFilter.FILTER_REJECT;
                    const parent = node.parentElement;
                    if (!parent) return NodeFilter.FILTER_REJECT;
                    const tag = parent.tagName.toUpperCase();
                    if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT' || tag === 'CODE') {
                        return NodeFilter.FILTER_REJECT;
                    }
                    if (node.nodeValue.trim().length === 0) return NodeFilter.FILTER_REJECT;
                    return NodeFilter.FILTER_ACCEPT;
                }
            },
            false
        );

        const nodes = [];
        while (walker.nextNode()) {
            nodes.push(walker.currentNode);
        }

        nodes.forEach(node => {
            const raw = node.nodeValue;
            const trimmed = raw.trim();
            if (!trimmed) return;

            // 1. Direct match
            if (DLSA_TRANSLATIONS[trimmed]) {
                if (node._dlsaOrig === undefined) node._dlsaOrig = raw;
                node.nodeValue = raw.replace(trimmed, DLSA_TRANSLATIONS[trimmed]);
                return;
            }

            // 2. Pattern: "All Locations (X)"
            const allLocMatch = trimmed.match(/^All Locations\s*(\(\d+\))?$/i);
            if (allLocMatch) {
                if (node._dlsaOrig === undefined) node._dlsaOrig = raw;
                node.nodeValue = raw.replace(trimmed, 'તમામ સ્થાનો ' + (allLocMatch[1] || ''));
                return;
            }

            // 3. Pattern: "Certified PLVs Directory (X)"
            const dirMatch = trimmed.match(/^Certified PLVs Directory\s*(\(\d+\))?$/i);
            if (dirMatch) {
                if (node._dlsaOrig === undefined) node._dlsaOrig = raw;
                node.nodeValue = raw.replace(trimmed, 'પ્રમાણિત પીએલવી ડિરેક્ટરી ' + (dirMatch[1] || ''));
                return;
            }

            // 4. Prefixes
            if (trimmed.startsWith('Assigned Center:')) {
                if (node._dlsaOrig === undefined) node._dlsaOrig = raw;
                node.nodeValue = raw.replace('Assigned Center:', 'ફાળવેલ કેન્દ્ર:');
                return;
            }
            if (trimmed.startsWith('Jurisdiction:')) {
                if (node._dlsaOrig === undefined) node._dlsaOrig = raw;
                node.nodeValue = raw.replace('Jurisdiction:', 'અધિકારક્ષેત્ર:');
                return;
            }
            if (trimmed.startsWith('In-charge:')) {
                if (node._dlsaOrig === undefined) node._dlsaOrig = raw;
                node.nodeValue = raw.replace('In-charge:', 'ઇન્ચાર્જ:');
                return;
            }
            if (trimmed.startsWith('Helpline:')) {
                if (node._dlsaOrig === undefined) node._dlsaOrig = raw;
                node.nodeValue = raw.replace('Helpline:', 'હેલ્પલાઇન:');
                return;
            }
            if (trimmed.startsWith('DLSA Sr. No. :') || trimmed.startsWith('DLSA Sr. No.:')) {
                if (node._dlsaOrig === undefined) node._dlsaOrig = raw;
                node.nodeValue = raw.replace(/DLSA Sr\. No\.\s*:/, 'ડીએલએસએ ક્રમ નં. :');
                return;
            }
            if (trimmed.startsWith('Card Issued:') || trimmed.includes('Valid Upto:')) {
                if (node._dlsaOrig === undefined) node._dlsaOrig = raw;
                node.nodeValue = raw.replace('Card Issued:', 'કાર્ડ તારીખ:').replace('Valid Upto:', 'માન્યતા:');
                return;
            }

            // 5. Look for multi-word phrase replacements within text
            for (const [enKey, guVal] of Object.entries(DLSA_TRANSLATIONS)) {
                if (enKey.length >= 6 && raw.includes(enKey)) {
                    if (node._dlsaOrig === undefined) node._dlsaOrig = raw;
                    node.nodeValue = node.nodeValue.replaceAll(enKey, guVal);
                }
            }
        });
    }

    function translateInputsAndOptions() {
        document.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(inp => {
            const ph = inp.getAttribute('placeholder') || '';
            if (!inp.getAttribute('data-original-ph')) inp.setAttribute('data-original-ph', ph);
            for (const [enKey, guVal] of Object.entries(DLSA_TRANSLATIONS)) {
                if (ph.includes(enKey)) {
                    inp.setAttribute('placeholder', ph.replaceAll(enKey, guVal));
                    break;
                }
            }
        });

        document.querySelectorAll('select option').forEach(opt => {
            const text = opt.textContent.trim();
            if (!opt.getAttribute('data-original-opt')) opt.setAttribute('data-original-opt', text);
            if (DLSA_TRANSLATIONS[text]) {
                opt.textContent = DLSA_TRANSLATIONS[text];
            }
        });
    }

    function translatePageToGujarati() {
        document.documentElement.lang = 'gu';
        walkAndTranslateTextNodes(document.body);
        translateInputsAndOptions();
    }

    function restorePageToEnglish() {
        document.documentElement.lang = 'en';
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );
        while (walker.nextNode()) {
            const node = walker.currentNode;
            if (node._dlsaOrig !== undefined) {
                node.nodeValue = node._dlsaOrig;
            }
        }
        document.querySelectorAll('input[data-original-ph], textarea[data-original-ph]').forEach(inp => {
            inp.setAttribute('placeholder', inp.getAttribute('data-original-ph'));
        });
        document.querySelectorAll('option[data-original-opt]').forEach(opt => {
            opt.textContent = opt.getAttribute('data-original-opt');
        });
    }

    // Auto-detect Language on load
    const cookieLang = (document.cookie.match(/dlsa_lang=([^;]+)/) || [])[1];
    const activeLang = document.documentElement.lang || cookieLang || localStorage.getItem('dlsa_lang') || 'en';
    if (activeLang === 'gu') {
        translatePageToGujarati();
    }

    // Language Toggle Click Handlers
    document.querySelectorAll('.lang-switch-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const selected = this.getAttribute('data-lang');
            localStorage.setItem('dlsa_lang', selected);
            document.cookie = `dlsa_lang=${selected};path=/;max-age=31536000`;
            document.cookie = `googtrans=/en/${selected};path=/;max-age=31536000`;
            if (selected === 'gu') {
                translatePageToGujarati();
            } else {
                restorePageToEnglish();
            }
        });
    });

    // ------------------------------------------------------------------------
    // 2. Tooltips initialization
    // ------------------------------------------------------------------------
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ------------------------------------------------------------------------
    // 3. PLV Live Search & Filter (Name, Status, Gender)
    // ------------------------------------------------------------------------
    const plvSearchInput = document.getElementById('plvSearchInput');
    const plvStatusFilter = document.getElementById('plvStatusFilter');
    const plvGenderFilter = document.getElementById('plvGenderFilter');
    const plvCards = document.querySelectorAll('.plv-item');

    function filterPLVs() {
        if (!plvCards.length) return;
        const query = (plvSearchInput ? plvSearchInput.value.toLowerCase().trim() : '');
        const status = (plvStatusFilter ? plvStatusFilter.value : 'all');
        const gender = (plvGenderFilter ? plvGenderFilter.value : 'all');

        plvCards.forEach(card => {
            const name = card.getAttribute('data-name')?.toLowerCase() || '';
            const location = card.getAttribute('data-location')?.toLowerCase() || '';
            const cardStatus = card.getAttribute('data-status') || '';
            const cardGender = card.getAttribute('data-gender') || '';

            const matchesQuery = !query || name.includes(query) || location.includes(query);
            const matchesStatus = (status === 'all') || (cardStatus === status);
            const matchesGender = (gender === 'all') || (cardGender.toLowerCase() === gender.toLowerCase());

            if (matchesQuery && matchesStatus && matchesGender) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    if (plvSearchInput) plvSearchInput.addEventListener('input', filterPLVs);
    if (plvStatusFilter) plvStatusFilter.addEventListener('change', filterPLVs);
    if (plvGenderFilter) plvGenderFilter.addEventListener('change', filterPLVs);

    // ------------------------------------------------------------------------
    // 4. Deployment Location Filters & Search
    // ------------------------------------------------------------------------
    const deploymentButtons = document.querySelectorAll('.deployment-filter-btn');
    const deploymentCards = document.querySelectorAll('.deployment-item');
    const deploymentSearchInput = document.getElementById('deploymentSearchInput');

    function filterDeployments() {
        if (!deploymentCards.length) return;
        const activeBtn = document.querySelector('.deployment-filter-btn.active');
        const filter = activeBtn ? activeBtn.getAttribute('data-filter') : 'all';
        const query = (deploymentSearchInput ? deploymentSearchInput.value.toLowerCase().trim() : '');

        deploymentCards.forEach(card => {
            const type = card.getAttribute('data-type');
            const searchData = (card.getAttribute('data-search') || card.innerText).toLowerCase();

            const matchesFilter = (filter === 'all' || type === filter);
            const matchesQuery = !query || searchData.includes(query);

            if (matchesFilter && matchesQuery) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    if (deploymentButtons.length && deploymentCards.length) {
        deploymentButtons.forEach(btn => {
            btn.addEventListener('click', function () {
                deploymentButtons.forEach(b => b.classList.remove('active', 'btn-primary'));
                deploymentButtons.forEach(b => b.classList.add('btn-outline-primary'));
                this.classList.remove('btn-outline-primary');
                this.classList.add('active', 'btn-primary');
                filterDeployments();
            });
        });
    }

    if (deploymentSearchInput) {
        deploymentSearchInput.addEventListener('input', filterDeployments);
    }

    // ------------------------------------------------------------------------
    // 5. Scheme Live Search
    // ------------------------------------------------------------------------
    const schemeSearchInput = document.getElementById('schemeSearchInput');
    const schemeCards = document.querySelectorAll('.scheme-item');

    if (schemeSearchInput && schemeCards.length) {
        schemeSearchInput.addEventListener('input', function () {
            const q = this.value.toLowerCase().trim();
            schemeCards.forEach(card => {
                const title = card.getAttribute('data-title')?.toLowerCase() || '';
                const target = card.getAttribute('data-target')?.toLowerCase() || '';
                const desc = card.innerText.toLowerCase();

                if (!q || title.includes(q) || target.includes(q) || desc.includes(q)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // ------------------------------------------------------------------------
    // 6. Section 12 Eligibility Quick Checker Modal/Widget
    // ------------------------------------------------------------------------
    const checkEligibleBtn = document.getElementById('btnRunEligibilityCheck');
    if (checkEligibleBtn) {
        checkEligibleBtn.addEventListener('click', function () {
            const isWomanOrChild = document.getElementById('chkWomanChild')?.checked;
            const isSCST = document.getElementById('chkSCST')?.checked;
            const isInCustody = document.getElementById('chkCustody')?.checked;
            const isWorkman = document.getElementById('chkWorkman')?.checked;
            const isDisabled = document.getElementById('chkDisabled')?.checked;
            const income = parseFloat(document.getElementById('checkIncome')?.value || '0');

            const resultDiv = document.getElementById('eligibilityResult');
            if (!resultDiv) return;

            const isGu = (document.documentElement.lang === 'gu');

            if (isWomanOrChild || isSCST || isInCustody || isWorkman || isDisabled || (income > 0 && income <= 300000)) {
                resultDiv.className = 'alert alert-success d-flex align-items-center mt-3';
                resultDiv.innerHTML = `
                    <i class="bi bi-check-circle-fill fs-3 me-3 text-success"></i>
                    <div>
                        <strong>${isGu ? 'તમે ૧૦૦% મફત કાનૂની સહાય મેળવવા માટે સંપૂર્ણ પાત્ર છો!' : 'You are Fully Eligible for 100% Free Legal Aid!'}</strong>
                        <div class="small mt-1">${isGu ? 'કાનૂની સેવા સત્તા મંડળ અધિનિયમ, ૧૯૮૭ ની કલમ ૧૨ હેઠળ તમે મફત સરકારી વકીલ, મફત અરજી ડ્રાફ્ટિંગ અને પીએલવી સહાય મેળવવા હકદાર છો.' : 'Under Section 12 of the Legal Services Authorities Act, 1987, you qualify for free court counsel, free drafting, court fee exemptions, and dedicated PLV support.'}</div>
                        <a href="/apply" class="btn btn-sm btn-success mt-2 fw-semibold">${isGu ? 'ઓનલાઇન અરજી કરો &rarr;' : 'Proceed to Apply Online &rarr;'}</a>
                    </div>
                `;
            } else if (income > 300000) {
                resultDiv.className = 'alert alert-warning d-flex align-items-center mt-3';
                resultDiv.innerHTML = `
                    <i class="bi bi-info-circle-fill fs-3 me-3 text-warning"></i>
                    <div>
                        <strong>${isGu ? 'આવક મર્યાદા વધારે છે, પરંતુ વિશેષ અપવાદ લાગુ પડી શકે છે!' : 'Income Exceeds Standard Threshold, but Exceptions Apply!'}</strong>
                        <div class="small mt-1">${isGu ? 'માનવ તસ્કરી, આપત્તિ સહાય, જેલ કસ્ટડી અથવા ઘરેલુ હિંસા સંબંધિત બાબતોમાં આવક મર્યાદા ધ્યાને લેવાતી નથી. સીધા મૂલ્યાંકન માટે ડીએલએસએ ફ્રન્ટ ઓફિસનો સંપર્ક કરો.' : 'If your matter involves human trafficking, disaster relief, custody, or domestic violence, income ceilings do not disqualify you. Please visit our Front Office for direct evaluation.'}</div>
                    </div>
                `;
            } else {
                resultDiv.className = 'alert alert-secondary mt-3';
                resultDiv.innerHTML = isGu ? 'કૃપા કરીને ઓછામાં ઓછી એક કેટેગરી પસંદ કરો અથવા તમારી વાર્ષિક આવક દાખલ કરો.' : 'Please select at least one category or enter your annual income to check eligibility.';
            }
        });
    }

    // ------------------------------------------------------------------------
    // 7. Mobile Navbar Floating Menu Auto-Close on Outside Click or Link Tap
    // ------------------------------------------------------------------------
    const navbarCollapse = document.getElementById('navbarMain');
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarCollapse && navbarToggler) {
        document.addEventListener('click', function (event) {
            const isInside = navbarCollapse.contains(event.target) || navbarToggler.contains(event.target);
            if (!isInside && navbarCollapse.classList.contains('show')) {
                const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse) || new bootstrap.Collapse(navbarCollapse, { toggle: false });
                bsCollapse.hide();
            }
        });

        navbarCollapse.querySelectorAll('.nav-link, .btn:not(.lang-switch-btn)').forEach(link => {
            link.addEventListener('click', function () {
                if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                    const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse) || new bootstrap.Collapse(navbarCollapse, { toggle: false });
                    bsCollapse.hide();
                }
            });
        });
    }
});
