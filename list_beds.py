from app import app, db, PostoLetto

with app.app_context():
    beds = PostoLetto.query.all()
    print(f"Numero totale di letti: {len(beds)}")
    for bed in beds:
        print(f"ID: {bed.id}, Numero: {bed.numero}, Stato: {bed.stato}")