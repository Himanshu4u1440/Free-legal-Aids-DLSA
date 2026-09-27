import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "static", "images")
os.makedirs(ASSETS_DIR, exist_ok=True)

def generate_svg(filename, title, subtitle, bg_color, text_color="#FFFFFF"):
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <linearGradient id="grad_{filename.replace('.', '_')}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg_color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0f2b48;stop-opacity:1" />
    </linearGradient>
  </defs>
  <circle cx="100" cy="100" r="95" fill="url(#grad_{filename.replace('.', '_')})" stroke="#c59b27" stroke-width="5"/>
  <circle cx="100" cy="75" r="35" fill="{text_color}" opacity="0.9"/>
  <path d="M45,160 C45,120 155,120 155,160 Z" fill="{text_color}" opacity="0.9"/>
  <rect x="20" y="145" width="160" height="30" rx="6" fill="#0f2b48" opacity="0.9"/>
  <text x="100" y="165" font-family="Segoe UI, sans-serif" font-size="10.5" font-weight="bold" fill="#ffdf7a" text-anchor="middle">{subtitle}</text>
</svg>"""
    with open(os.path.join(ASSETS_DIR, filename), "w", encoding="utf-8") as f:
        f.write(svg_content)

def generate_initials_avatar(filename, initials, role_badge, bg_color):
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <linearGradient id="grad_{filename.replace('.', '_')}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg_color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0f2b48;stop-opacity:1" />
    </linearGradient>
  </defs>
  <circle cx="100" cy="100" r="95" fill="url(#grad_{filename.replace('.', '_')})" stroke="#c59b27" stroke-width="4"/>
  <text x="100" y="115" font-family="Segoe UI, sans-serif" font-size="52" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="1">{initials}</text>
  <rect x="25" y="148" width="150" height="28" rx="6" fill="#0f2b48" opacity="0.95"/>
  <text x="100" y="167" font-family="Segoe UI, sans-serif" font-size="10" font-weight="bold" fill="#ffdf7a" text-anchor="middle">{role_badge}</text>
</svg>"""
    with open(os.path.join(ASSETS_DIR, filename), "w", encoding="utf-8") as f:
        f.write(svg_content)

# Emblem SVG - DLSA Porbandar Gujarat
emblem_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" width="300" height="300">
  <circle cx="150" cy="150" r="140" fill="#0f2b48" stroke="#c59b27" stroke-width="8"/>
  <circle cx="150" cy="150" r="125" fill="#ffffff" stroke="#c59b27" stroke-width="2"/>
  
  <!-- Scales of Justice -->
  <line x1="150" y1="60" x2="150" y2="210" stroke="#0f2b48" stroke-width="6"/>
  <line x1="85" y1="95" x2="215" y2="95" stroke="#c59b27" stroke-width="6" stroke-linecap="round"/>
  <circle cx="150" cy="95" r="10" fill="#0f2b48"/>
  
  <!-- Left Pan -->
  <line x1="85" y1="95" x2="65" y2="145" stroke="#64748b" stroke-width="2"/>
  <line x1="85" y1="95" x2="105" y2="145" stroke="#64748b" stroke-width="2"/>
  <path d="M55,145 Q85,175 115,145 Z" fill="#c59b27" stroke="#0f2b48" stroke-width="2"/>
  
  <!-- Right Pan -->
  <line x1="215" y1="95" x2="195" y2="145" stroke="#64748b" stroke-width="2"/>
  <line x1="215" y1="95" x2="235" y2="145" stroke="#64748b" stroke-width="2"/>
  <path d="M185,145 Q215,175 245,145 Z" fill="#c59b27" stroke="#0f2b48" stroke-width="2"/>
  
  <!-- Pedestal -->
  <rect x="110" y="210" width="80" height="15" rx="4" fill="#0f2b48"/>
  <rect x="90" y="225" width="120" height="12" rx="4" fill="#c59b27"/>
  
  <!-- Outer Text -->
  <text x="150" y="46" font-family="Segoe UI, sans-serif" font-size="12" font-weight="800" fill="#0f2b48" text-anchor="middle" letter-spacing="1.5">DISTRICT LEGAL SERVICES AUTHORITY</text>
  <text x="150" y="258" font-family="Segoe UI, sans-serif" font-size="13" font-weight="800" fill="#0f2b48" text-anchor="middle" letter-spacing="2">PORBANDAR • GUJARAT</text>
  <text x="150" y="278" font-family="Segoe UI, sans-serif" font-size="10" font-weight="700" fill="#138808" text-anchor="middle">સર્વેષાં ન્યાયઃ • JUSTICE FOR ALL</text>
