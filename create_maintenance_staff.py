from app import app, db
import maintenance_staff

# I modelli sono già inizializzati in app.py, quindi possiamo accedere direttamente
PersonaleManutenzione = maintenance_staff.PersonaleManutenzione

# Lista del personale sanitario addetto alla manutenzione letti da creare
personale_da_creare = [
    {
        'nome': 'Marco Infermiere',
        'ruolo': 'Infermiere Senior',
        'device_id': 'BT001',
        'coordinate_x': -5,
        'coordinate_y': 0,
        'coordinate_z': -2,
        'piano': 1
    },
    {
        'nome': 'Laura OSS',
        'ruolo': 'Operatore Socio Sanitario',
        'device_id': 'BT002',
        'coordinate_x': 2,
        'coordinate_y': 0,
        'coordinate_z': 3,
        'piano': 2
    },
    {
        'nome': 'Giovanni Infermiere',
        'ruolo': 'Infermiere Specializzato',
        'device_id': 'BT003',
        'coordinate_x': -1,
        'coordinate_y': 0,
        'coordinate_z': 5,
        'piano': 3
    },
    {
        'nome': 'Francesca OSS',
        'ruolo': 'Operatore Socio Sanitario',
        'device_id': 'BT004',
        'coordinate_x': 4,
        'coordinate_y': 0,
        'coordinate_z': -3,
        'piano': 1
    },
    {
        'nome': 'Roberto Coordinatore',
        'ruolo': 'Coordinatore Infermieristico',
        'device_id': 'BT005',
        'coordinate_x': 0,
        'coordinate_y': 0,
        'coordinate_z': 0,
        'piano': 2
    }
]

# Crea un contesto dell'applicazione
with app.app_context():
    # Creazione del personale
    for persona in personale_da_creare:
        # Verifica se il personale esiste già
        existing_staff = PersonaleManutenzione.query.filter_by(device_id=persona['device_id']).first()
        
        if not existing_staff:
            # Crea nuovo personale
            new_staff = PersonaleManutenzione(
                nome=persona['nome'],
                ruolo=persona['ruolo'],
                device_id=persona['device_id'],
                coordinate_x=persona['coordinate_x'],
                coordinate_y=persona['coordinate_y'],
                coordinate_z=persona['coordinate_z'],
                piano=persona['piano'],
                disponibile=True
            )
            
            db.session.add(new_staff)
            print(f"Personale creato: {persona['nome']} con dispositivo {persona['device_id']}")
        else:
            print(f"Il personale con dispositivo {persona['device_id']} esiste già")
    
    # Commit delle modifiche
    try:
        db.session.commit()
        print("\nPersonale di manutenzione creato con successo!")
    except Exception as e:
        db.session.rollback()
        print(f"Errore durante la creazione del personale: {str(e)}")