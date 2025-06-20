from app import app, db, PostoLetto

# Crea un contesto dell'applicazione
with app.app_context():
    # Verifica se esiste già un letto con numero '101'
    existing_bed = PostoLetto.query.filter_by(numero='101').first()
    
    if not existing_bed:
        # Crea un nuovo letto di test
        test_bed = PostoLetto(numero='101', stato='libero')
        db.session.add(test_bed)
        db.session.commit()
        print("Letto di test creato con ID:", test_bed.id)
    else:
        print("Il letto di test esiste già con ID:", existing_bed.id)