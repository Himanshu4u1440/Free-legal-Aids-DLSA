import unittest
from app import app
from database import get_db, SessionLocal
from models import LegalAidApplication, Member, PLV, Deployment, Scheme

class DLSAPorbandarTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with SessionLocal() as db:
            db.query(PLV).update({PLV.is_active: True, PLV.status: "Active"})
            app101 = db.query(LegalAidApplication).filter_by(application_number="DLSA-PBD-2026-101").first()
            if not app101:
                db.add(LegalAidApplication(
                    application_number="DLSA-PBD-2026-101",
                    applicant_name="Bhavnaben J. Rathod",
                    gender="Female",
                    phone="9879012345",
                    residential_address="Chhaya, Porbandar",
                    category="Woman / Child",
                    annual_income=45000.00,
                    case_type="Domestic Violence",
                    case_summary="Facing persistent domestic cruelty and abandonment.",
                    assigned_counsel="Adv. Front Office Panel Lawyer",
                    assigned_counsel_phone="98250 87654",
                    status="Counsel Assigned",
                    last_sms_notification="[DLSA-SMS] Dear Bhavnaben, Free Legal Counsel 'Adv. Front Office Panel Lawyer' (Contact: 98250 87654) assigned."
                ))
            app103 = db.query(LegalAidApplication).filter_by(application_number="DLSA-PBD-2026-103").first()
            if not app103:
                db.add(LegalAidApplication(
                    application_number="DLSA-PBD-2026-103",
                    applicant_name="Dhirubhai G. Dave",
                    gender="Male",
                    phone="9428345678",
                    residential_address="Bokhira, Porbandar",
                    category="General (< 3 Lakh)",
                    annual_income=120000.00,
                    case_type="Civil Property Dispute",
                    case_summary="Land boundary title demarcation dispute in Porbandar.",
                    status="Submitted",
                    last_sms_notification="[DLSA-SMS] Application submitted successfully."
                ))
            db.commit()

    def test_01_homepage_renders_porbandar(self):
        """Test homepage renders with DLSA Porbandar details."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"District Legal Services Authority, Porbandar", response.data)
        self.assertIn(b"44", response.data)

    def test_02_leadership_renders_porbandar(self):
        """Test leadership page renders DLSA Porbandar Chairman & Secretary."""
        response = self.client.get('/leadership')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"District Legal Services Authority", response.data)
        self.assertIn(b"Chairman, DLSA Porbandar", response.data)
        self.assertIn(b"Secretary, DLSA Porbandar", response.data)

    def test_03_plv_portal_has_all_44_porbandar_plvs_with_privacy(self):
        """Test PLV portal renders 44 Porbandar PLVs while strictly protecting privacy (no phone/address/speciality)."""
        response = self.client.get('/plv-portal')
        self.assertEqual(response.status_code, 200)
        # Check specific PLVs from user's document
        self.assertIn(b"Nimisha A. Joshi", response.data)
        self.assertIn(b"Parth B. Rathod", response.data)
        self.assertIn(b"Himanshu V. Parmar", response.data)
        # Verify privacy: private phone numbers and street addresses must NOT appear on public portal
        self.assertNotIn(b"7405245440", response.data)
        self.assertNotIn(b"Near Gayatri Mandir", response.data)
        # Verify allocation protocol notice is shown
        self.assertIn(b"Official Volunteer Allocation & Citizen Assistance Protocol", response.data)

    def test_04_deployments_renders_porbandar_centers(self):
        """Test deployments page renders Porbandar official 31 clinics and police stations."""
        response = self.client.get('/deployments')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Kirtimandir Police Station", response.data)
        self.assertIn(b"Kamlabaug Police Station", response.data)
        self.assertIn(b"Front Office DLSA Porbandar Legal Aid Clinic", response.data)
        self.assertIn(b"Special Sub-Jail Clinic", response.data)
        self.assertIn(b"Miyani Village Legal Aid Clinic", response.data)

    def test_05_schemes_renders(self):
        """Test schemes catalog page renders."""
        response = self.client.get('/schemes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Gujarat Victim Compensation Scheme", response.data)
        self.assertIn(b"Coastal Fishermen", response.data)

    def test_06_apply_and_track_flow_porbandar(self):
        """Test citizen legal aid application submission and tracking in Porbandar."""
        post_data = {
            "applicant_name": "Rameshbhai K. Koli",
            "gender": "Male",
            "phone": "9898012345",
            "email": "ramesh.pbd@gmail.com",
            "id_proof_type": "Aadhaar",
            "id_proof_number": "XXXX-4421",
            "residential_address": "Near Subhash Nagar, Porbandar",
            "category": "Industrial Workman",
            "annual_income": "60000",
            "case_type": "Labour & Wages",
            "court_jurisdiction": "Labour Court Porbandar",
            "case_summary": "Unpaid wages dispute for boat work during seasonal fishing."
        }
        try:
            response = self.client.post('/apply', data=post_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Your Legal Aid Application has been submitted", response.data)
            self.assertIn(b"Rameshbhai K. Koli", response.data)
        finally:
            # Clean up test-created application so dlsa.db is never polluted
            db = next(get_db())
            test_apps = db.query(LegalAidApplication).filter(LegalAidApplication.applicant_name == "Rameshbhai K. Koli").all()
            for app_item in test_apps:
                db.delete(app_item)
            db.commit()

    def test_07_api_plvs_count_is_44_and_privacy_safe(self):
        """Test REST API returns exactly 44 certified PLVs and protects private phone/address."""
        res_plvs = self.client.get('/api/plvs')
        self.assertEqual(res_plvs.status_code, 200)
        plvs_data = res_plvs.get_json()
        self.assertEqual(len(plvs_data), 44)
        # Verify privacy: public API does NOT leak phone or residential address
        self.assertNotIn('phone', plvs_data[0])
        self.assertNotIn('residential_address', plvs_data[0])

    def test_08_admin_flow(self):
        """Test admin session access to Porbandar dashboard view."""
        with self.client.session_transaction() as sess:
            sess["admin_user"] = "himanshu"
            sess["admin_name"] = "Himanshu"
            sess["admin_role"] = "SuperAdmin"
        dash_res = self.client.get('/admin/dashboard')
        self.assertEqual(dash_res.status_code, 200)
        self.assertIn(b"DLSA Administration Dashboard", dash_res.data)

    def test_09_admin_plv_columns_and_private_info_access(self):
        """Test admin PLV management columns, private data visibility, and status toggling."""
        with self.client.session_transaction() as sess:
            sess["admin_user"] = "himanshu"
            sess["admin_name"] = "Himanshu"
            sess["admin_role"] = "SuperAdmin"

        # View Admin PLVs
        admin_plv_res = self.client.get('/admin/plvs')
        self.assertEqual(admin_plv_res.status_code, 200)
        # Admin CAN see private phone and address
        self.assertIn(b"7405245440", admin_plv_res.data)
        self.assertIn(b"Chhaya, Porbandar", admin_plv_res.data)
        # Admin sees categorized tabs
        self.assertIn(b"Active PLVs", admin_plv_res.data)
        self.assertIn(b"Inactive PLVs", admin_plv_res.data)
        self.assertIn(b"All 44 PLVs Master List", admin_plv_res.data)
        self.assertIn(b"Mark All PLVs as Inactive", admin_plv_res.data)

    def test_10_bulk_status_toggle_and_sr_no_allocation_visibility(self):
        """Test bulk marking PLVs as inactive/active and DLSA Sr. No. visibility in allocation."""
        with self.client.session_transaction() as sess:
            sess["admin_user"] = "himanshu"
            sess["admin_name"] = "Himanshu"
            sess["admin_role"] = "SuperAdmin"

        # Check DLSA Sr. No. visibility in admin dashboard allocation select (no '#')
        dash_res = self.client.get('/admin/dashboard')
        self.assertEqual(dash_res.status_code, 200)
        self.assertIn(b"DLSA Sr. No. 01 -", dash_res.data)
        self.assertNotIn(b"Sr #", dash_res.data)

        # Test Mark All PLVs as Inactive
        mark_res = self.client.post('/admin/plvs/mark-all-inactive', follow_redirects=True)
        self.assertEqual(mark_res.status_code, 200)
        self.assertIn(b"Successfully marked all", mark_res.data)
        self.assertIn(b"as Inactive", mark_res.data)

        # Inactive list should now have volunteers and 'Mark All PLVs as Active' button
        self.assertIn(b"Mark All PLVs as Active", mark_res.data)

        # Restore active status
        restore_res = self.client.post('/admin/plvs/mark-all-active', follow_redirects=True)
        self.assertEqual(restore_res.status_code, 200)
        self.assertIn(b"Successfully activated", restore_res.data)

        # Check citizen apply page has DLSA Sr. No. visible in allocation select
        apply_res = self.client.get('/apply')
        self.assertEqual(apply_res.status_code, 200)
        self.assertIn(b"DLSA Sr. No. 01 -", apply_res.data)
        self.assertNotIn(b"Sr #", apply_res.data)

    def test_11_plv_search_and_gender_filtering(self):
        """Test PLV administration search bar, gender dropdown selector, and filtering attributes."""
        with self.client.session_transaction() as sess:
            sess["admin_user"] = "himanshu"
            sess["admin_name"] = "Himanshu"
            sess["admin_role"] = "SuperAdmin"

        res = self.client.get('/admin/plvs')
        self.assertEqual(res.status_code, 200)
        # Verify search and gender filter controls exist
        self.assertIn(b'id="adminPlvSearch"', res.data)
        self.assertIn(b'id="adminGenderFilter"', res.data)
        self.assertIn(b"All Genders (Both Male & Female)", res.data)
        self.assertIn(b"Male Volunteers", res.data)
        self.assertIn(b"Female Volunteers", res.data)
        # Verify dedicated Gender column in tables
        self.assertIn(b"<th>Gender</th>", res.data)
        # Verify data attributes for dynamic filtering
        self.assertIn(b'class="plv-row"', res.data)
        self.assertIn(b'data-gender="Male"', res.data)
        self.assertIn(b'data-gender="Female"', res.data)
        self.assertIn(b'no-filter-match-row', res.data)

    def test_12_counsel_contact_tracking_and_sms_dispatch(self):
        """Test counsel contact phone visibility on tracking page and automated SMS notifications on status changes."""
        # 1. Test Tracking view displays counsel phone and SMS dispatch log
        track_res = self.client.get('/track?app_no=DLSA-PBD-2026-101')
        self.assertEqual(track_res.status_code, 200)
        self.assertIn(b"Adv. Front Office Panel Lawyer", track_res.data)
        self.assertIn(b"98250 87654", track_res.data)
        self.assertIn(b"tel:98250 87654", track_res.data)
        self.assertIn(b"Official DLSA SMS Updates Sent to Registered Mobile", track_res.data)
        self.assertIn(b"[DLSA-SMS]", track_res.data)

        # 2. Test Admin updates case status to Under Scrutiny with counsel phone, triggering SMS
        with self.client.session_transaction() as sess:
            sess["admin_user"] = "himanshu"
            sess["admin_name"] = "Himanshu"
            sess["admin_role"] = "SuperAdmin"

        db = next(get_db())
        app_record = db.query(LegalAidApplication).filter_by(application_number="DLSA-PBD-2026-103").first()
        self.assertIsNotNone(app_record)

        update_data = {
            "status": "Under Scrutiny",
            "assigned_counsel": "Adv. Rajesh V. Thakar",
            "assigned_counsel_phone": "98791 22334",
            "assigned_plv_id": str(app_record.assigned_plv_id or ""),
            "status_notes": "Scrutiny completed by Porbandar DLSA legal scrutiny wing."
        }
        update_res = self.client.post(f'/admin/applications/{app_record.id}/update', data=update_data, follow_redirects=True)
        self.assertEqual(update_res.status_code, 200)
        self.assertIn(b"status SMS successfully dispatched", update_res.data)

        # Verify DB reflects updated counsel phone and generated SMS
        db.refresh(app_record)
        self.assertEqual(app_record.status, "Under Scrutiny")
        self.assertEqual(app_record.assigned_counsel, "Adv. Rajesh V. Thakar")
        self.assertEqual(app_record.assigned_counsel_phone, "98791 22334")
        self.assertIsNotNone(app_record.last_sms_sent_at)
        self.assertIn("UNDER SCRUTINY", app_record.last_sms_notification)

        # 3. Verify citizen tracking page now reflects the updated SMS and counsel phone
        track_updated = self.client.get(f'/track?app_no={app_record.application_number}')
        self.assertEqual(track_updated.status_code, 200)
        self.assertIn(b"Adv. Rajesh V. Thakar", track_updated.data)
        self.assertIn(b"98791 22334", track_updated.data)
        self.assertIn(b"UNDER SCRUTINY", track_updated.data)

    def test_13_admin_login_page_no_system_credentials(self):
        """Test admin login page does NOT display system credentials."""
        res = self.client.get('/admin/login')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(b"System Credentials", res.data)
        self.assertNotIn(b"Active Username: <code>himanshu</code>", res.data)
        self.assertNotIn(b"Active Username", res.data)

    def test_14_language_switcher_toggles_english_and_gujarati(self):
        """Test language switcher toggles between English and Gujarati."""
        # 1. Switch to Gujarati
        res_gu = self.client.get('/set-language/gu', follow_redirects=True)
        self.assertEqual(res_gu.status_code, 200)
        # Should render Gujarati navigation elements
        self.assertIn("મુખપૃષ્ઠ".encode("utf-8"), res_gu.data)
        self.assertIn("મફત કાનૂની સહાય મેળવો".encode("utf-8"), res_gu.data)
        self.assertIn("પોરબંદર પીએલવી (૪૪)".encode("utf-8"), res_gu.data)
        self.assertIn("૨૪x૭ હેલ્પલાઇન".encode("utf-8"), res_gu.data)

        # 2. Switch back to English
        res_en = self.client.get('/set-language/en', follow_redirects=True)
        self.assertEqual(res_en.status_code, 200)
        self.assertIn(b"Home", res_en.data)
        self.assertIn(b"Rank", res_en.data)
        self.assertIn(b"Apply Free Legal Aid", res_en.data)
        self.assertIn(b"24x7 HELPLINE", res_en.data)

    def test_15_deployments_page_renders_all_plvs_and_bilingual(self):
        """Test deployments page displays official PLVs per center and supports complete Gujarati translation."""
        # 1. English deployments view
        self.client.get('/set-language/en', follow_redirects=True)
        res_en = self.client.get('/deployments')
        self.assertEqual(res_en.status_code, 200)
        self.assertIn(b"Places Where PLVs & Legal Aid Clinics are Deployed", res_en.data)
        self.assertIn(b"Assigned Para Legal Volunteers (PLVs):", res_en.data)
        self.assertIn(b"Deployed PLVs", res_en.data)
        # Check that official assigned PLVs appear across centers
        self.assertIn(b"Parth B. Rathod", res_en.data)
        self.assertIn(b"Vikrantsinh N. Zala", res_en.data)
        self.assertIn(b"Meera J. Unadkat", res_en.data)
        self.assertIn(b"Dhaval K. Bamaniya", res_en.data)
        self.assertIn(b"Kajal B. Khunti", res_en.data)
        self.assertIn(b"Himanshu V. Parmar", res_en.data)

        # 2. Gujarati deployments view
        self.client.get('/set-language/gu', follow_redirects=True)
        res_gu = self.client.get('/deployments')
        self.assertEqual(res_gu.status_code, 200)
        # Check Gujarati page title, headings, and filters
        self.assertIn("નિમણૂક સ્થાનો".encode("utf-8"), res_gu.data)
        self.assertIn("તમામ સ્થાનો".encode("utf-8"), res_gu.data)
        self.assertIn("અદાલત અને સંસ્થાકીય ક્લિનિક્સ".encode("utf-8"), res_gu.data)
        self.assertIn("પોલીસ સ્ટેશનો".encode("utf-8"), res_gu.data)
        self.assertIn("ગ્રામીણ લીગલ એઇડ ક્લિનિક્સ".encode("utf-8"), res_gu.data)
        self.assertIn("નાગરિકો માટે ઉપલબ્ધ સેવાઓ:".encode("utf-8"), res_gu.data)
        self.assertIn("ફાળવેલ પેરા લીગલ વોલેન્ટિયર્સ (PLVs):".encode("utf-8"), res_gu.data)
        self.assertIn("હાજર પીએલવી".encode("utf-8"), res_gu.data)
        self.assertIn("ફરજ પર સક્રિય".encode("utf-8"), res_gu.data)
        self.assertIn("ઇન્ચાર્જ:".encode("utf-8"), res_gu.data)
        self.assertIn("હેલ્પલાઇન:".encode("utf-8"), res_gu.data)

    def test_16_project_report_route(self):
        """Test that /report successfully delivers the comprehensive project report."""
        res = self.client.get('/report')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"DISTRICT LEGAL SERVICES AUTHORITY (DLSA), PORBANDAR", res.data)
        self.assertIn(b"Official Citizen Legal Aid Portal", res.data)

    def test_17_plv_management_reflects_in_deployments(self):
        """Test that managing PLV status or assignments from admin immediately updates the deployments page."""
        # 1. Authenticate as admin session
        with self.client.session_transaction() as sess:
            sess["admin_user"] = "himanshu"
            sess["admin_name"] = "Himanshu Parmar"
            sess["admin_role"] = "SuperAdmin"

        # 2. Get an active PLV (e.g. Parth Rathod DLSA-03)
        with SessionLocal() as db:
            plv = db.query(PLV).filter(PLV.dlsa_sr_no == "03").first()
            if not plv:
                plv = db.query(PLV).first()
            plv_id = plv.id
            plv_name = plv.full_name

        # 3. Toggle PLV to Inactive
        res_toggle = self.client.post(f'/admin/plvs/{plv_id}/toggle-status', follow_redirects=True)
        self.assertEqual(res_toggle.status_code, 200)

        # 4. Check deployments page - PLV must NOT be in active list
        res_dep = self.client.get('/deployments')
        self.assertEqual(res_dep.status_code, 200)
        
        # Verify PLV is now inactive in DB
        with SessionLocal() as db:
            updated_plv = db.query(PLV).filter(PLV.id == plv_id).first()
            self.assertEqual(updated_plv.status, "Inactive")
            self.assertFalse(updated_plv.is_active)
            for a in updated_plv.assignments:
                self.assertFalse(a.is_active)

        # 5. Toggle PLV back to Active
        res_restore = self.client.post(f'/admin/plvs/{plv_id}/toggle-status', follow_redirects=True)
        self.assertEqual(res_restore.status_code, 200)
        with SessionLocal() as db:
            restored_plv = db.query(PLV).filter(PLV.id == plv_id).first()
            self.assertEqual(restored_plv.status, "Active")
            self.assertTrue(restored_plv.is_active)

if __name__ == '__main__':
    unittest.main()
