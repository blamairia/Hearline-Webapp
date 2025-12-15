import csv
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from app import app, db
from models import Medicament

def import_medicaments():
    csv_path = os.path.join(app.root_path, 'medicament.csv')
    if not os.path.exists(csv_path):
        print(f"❌ Medicament CSV not found at {csv_path}")
        return

    with app.app_context():
        # Efficiency Check: If data exists, skip
        if Medicament.query.count() > 0:
            print("✅ Medicaments already loaded. Skipping import.")
            return

        print("💊 Importing medicaments from CSV...")
        count = 0
        batch_size = 500
        objects = []

        try:
            with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 5:
                        continue
                    
                    # Columns: 0=num_enr, 1=nom_com, 2=nom_dci, 3=dosage, 4=unite
                    med = Medicament(
                        num_enr=row[0].strip(),
                        nom_com=row[1].strip(),
                        nom_dci=row[2].strip(),
                        dosage=row[3].strip(),
                        unite=row[4].strip()
                    )
                    objects.append(med)
                    count += 1
                    
                    if len(objects) >= batch_size:
                        db.session.bulk_save_objects(objects)
                        db.session.commit()
                        objects = []
                        print(f"   Imported {count} medicaments...")

            if objects:
                db.session.bulk_save_objects(objects)
                db.session.commit()

            print(f"✅ Successfully imported {count} medicaments.")
        
        except Exception as e:
            print(f"❌ Error during import: {e}")
            db.session.rollback()

if __name__ == '__main__':
    import_medicaments()
