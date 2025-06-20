from app import app, db, Notifica

with app.app_context():
    notifications = Notifica.query.all()
    print(f"Numero totale di notifiche: {len(notifications)}")
    for n in notifications:
        print(f"ID: {n.id}, Letto ID: {n.bed_id}, Messaggio: {n.messaggio}, Consegnata: {n.consegnata}")