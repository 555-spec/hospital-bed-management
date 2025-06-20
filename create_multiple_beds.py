from app import app, db, PostoLetto

# Lista di letti da creare con i loro dettagli
letti_da_creare = [
    {'numero': '101', 'stato': 'libero', 'reparto': 'Cardiologia'},
    {'numero': '102', 'stato': 'libero', 'reparto': 'Cardiologia'},
    {'numero': '103', 'stato': 'occupato', 'reparto': 'Cardiologia'},
    {'numero': '201', 'stato': 'libero', 'reparto': 'Pediatria'},
    {'numero': '202', 'stato': 'occupato', 'reparto': 'Pediatria'},
    {'numero': '301', 'stato': 'libero', 'reparto': 'Ortopedia'},
    {'numero': '302', 'stato': 'occupato', 'reparto': 'Ortopedia'},
    {'numero': '303', 'stato': 'in_pulizia', 'reparto': 'Ortopedia'}
]

# Crea un contesto dell'applicazione
with app.app_context():
    # Creazione dei letti
    for letto in letti_da_creare:
        # Verifica se il letto esiste già
        existing_bed = PostoLetto.query.filter_by(numero=letto['numero']).first()
        
        if existing_bed:
            print(f"Il letto {letto['numero']} esiste già nel database.")
            # Aggiorna il reparto se necessario
            if existing_bed.reparto != letto['reparto']:
                existing_bed.reparto = letto['reparto']
                db.session.commit()
                print(f"  Aggiornato reparto a: {letto['reparto']}")
        else:
            # Inserisci il nuovo letto
            new_bed = PostoLetto(
                numero=letto['numero'],
                stato=letto['stato'],
                reparto=letto['reparto']
            )
            db.session.add(new_bed)
            db.session.commit()
            print(f"Creato nuovo letto: {letto['numero']} - {letto['reparto']} - {letto['stato']}")

print("Operazione completata!")