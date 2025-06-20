from app import app, db, PostoLetto

# Coordinate 3D per i letti esistenti
# Simuliamo un ospedale con 3 piani e diverse stanze per reparto
bed_coordinates = {
    # Piano 1 - Cardiologia
    '101': {'x': -6, 'y': 0, 'z': -3, 'piano': 1},
    '102': {'x': -6, 'y': 0, 'z': 0, 'piano': 1},
    '103': {'x': -6, 'y': 0, 'z': 3, 'piano': 1},
    
    # Piano 2 - Pediatria
    '201': {'x': -3, 'y': 0, 'z': -3, 'piano': 2},
    '202': {'x': -3, 'y': 0, 'z': 0, 'piano': 2},
    '203': {'x': -3, 'y': 0, 'z': 3, 'piano': 2},
    
    # Piano 3 - Ortopedia
    '301': {'x': 0, 'y': 0, 'z': -3, 'piano': 3},
    '302': {'x': 0, 'y': 0, 'z': 0, 'piano': 3},
    '303': {'x': 0, 'y': 0, 'z': 3, 'piano': 3},
    
    # Aggiungiamo altri letti per una dimostrazione più ricca
    # Piano 1 - Cardiologia (stanza 2)
    '104': {'x': -3, 'y': 0, 'z': -3, 'piano': 1},
    '105': {'x': -3, 'y': 0, 'z': 0, 'piano': 1},
    '106': {'x': -3, 'y': 0, 'z': 3, 'piano': 1},
    
    # Piano 2 - Pediatria (stanza 2)
    '204': {'x': 0, 'y': 0, 'z': -3, 'piano': 2},
    '205': {'x': 0, 'y': 0, 'z': 0, 'piano': 2},
    '206': {'x': 0, 'y': 0, 'z': 3, 'piano': 2},
    
    # Piano 3 - Ortopedia (stanza 2)
    '304': {'x': 3, 'y': 0, 'z': -3, 'piano': 3},
    '305': {'x': 3, 'y': 0, 'z': 0, 'piano': 3},
    '306': {'x': 3, 'y': 0, 'z': 3, 'piano': 3},
    
    # Piano 1 - Medicina Generale
    '107': {'x': 3, 'y': 0, 'z': -3, 'piano': 1},
    '108': {'x': 3, 'y': 0, 'z': 0, 'piano': 1},
    '109': {'x': 3, 'y': 0, 'z': 3, 'piano': 1},
    
    # Piano 2 - Chirurgia
    '207': {'x': 6, 'y': 0, 'z': -3, 'piano': 2},
    '208': {'x': 6, 'y': 0, 'z': 0, 'piano': 2},
    '209': {'x': 6, 'y': 0, 'z': 3, 'piano': 2},
}

# Nuovi letti da creare con coordinate
new_beds = [
    # Piano 1
    {'numero': '104', 'stato': 'libero', 'reparto': 'Cardiologia'},
    {'numero': '105', 'stato': 'occupato', 'reparto': 'Cardiologia'},
    {'numero': '106', 'stato': 'in_pulizia', 'reparto': 'Cardiologia'},
    {'numero': '107', 'stato': 'libero', 'reparto': 'Medicina Generale'},
    {'numero': '108', 'stato': 'occupato', 'reparto': 'Medicina Generale'},
    {'numero': '109', 'stato': 'libero', 'reparto': 'Medicina Generale'},
    
    # Piano 2
    {'numero': '203', 'stato': 'libero', 'reparto': 'Pediatria'},
    {'numero': '204', 'stato': 'occupato', 'reparto': 'Pediatria'},
    {'numero': '205', 'stato': 'in_pulizia', 'reparto': 'Pediatria'},
    {'numero': '206', 'stato': 'libero', 'reparto': 'Pediatria'},
    {'numero': '207', 'stato': 'occupato', 'reparto': 'Chirurgia'},
    {'numero': '208', 'stato': 'libero', 'reparto': 'Chirurgia'},
    {'numero': '209', 'stato': 'in_pulizia', 'reparto': 'Chirurgia'},
    
    # Piano 3
    {'numero': '304', 'stato': 'libero', 'reparto': 'Ortopedia'},
    {'numero': '305', 'stato': 'occupato', 'reparto': 'Ortopedia'},
    {'numero': '306', 'stato': 'libero', 'reparto': 'Ortopedia'},
]

with app.app_context():
    print("Aggiornamento coordinate letti esistenti...")
    
    # Aggiorna le coordinate dei letti esistenti
    for bed_number, coords in bed_coordinates.items():
        bed = PostoLetto.query.filter_by(numero=bed_number).first()
        if bed:
            bed.coordinate_x = coords['x']
            bed.coordinate_y = coords['y']
            bed.coordinate_z = coords['z']
            bed.piano = coords['piano']
            print(f"Aggiornate coordinate per letto {bed_number}: ({coords['x']}, {coords['y']}, {coords['z']}) - Piano {coords['piano']}")
        else:
            print(f"Letto {bed_number} non trovato nel database")
    
    print("\nCreazione nuovi letti...")
    
    # Crea nuovi letti se non esistono
    for bed_data in new_beds:
        existing_bed = PostoLetto.query.filter_by(numero=bed_data['numero']).first()
        
        if not existing_bed:
            coords = bed_coordinates.get(bed_data['numero'], {'x': 0, 'y': 0, 'z': 0, 'piano': 1})
            
            new_bed = PostoLetto(
                numero=bed_data['numero'],
                stato=bed_data['stato'],
                reparto=bed_data['reparto'],
                coordinate_x=coords['x'],
                coordinate_y=coords['y'],
                coordinate_z=coords['z'],
                piano=coords['piano']
            )
            
            db.session.add(new_bed)
            print(f"Creato nuovo letto {bed_data['numero']} - {bed_data['reparto']} - Piano {coords['piano']}")
        else:
            print(f"Letto {bed_data['numero']} già esistente")
    
    try:
        db.session.commit()
        print("\n✅ Aggiornamento completato con successo!")
        
        # Mostra statistiche finali
        total_beds = PostoLetto.query.count()
        floors = db.session.query(PostoLetto.piano).distinct().count()
        departments = db.session.query(PostoLetto.reparto).distinct().count()
        
        print(f"\n📊 Statistiche:")
        print(f"   Totale letti: {total_beds}")
        print(f"   Piani: {floors}")
        print(f"   Reparti: {departments}")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Errore durante l'aggiornamento: {e}")