</svg>"""

with open(os.path.join(ASSETS_DIR, "emblem.svg"), "w", encoding="utf-8") as f:
    f.write(emblem_svg)

# Officials
generate_svg("chairman.svg", "Chairman", "PRINCIPAL DIST. JUDGE", "#1e3a8a")
generate_svg("secretary.svg", "Secretary", "SR CIVIL JUDGE / SECY", "#0d9488")
generate_svg("chief_ladc.svg", "Chief LADC", "CHIEF DEFENSE COUNSEL", "#b45309")
generate_svg("deputy_ladc.svg", "Deputy LADC", "DEPUTY DEFENSE COUNSEL", "#7c3aed")
generate_svg("panel_convener.svg", "Panel Convener", "PANEL ADVOCATE CONVENER", "#475569")
generate_svg("avatar_placeholder.svg", "Member", "DLSA OFFICIAL", "#64748b")
generate_svg("plv_m.svg", "PLV Male", "PLV • PORBANDAR", "#0284c7")
generate_svg("plv_f.svg", "PLV Female", "PLV • PORBANDAR", "#db2777")

# Porbandar PLV list
porbandar_plvs = [
    ("01", "Nimisha A. Joshi", "Female", "NJ", "#db2777"),
    ("03", "Parth B. Rathod", "Male", "PR", "#0284c7"),
    ("04", "Nidhi D. Mashru", "Female", "NM", "#9333ea"),
    ("05", "Tejal L. Gami", "Female", "TG", "#059669"),
    ("06", "Anjali N. Vaghela", "Female", "AV", "#d97706"),
    ("07", "Hetvi B. Dave", "Female", "HD", "#e11d48"),
    ("08", "Meera J. Unadkat", "Female", "MU", "#7c3aed"),
    ("09", "Vibhuti D. Pandavadadra", "Female", "VP", "#0891b2"),
    ("10", "Vikrantsinh N. Zala", "Male", "VZ", "#2563eb"),
    ("11", "Priti C. Rathod", "Female", "PR", "#c026d3"),
    ("13", "Keval B. Jora", "Male", "KJ", "#0d9488"),
    ("14", "Devendra B. Gareja", "Male", "DG", "#4f46e5"),
    ("16", "Manjula S. Chanpa", "Female", "MC", "#ea580c"),
    ("18", "Amir Mahmmad Ali", "Male", "AA", "#16a34a"),
    ("19", "Komal R. Jungi", "Female", "KJ", "#be185d"),
    ("21", "Heet H. Shingarakhiya", "Male", "HS", "#0284c7"),
    ("22", "Shivani M. Khiloshiya", "Female", "SK", "#a21caf"),
    ("24", "Arpita N. Parmar", "Female", "AP", "#b91c1c"),
    ("25", "Alpana H. Poriya", "Female", "AP", "#047857"),
    ("27", "Nikita S. Parmar", "Female", "NP", "#6d28d9"),
    ("28", "Divyeshkumar M. Jadav", "Male", "DJ", "#1d4ed8"),
    ("29", "Hasti V. Pandya", "Female", "HP", "#be123c"),
    ("30", "Muskan V. Cholera", "Female", "MC", "#9333ea"),
    ("31", "Kinjal R. Pandavadra", "Female", "KP", "#0f766e"),
    ("33", "Sonal J. Bamaniya", "Female", "SB", "#b45309"),
    ("34", "Dhaval K. Bamaniya", "Male", "DB", "#15803d"),
    ("35", "Chandrika R. Chanchiya", "Female", "CC", "#c2410c"),
    ("37", "Madhvi K. Shingrakhiya", "Female", "MS", "#7e22ce"),
    ("38", "Pooja B. Jebar", "Female", "PJ", "#be185d"),
    ("41", "Hina V. Toraniya", "Female", "HT", "#0369a1"),
    ("43", "Bharti D. Sida", "Female", "BS", "#0e7490"),
    ("44", "Himanshu V. Parmar", "Male", "HP", "#1e40af"),
    ("48", "Hemang R. Solanki", "Male", "HS", "#15803d"),
    ("49", "Aman A. Sadiya", "Male", "AS", "#0284c7"),
    ("50", "Payal R. Vaja", "Female", "PV", "#a21caf"),
    ("51", "Sanjana A. Baleja", "Female", "SB", "#b91c1c"),
    ("52", "Kamlesh R. Parmar", "Male", "KP", "#4338ca"),
    ("53", "Shruti D. Vaghela", "Female", "SV", "#d97706"),
    ("54", "Mahek B. Kothari", "Female", "MK", "#047857"),
    ("55", "Chetna G. Parmar", "Female", "CP", "#b45309"),
    ("57", "Jivan K. Chauhan", "Male", "JC", "#1d4ed8"),
    ("58", "Vrutika N. Kanabar", "Female", "VK", "#7e22ce"),
    ("59", "Rekha D. Dafda", "Female", "RD", "#be123c"),
    ("60", "Laxmi D. Gosai", "Female", "LG", "#0f766e"),
]

for sr_no, name, gender, initials, color in porbandar_plvs:
    badge = f"PLV • NO.{sr_no}"
    generate_initials_avatar(f"plv_pbd_{sr_no}.svg", initials, badge, color)

print(f"Generated DLSA Porbandar emblem and all {len(porbandar_plvs)} PLV visual identity assets successfully!")
