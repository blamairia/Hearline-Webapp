#!/usr/bin/env python3
"""
Demo Data Generator for Heartline Webapp
Creates realistic Algerian medical showcase data
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import app directly - it's defined in app.py at module level
from app import app
from models import db, Patient, Doctor, Visit, Appointment, Prescription, Medicament, User

# Algerian Names (Annaba region)
FIRST_NAMES_MALE = [
    "Ahmed", "Mohamed", "Karim", "Yassine", "Bilal", "Hamza", "Amine", 
    "Mehdi", "Rayan", "Sofiane", "Aymen", "Walid", "Rachid", "Farid", "Samir"
]

FIRST_NAMES_FEMALE = [
    "Amina", "Fatima", "Yasmine", "Sara", "Leila", "Nour", "Hanane",
    "Salma", "Khadija", "Asma", "Meriem", "Samia", "Houria", "Nawal", "Zohra"
]

LAST_NAMES = [
    "Benali", "Bouzid", "Cherif", "Djebbar", "Fekhar", "Gharbi", "Hamdi",
    "Khelifi", "Larbi", "Mansouri", "Nouri", "Rezki", "Saidi", "Toumi", "Zerrouki",
    "Bencheikh", "Boudiaf", "Chennaoui", "Dridi", "Ferhat", "Ghoul", "Hadj",
    "Khaldi", "Lounici", "Mahdi", "Naceur", "Rahmani", "Slimani", "Tebessi", "Ziani"
]

# Annaba addresses
ADDRESSES = [
    "Rue de la République, Centre-ville, Annaba",
    "Avenue de l'ALN, Sidi Amar, Annaba",
    "Cité 5 Juillet, El Bouni, Annaba",
    "Rue Zighoud Youcef, Annaba",
    "Boulevard du 1er Novembre, Annaba",
    "Cité Plaine Ouest, Annaba",
    "Rue des Frères Boumendjel, Annaba",
    "Avenue Didouche Mourad, Annaba",
    "Cité 20 Août, Annaba",
    "Rue Larbi Ben M'hidi, Annaba",
    "Boulevard de la Révolution, Annaba",
    "Cité AADL, El Hadjar, Annaba",
    "Rue Emir Abdelkader, Annaba",
    "Avenue Med Boudiaf, Annaba",
    "Cité des Fonctionnaires, Annaba"
]

# Medical conditions in French
MEDICAL_CONDITIONS = [
    "Hypertension artérielle contrôlée",
    "Diabète type 2 sous traitement",
    "Antécédents de troubles cardiaques",
    "Arythmie diagnostiquée",
    "Insuffisance cardiaque légère",
    "Angine de poitrine stable",
    "Fibrillation auriculaire",
    "Bloc auriculo-ventriculaire",
    "Tachycardie sinusale",
    "Bradycardie sinusale"
]

# Diagnosis texts in French
DIAGNOSES = [
    "Rythme sinusal normal, ECG sans particularité",
    "Fibrillation auriculaire détectée, traitement anticoagulant recommandé",
    "Bloc auriculo-ventriculaire du 1er degré",
    "Tachycardie supraventriculaire, surveillance recommandée",
    "Extrasystoles ventriculaires isolées",
    "Ischémie myocardique suspectée, examens complémentaires nécessaires",
    "Hypertrophie ventriculaire gauche",
    "Troubles de la repolarisation",
    "Bloc de branche gauche incomplet",
    "Signes d'infarctus ancien inférieur"
]

def create_demo_data():
    """Create comprehensive demo data"""
    
    with app.app_context():
        print("🏥 Heartline Demo Data Generator")
        print("=" * 50)
        
        # Check current status
        print("\n📊 Current Database Status:")
        print(f"   Patients: {Patient.query.count()}")
        print(f"   Doctors: {Doctor.query.count()}")
        print(f"   Users: {User.query.count()}")
        print(f"   Visits: {Visit.query.count()}")
        print(f"   Appointments: {Appointment.query.count()}")
        print(f"   Medicaments: {Medicament.query.count()}")
        
        # Check if we have medicaments
        med_count = Medicament.query.count()
        if med_count == 0:
            print("\n❌ No medicaments found in database!")
            print("   Please import the Algerian medication database first.")
            return
        
        print(f"\n✅ Found {med_count} medications in database")
        
        # Create doctors if needed
        print("\n👨‍⚕️ Creating Doctors...")
        doctors = []
        
        doctor_data = [
            ("Dr. Ahmed", "Benali", "Cardiologue", "+213 555 123 456", "a.benali@heartline.dz"),
            ("Dr. Fatima", "Bouzid", "Cardiologue", "+213 555 234 567", "f.bouzid@heartline.dz"),
            ("Dr. Karim", "Cherif", "Médecin Généraliste", "+213 555 345 678", "k.cherif@heartline.dz"),
        ]
        
        for fname, lname, spec, phone, email in doctor_data:
            existing = Doctor.query.filter_by(first_name=fname, last_name=lname).first()
            if not existing:
                doc = Doctor(
                    first_name=fname,
                    last_name=lname,
                    specialty=spec,
                    phone=phone,
                    email=email,
                    bio=f"Spécialiste en {spec} à Annaba avec 10+ années d'expérience"
                )
                db.session.add(doc)
                doctors.append(doc)
                print(f"   ✓ Created {fname} {lname} - {spec}")
            else:
                doctors.append(existing)
                print(f"   → {fname} {lname} already exists")
        
        db.session.commit()
        
        # Create users for doctors if needed
        print("\n👤 Creating User Accounts...")
        for doctor in doctors:
            existing_user = User.query.filter_by(email=doctor.email).first()
            if not existing_user:
                user = User(
                    username=doctor.email.split('@')[0],
                    email=doctor.email,
                    first_name=doctor.first_name,
                    last_name=doctor.last_name,
                    phone=doctor.phone,
                    role='doctor',
                    doctor_id=doctor.id
                )
                user.set_password('demo123')
                db.session.add(user)
                print(f"   ✓ Created user for {doctor.first_name} {doctor.last_name}")
        
        # Create assistant user
        assistant_exists = User.query.filter_by(username='assistant').first()
        if not assistant_exists:
            assistant = User(
                username='assistant',
                email='assistant@heartline.dz',
                first_name='Amina',
                last_name='Mansouri',
                phone='+213 555 999 888',
                role='assistant'
            )
            assistant.set_password('demo123')
            db.session.add(assistant)
            print("   ✓ Created assistant user")
            
        # Create admin user
        admin_exists = User.query.filter_by(username='admin').first()
        if not admin_exists:
            admin = User(
                username='admin',
                email='admin@heartline.dz',
                first_name='Admin',
                last_name='Administrator',
                role='doctor', # Admin usually has highest privilege, mapping to doctor for now or if role exists
                is_active=True
            )
            admin.set_password('admin')
            db.session.add(admin)
            print("   ✓ Created admin user (admin/admin)")

        
        db.session.commit()
        
        # Create patients
        print("\n👥 Creating Patients...")
        patients = []
        num_patients = 30
        
        for i in range(num_patients):
            gender = random.choice(["Male", "Female"])
            if gender == "Male":
                first_name = random.choice(FIRST_NAMES_MALE)
            else:
                first_name = random.choice(FIRST_NAMES_FEMALE)
            
            last_name = random.choice(LAST_NAMES)
            
            # Generate realistic birth dates (25-80 years old)
            age = random.randint(25, 80)
            birth_date = datetime.now() - timedelta(days=age*365 + random.randint(0, 365))
            
            # Generate unique email (SQL Server UNIQUE constraint doesn't allow multiple NULLs)
            email = f"{first_name.lower()}.{last_name.lower()}.{i}@heartline.dz"
            
            # Check if patient exists by name and birth date OR by email
            existing = None
            if email:
                existing = Patient.query.filter_by(email=email).first()
            if not existing:
                existing = Patient.query.filter_by(
                    first_name=first_name, 
                    last_name=last_name,
                    date_of_birth=birth_date.date()
                ).first()
            
            if not existing:
                patient = Patient(
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=birth_date.date(),
                    gender=gender,
                    address=random.choice(ADDRESSES),
                    phone=f"+213 {random.randint(550, 799)} {random.randint(100, 999)} {random.randint(100, 999)}",
                    email=email,
                    medical_history=random.choice(MEDICAL_CONDITIONS) if random.random() > 0.4 else None
                )
                db.session.add(patient)
                patients.append(patient)
                print(f"   ✓ Created patient {i+1}/{num_patients}: {first_name} {last_name}")
        
        db.session.commit()
        print(f"\n✅ Created {len(patients)} new patients")
        
        # Get all patients for visits
        all_patients = Patient.query.all()
        
        # Get some medications for prescriptions
        print("\n💊 Fetching medications...")
        medications = Medicament.query.limit(100).all()
        print(f"   ✓ Found {len(medications)} medications for prescriptions")
        
        # Create visits with varied dates
        print("\n🏥 Creating Visits...")
        visits_created = 0
        
        # Create visits spread over the last 6 months
        for patient in all_patients[:25]:  # Create visits for 25 patients
            # Each patient gets 1-4 visits
            num_visits = random.randint(1, 4)
            
            for v in range(num_visits):
                # Spread visits over last 180 days
                days_ago = random.randint(1, 180)
                visit_date = datetime.now() - timedelta(days=days_ago, hours=random.randint(8, 18))
                
                # Create visit
                visit = Visit(
                    patient_id=patient.id,
                    doctor_id=random.choice(doctors).id,
                    visit_date=visit_date,
                    diagnosis=random.choice(DIAGNOSES),
                    payment_total=random.choice([1500, 2000, 2500, 3000, 3500, 4000]),
                    payment_status=random.choice(['paid', 'paid', 'paid', 'partial', 'unpaid']),
                    payment_remaining=0 if random.random() > 0.3 else random.choice([500, 1000, 1500])
                )
                
                # Add follow-up date for some visits
                if random.random() > 0.6:
                    visit.follow_up_date = visit_date + timedelta(days=random.randint(7, 30))
                
                db.session.add(visit)
                db.session.flush()
                
                # Add 1-3 prescriptions per visit
                num_prescriptions = random.randint(1, 3)
                for _ in range(num_prescriptions):
                    med = random.choice(medications)
                    prescription = Prescription(
                        visit_id=visit.id,
                        medicament_num_enr=med.num_enr,
                        dosage_instructions=random.choice([
                            "1 comprimé matin et soir après les repas",
                            "2 comprimés 3 fois par jour",
                            "1 comprimé le soir au coucher",
                            "1/2 comprimé matin et soir",
                            "1 comprimé toutes les 8 heures"
                        ]),
                        quantity=random.randint(1, 3)
                    )
                    db.session.add(prescription)
                
                visits_created += 1
        
        db.session.commit()
        print(f"✅ Created {visits_created} visits with prescriptions")
        
        # Create appointments (future and past)
        print("\n📅 Creating Appointments...")
        appointments_created = 0
        
        # Past appointments (completed)
        for _ in range(15):
            days_ago = random.randint(1, 60)
            appt_date = datetime.now() - timedelta(days=days_ago, hours=random.randint(8, 17))
            
            appointment = Appointment(
                patient_id=random.choice(all_patients).id,
                doctor_id=random.choice(doctors).id,
                date=appt_date,
                reason=random.choice([
                    "Consultation de contrôle",
                    "ECG de routine",
                    "Suivi post-opératoire",
                    "Renouvellement d'ordonnance",
                    "Contrôle tension artérielle"
                ]),
                state='completed'
            )
            db.session.add(appointment)
            appointments_created += 1
        
        # Future appointments (scheduled)
        for _ in range(20):
            days_ahead = random.randint(1, 45)
            appt_date = datetime.now() + timedelta(days=days_ahead, hours=random.randint(8, 17))
            
            appointment = Appointment(
                patient_id=random.choice(all_patients).id,
                doctor_id=random.choice(doctors).id,
                date=appt_date,
                reason=random.choice([
                    "Consultation de contrôle",
                    "ECG programmé",
                    "Bilan cardiologique",
                    "Consultation initiale",
                    "Suivi traitement"
                ]),
                state='scheduled'
            )
            db.session.add(appointment)
            appointments_created += 1
        
        db.session.commit()
        print(f"✅ Created {appointments_created} appointments")
        
        # Final summary
        print("\n" + "=" * 50)
        print("✅ Demo Data Creation Complete!")
        print("=" * 50)
        print("\n📊 Final Database Status:")
        print(f"   👥 Patients: {Patient.query.count()}")
        print(f"   👨‍⚕️ Doctors: {Doctor.query.count()}")
        print(f"   👤 Users: {User.query.count()}")
        print(f"   🏥 Visits: {Visit.query.count()}")
        print(f"   💊 Prescriptions: {Prescription.query.count()}")
        print(f"   📅 Appointments: {Appointment.query.count()}")
        print(f"   💊 Medications: {Medicament.query.count()}")
        
        print("\n🔐 Login Credentials:")
        print("   Doctor:")
        print("     Username: a.benali")
        print("     Password: demo123")
        print("   Assistant:")
        print("     Username: assistant")
        print("     Password: demo123")
        
        print("\n✨ Ready for showcase!")

if __name__ == "__main__":
    try:
        create_demo_data()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
