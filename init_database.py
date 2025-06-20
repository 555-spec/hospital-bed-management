from app import app, db
import maintenance_staff

# Script per inizializzare il database e creare tutte le tabelle

print("Inizializzazione del database...")

# Inizializza i modelli di maintenance_staff
maintenance_staff.db = db
maintenance_staff.init_models()

# Crea un contesto dell'applicazione
with app.app_context():
    # Crea tutte le tabelle
    db.create_all()
    print("Database inizializzato con successo!")
    print("Tabelle create:")
    
    # Mostra le tabelle create
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    table_names = inspector.get_table_names()
    for table in table_names:
        print(f"- {table}")
    
    print("\nOra puoi eseguire create_maintenance_staff.py per popolare il database.")