from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import pathlib
from flask_cors import CORS
from dotenv import load_dotenv
import random  # Per simulare l'algoritmo di ottimizzazione

# Carica le variabili d'ambiente
load_dotenv()

# Crea la directory per il database se non esiste (fallback per SQLite)
database_dir = pathlib.Path(__file__).parent.parent / 'database'
database_dir.mkdir(exist_ok=True)
database_file = database_dir / 'hospital.db'

app = Flask(__name__)

# Configurazione CORS migliorata per produzione
if os.getenv('FLASK_ENV') == 'production':
    # In produzione, specifica i domini consentiti
    allowed_origins = [
        "https://your-frontend-domain.vercel.app",  # Sostituisci con il tuo dominio Vercel
        "https://your-render-domain.onrender.com",  # Sostituisci con il tuo dominio Render
    ]
    CORS(app, origins=allowed_origins)
else:
    # In sviluppo, permetti tutti i domini
    CORS(app)

# Usa DATABASE_URL dal .env se disponibile, altrimenti SQLite
database_url = os.getenv('DATABASE_URL')
try:
    if database_url and 'mysql' in database_url:
        # Testa se mysql-connector-python è disponibile
        import mysql.connector
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print(f"🗄️ Usando database MySQL: {database_url.split('@')[1] if '@' in database_url else 'configurato'}")
    else:
        raise ImportError("MySQL non configurato o non disponibile")
except ImportError:
    # Fallback a SQLite se MySQL non è disponibile
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_file}'
    print(f"🗄️ MySQL non disponibile, usando database SQLite: {database_file}")
    print(f"💡 Per usare MySQL, installa: pip install mysql-connector-python")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class PostoLetto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True, nullable=False)
    stato = db.Column(db.String(20), default='libero')
    reparto = db.Column(db.String(50), default='Generale')
    coordinate_x = db.Column(db.Float, default=0)  # Per la mappa 3D
    coordinate_y = db.Column(db.Float, default=0)  # Per la mappa 3D
    coordinate_z = db.Column(db.Float, default=0)  # Per la mappa 3D
    piano = db.Column(db.Integer, default=1)       # Piano dell'edificio

class Paziente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    gravita = db.Column(db.Integer, default=3)  # Scala 1-5, dove 5 è più grave
    reparto_richiesto = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    assegnato = db.Column(db.Boolean, default=False)
    bed_id = db.Column(db.Integer, db.ForeignKey('posto_letto.id'), nullable=True)

class Notifica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bed_id = db.Column(db.Integer, db.ForeignKey('posto_letto.id'), nullable=False)
    messaggio = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    consegnata = db.Column(db.Boolean, default=False)
    priorita = db.Column(db.String(20), default='medium')  # Priorità: high, medium, low

# Crea tutte le tabelle
with app.app_context():
    db.create_all()

# NUOVO ENDPOINT: Inizializza demo con dati di esempio
@app.route('/api/init-demo', methods=['POST'])
def init_demo():
    """Popola il database con dati di esempio per la demo"""
    try:
        # Verifica se i dati demo esistono già
        if PostoLetto.query.count() > 0:
            return jsonify({'message': 'Demo già inizializzata', 'status': 'already_initialized'}), 200
        
        # Crea letti di esempio
        demo_beds = [
            # Piano 1 - Pronto Soccorso
            {'numero': 'PS001', 'stato': 'libero', 'reparto': 'Pronto Soccorso', 'x': 100, 'y': 150, 'z': 0, 'piano': 1},
            {'numero': 'PS002', 'stato': 'occupato', 'reparto': 'Pronto Soccorso', 'x': 150, 'y': 150, 'z': 0, 'piano': 1},
            {'numero': 'PS003', 'stato': 'in_pulizia', 'reparto': 'Pronto Soccorso', 'x': 200, 'y': 150, 'z': 0, 'piano': 1},
            {'numero': 'PS004', 'stato': 'libero', 'reparto': 'Pronto Soccorso', 'x': 250, 'y': 150, 'z': 0, 'piano': 1},
            
            # Piano 2 - Cardiologia
            {'numero': 'CAR001', 'stato': 'occupato', 'reparto': 'Cardiologia', 'x': 100, 'y': 250, 'z': 0, 'piano': 2},
            {'numero': 'CAR002', 'stato': 'libero', 'reparto': 'Cardiologia', 'x': 150, 'y': 250, 'z': 0, 'piano': 2},
            {'numero': 'CAR003', 'stato': 'libero', 'reparto': 'Cardiologia', 'x': 200, 'y': 250, 'z': 0, 'piano': 2},
            
            # Piano 3 - Pediatria
            {'numero': 'PED001', 'stato': 'libero', 'reparto': 'Pediatria', 'x': 100, 'y': 350, 'z': 0, 'piano': 3},
            {'numero': 'PED002', 'stato': 'occupato', 'reparto': 'Pediatria', 'x': 150, 'y': 350, 'z': 0, 'piano': 3},
            {'numero': 'PED003', 'stato': 'libero', 'reparto': 'Pediatria', 'x': 200, 'y': 350, 'z': 0, 'piano': 3},
        ]
        
        for bed_data in demo_beds:
            bed = PostoLetto(
                numero=bed_data['numero'],
                stato=bed_data['stato'],
                reparto=bed_data['reparto'],
                coordinate_x=bed_data['x'],
                coordinate_y=bed_data['y'],
                coordinate_z=bed_data['z'],
                piano=bed_data['piano']
            )
            db.session.add(bed)
        
        # Crea pazienti di esempio in attesa
        demo_patients = [
            {'nome': 'Mario Rossi', 'gravita': 4, 'reparto': 'Cardiologia'},
            {'nome': 'Anna Bianchi', 'gravita': 2, 'reparto': 'Pediatria'},
            {'nome': 'Giuseppe Verdi', 'gravita': 5, 'reparto': 'Pronto Soccorso'},
        ]
        
        for patient_data in demo_patients:
            patient = Paziente(
                nome=patient_data['nome'],
                gravita=patient_data['gravita'],
                reparto_richiesto=patient_data['reparto'],
                assegnato=False
            )
            db.session.add(patient)
        
        # Crea alcune notifiche di esempio
        demo_notifications = [
            {'bed_id': 3, 'messaggio': 'Letto PS003 richiede pulizia urgente', 'priorita': 'high'},
            {'bed_id': 1, 'messaggio': 'Letto PS001 pronto per nuovo paziente', 'priorita': 'medium'},
        ]
        
        for notif_data in demo_notifications:
            notification = Notifica(
                bed_id=notif_data['bed_id'],
                messaggio=notif_data['messaggio'],
                priorita=notif_data['priorita'],
                consegnata=False
            )
            db.session.add(notification)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Demo inizializzata con successo',
            'status': 'initialized',
            'data': {
                'beds_created': len(demo_beds),
                'patients_created': len(demo_patients),
                'notifications_created': len(demo_notifications)
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Inizializzazione demo fallita', 'details': str(e)}), 500

@app.route('/api/sensor_update', methods=['POST'])
def sensor_update():
    data = request.json
    bed_id = data.get('bed_id')
    pressure = data.get('pressure')

    if not bed_id or pressure is None:
        return jsonify({'error': 'Mancano bed_id o dati di pressione'}), 400

    bed = PostoLetto.query.get(bed_id)
    if not bed:
        return jsonify({'error': 'Letto non trovato'}), 404

    if pressure < 10:  # Pressione bassa = letto libero
        if bed.stato == 'occupato':
            bed.stato = 'in_pulizia'
            send_notification(bed_id, f'Letto {bed_id} richiede pulizia', 'high')
        elif bed.stato == 'in_pulizia':
            pass  # Rimane in pulizia finché non completata

    elif pressure >= 10:  # Pressione alta = letto occupato
        bed.stato = 'occupato'

    try:
        db.session.commit()
        return jsonify({'message': f'Stato letto {bed_id} aggiornato a {bed.stato}'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Aggiornamento database fallito', 'details': str(e)}), 500

@app.route('/api/complete_cleaning', methods=['POST'])
def complete_cleaning():
    data = request.json
    bed_id = data.get('bed_id')

    if not bed_id:
        return jsonify({'error': 'Mancano bed_id'}), 400

    bed = PostoLetto.query.get(bed_id)
    if not bed:
        return jsonify({'error': 'Letto non trovato'}), 404

    if bed.stato != 'in_pulizia':
        return jsonify({'error': 'Il letto non è in stato di pulizia'}), 400

    bed.stato = 'libero'
    send_notification(bed_id, f'Letto {bed_id} pulito e pronto', 'medium')

    # Verifica se ci sono pazienti in attesa che possono essere assegnati a questo letto
    run_optimization()

    try:
        db.session.commit()
        return jsonify({'message': f'Letto {bed_id} ora è libero'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Aggiornamento database fallito', 'details': str(e)}), 500

def send_notification(bed_id, message, priority='medium'):
    try:
        # Simulazione invio notifica in tempo reale
        # Se fallisce, salva nel database
        new_notification = Notifica(
            bed_id=bed_id,
            messaggio=message,
            consegnata=False,
            priorita=priority
        )
        db.session.add(new_notification)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f'Errore invio notifica: {str(e)}')

@app.route('/api/get_pending_notifications', methods=['GET'])
def get_pending_notifications():
    notifications = Notifica.query.filter_by(consegnata=False).all()
    result = []
    
    for n in notifications:
        # Ottieni il reparto del letto associato alla notifica
        bed = PostoLetto.query.get(n.bed_id)
        department = bed.reparto if bed else 'Generale'
        
        result.append({
            'id': n.id,
            'bed_number': n.bed_id,
            'title': f'Notifica per letto {n.bed_id}',
            'message': n.messaggio,
            'department': department,
            'priority': n.priorita,
            'timestamp': n.timestamp.isoformat() if n.timestamp else datetime.utcnow().isoformat()
        })

    # Marca come consegnate
    for n in notifications:
        n.consegnata = True
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Aggiornamento notifiche fallito', 'details': str(e)}), 500

    return jsonify(result), 200

@app.route('/api/sync_notifications', methods=['POST'])
def sync_notifications():
    data = request.json
    last_sync = datetime.fromisoformat(data.get('last_sync')) if data.get('last_sync') else None

    query = Notifica.query
    if last_sync:
        query = query.filter(Notifica.timestamp > last_sync)

    notifications = query.all()
    result = []
    
    for n in notifications:
        # Ottieni il reparto del letto associato alla notifica
        bed = PostoLetto.query.get(n.bed_id)
        department = bed.reparto if bed else 'Generale'
        
        result.append({
            'id': n.id,
            'bed_number': n.bed_id,
            'title': f'Notifica per letto {n.bed_id}',
            'message': n.messaggio,
            'department': department,
            'priority': n.priorita,
            'timestamp': n.timestamp.isoformat()
        })

    return jsonify(result), 200

# Funzione per tradurre gli stati dall'italiano all'inglese
def translate_status(stato):
    translations = {
        'libero': 'available',
        'occupato': 'occupied',
        'in_pulizia': 'maintenance'
    }
    return translations.get(stato, stato)

# NUOVO ENDPOINT: Aggiornamento stato letto
@app.route('/api/update_bed_status', methods=['POST'])
def update_bed_status():
    data = request.json
    bed_id = data.get('bed_id')
    status = data.get('status')

    if not bed_id or not status:
        return jsonify({'error': 'Mancano bed_id o status'}), 400

    bed = PostoLetto.query.get(bed_id)
    if not bed:
        return jsonify({'error': 'Letto non trovato'}), 404

    # Traduci lo stato dall'inglese all'italiano
    status_translations = {
        'available': 'libero',
        'occupied': 'occupato',
        'maintenance': 'in_pulizia'
    }
    
    italian_status = status_translations.get(status)
    if not italian_status:
        return jsonify({'error': 'Stato non valido'}), 400
    
    # Salva lo stato precedente per confronto
    previous_status = bed.stato
    
    # Aggiorna lo stato
    bed.stato = italian_status
    
    # Genera notifiche appropriate in base al cambio di stato
    if previous_status != italian_status:
        if italian_status == 'libero':
            send_notification(bed_id, f'Letto {bed_id} ora disponibile', 'medium')
            # Esegui ottimizzazione quando un letto diventa disponibile
            run_optimization()
        elif italian_status == 'occupato':
            send_notification(bed_id, f'Letto {bed_id} ora occupato', 'low')
        elif italian_status == 'in_pulizia':
            send_notification(bed_id, f'Letto {bed_id} richiede pulizia', 'high')

    try:
        db.session.commit()
        return jsonify({
            'message': f'Stato letto {bed_id} aggiornato a {status}',
            'bed': {
                'id': bed.id,
                'bed_number': bed.numero,
                'status': status,
                'department': bed.reparto,
                'coordinates': {
                    'x': bed.coordinate_x,
                    'y': bed.coordinate_y,
                    'z': bed.coordinate_z,
                    'floor': bed.piano
                }
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Aggiornamento database fallito', 'details': str(e)}), 500

# Endpoint per ottenere i dati dei letti
@app.route('/api/beds', methods=['GET'])
def get_beds():
    beds = PostoLetto.query.all()
    result = [{
        'id': bed.id,
        'bed_number': bed.numero,
        'status': translate_status(bed.stato),
        'department': bed.reparto,
        'coordinates': {
            'x': bed.coordinate_x,
            'y': bed.coordinate_y,
            'z': bed.coordinate_z,
            'floor': bed.piano
        }
    } for bed in beds]
    
    return jsonify(result), 200

# NUOVO ENDPOINT: Aggiunta paziente in attesa
@app.route('/api/add_patient', methods=['POST'])
def add_patient():
    data = request.json
    nome = data.get('nome')
    gravita = data.get('gravita', 3)
    reparto = data.get('reparto', 'Generale')
    
    if not nome:
        return jsonify({'error': 'Nome paziente mancante'}), 400
        
    new_patient = Paziente(
        nome=nome,
        gravita=gravita,
        reparto_richiesto=reparto
    )
    
    db.session.add(new_patient)
    
    try:
        db.session.commit()
        # Esegui ottimizzazione per assegnare un letto al nuovo paziente
        assigned_bed = run_optimization(new_patient.id)
        
        return jsonify({
            'message': 'Paziente aggiunto con successo',
            'patient_id': new_patient.id,
            'assigned_bed': assigned_bed
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Aggiunta paziente fallita', 'details': str(e)}), 500

# NUOVO ENDPOINT: Ottieni pazienti in attesa
@app.route('/api/waiting_patients', methods=['GET'])
def get_waiting_patients():
    patients = Paziente.query.filter_by(assegnato=False).all()
    result = [{
        'id': p.id,
        'nome': p.nome,
        'gravita': p.gravita,
        'reparto_richiesto': p.reparto_richiesto,
        'timestamp': p.timestamp.isoformat() if p.timestamp else datetime.utcnow().isoformat()
    } for p in patients]
    
    return jsonify(result), 200

# NUOVO ENDPOINT: Esegui ottimizzazione manualmente
@app.route('/api/run_optimization', methods=['POST'])
def api_run_optimization():
    result = run_optimization()
    return jsonify(result), 200

# Funzione di ottimizzazione
def run_optimization(specific_patient_id=None):
    # Ottieni tutti i letti disponibili
    available_beds = PostoLetto.query.filter_by(stato='libero').all()
    
    # Se non ci sono letti disponibili, termina
    if not available_beds:
        return {'message': 'Nessun letto disponibile per l\'ottimizzazione'}
    
    # Ottieni i pazienti in attesa
    if specific_patient_id:
        patients = Paziente.query.filter_by(id=specific_patient_id, assegnato=False).all()
    else:
        patients = Paziente.query.filter_by(assegnato=False).order_by(Paziente.gravita.desc()).all()
    
    # Se non ci sono pazienti in attesa, termina
    if not patients:
        return {'message': 'Nessun paziente in attesa'}
    
    assignments = []
    
    # Algoritmo di ottimizzazione semplificato
    for patient in patients:
        # Cerca un letto nello stesso reparto richiesto dal paziente
        matching_beds = [bed for bed in available_beds if bed.reparto == patient.reparto_richiesto]
        
        if matching_beds:
            # Assegna il primo letto disponibile nel reparto richiesto
            bed = matching_beds[0]
        elif available_beds:
            # Se non ci sono letti nel reparto richiesto, assegna il primo disponibile
            bed = available_beds[0]
        else:
            # Non ci sono più letti disponibili
            continue
        
        # Rimuovi il letto assegnato dalla lista dei disponibili
        available_beds.remove(bed)
        
        # Aggiorna lo stato del letto
        bed.stato = 'occupato'
        
        # Aggiorna lo stato del paziente
        patient.assegnato = True
        patient.bed_id = bed.id
        
        # Crea una notifica
        send_notification(
            bed.id, 
            f'Paziente {patient.nome} assegnato automaticamente al letto {bed.numero}',
            'high' if patient.gravita >= 4 else 'medium'
        )
        
        assignments.append({
            'patient_id': patient.id,
            'patient_name': patient.nome,
            'bed_id': bed.id,
            'bed_number': bed.numero,
            'department': bed.reparto
        })
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {'error': 'Ottimizzazione fallita', 'details': str(e)}
    
    return {
        'message': f'Ottimizzazione completata: {len(assignments)} pazienti assegnati',
        'assignments': assignments
    }

# Import e inizializzazione dei moduli di manutenzione (solo se esistono)
try:
    import maintenance_staff
    maintenance_staff.db = db  # Inizializza db nel modulo maintenance_staff
    maintenance_staff.init_models()  # Inizializza i modelli dopo aver impostato db

    import maintenance_api
    maintenance_api.app = app  # Inizializza app nel modulo maintenance_api
    maintenance_api.db = db    # Inizializza db nel modulo maintenance_api
    maintenance_api.PostoLetto = PostoLetto  # Inizializza PostoLetto nel modulo maintenance_api
    maintenance_api.init_routes()  # Inizializza le route dopo aver impostato le variabili

    # Popola il database con personale sanitario OSS e Infermieri se vuoto
    with app.app_context():
        from maintenance_staff import PersonaleManutenzione
        if PersonaleManutenzione.query.count() == 0:
            print("Popolamento database con personale sanitario (OSS e Infermieri)...")
            
            personale_sanitario = [
                # Piano 1 - Pronto Soccorso/Emergenze (9 persone)
                {"nome": "Marco Rossi", "ruolo": "OSS", "device_id": "OSS001_BT", "x": 120, "y": 180, "piano": 1},
                {"nome": "Anna Verdi", "ruolo": "Infermiere", "device_id": "INF001_BT", "x": 180, "y": 160, "piano": 1},
                {"nome": "Giuseppe Bianchi", "ruolo": "OSS", "device_id": "OSS002_BT", "x": 220, "y": 200, "piano": 1},
                {"nome": "Laura Neri", "ruolo": "Infermiere", "device_id": "INF002_BT", "x": 160, "y": 220, "piano": 1},
                {"nome": "Francesco Blu", "ruolo": "OSS", "device_id": "OSS003_BT", "x": 200, "y": 140, "piano": 1},
                {"nome": "Giulia Rosa", "ruolo": "Infermiere", "device_id": "INF003_BT", "x": 140, "y": 200, "piano": 1},
                {"nome": "Roberto Verde", "ruolo": "OSS", "device_id": "OSS004_BT", "x": 240, "y": 180, "piano": 1},
                {"nome": "Maria Gialli", "ruolo": "Infermiere", "device_id": "INF004_BT", "x": 200, "y": 240, "piano": 1},
                {"nome": "Paolo Viola", "ruolo": "Infermiere", "device_id": "INF005_BT", "x": 180, "y": 120, "piano": 1},
                
                # Piano 2 - Reparti Specialistici (9 persone)
                {"nome": "Elena Arancio", "ruolo": "OSS", "device_id": "OSS005_BT", "x": 150, "y": 280, "piano": 2},
                {"nome": "Luca Marrone", "ruolo": "Infermiere", "device_id": "INF006_BT", "x": 200, "y": 260, "piano": 2},
                {"nome": "Sara Grigio", "ruolo": "OSS", "device_id": "OSS006_BT", "x": 180, "y": 300, "piano": 2},
                {"nome": "Andrea Nero", "ruolo": "Infermiere", "device_id": "INF007_BT", "x": 220, "y": 280, "piano": 2},
                {"nome": "Chiara Celeste", "ruolo": "OSS", "device_id": "OSS007_BT", "x": 160, "y": 320, "piano": 2},
                {"nome": "Matteo Oro", "ruolo": "Infermiere", "device_id": "INF008_BT", "x": 240, "y": 300, "piano": 2},
                {"nome": "Federica Argento", "ruolo": "OSS", "device_id": "OSS008_BT", "x": 140, "y": 260, "piano": 2},
                {"nome": "Davide Bronzo", "ruolo": "Infermiere", "device_id": "INF009_BT", "x": 200, "y": 320, "piano": 2},
                {"nome": "Valentina Rame", "ruolo": "Infermiere", "device_id": "INF010_BT", "x": 180, "y": 240, "piano": 2},
                
                # Piano 3 - Pediatria/Maternità (9 persone)
                {"nome": "Simone Perla", "ruolo": "OSS", "device_id": "OSS009_BT", "x": 170, "y": 380, "piano": 3},
                {"nome": "Alessia Corallo", "ruolo": "Infermiere", "device_id": "INF011_BT", "x": 210, "y": 360, "piano": 3},
                {"nome": "Nicola Turchese", "ruolo": "OSS", "device_id": "OSS010_BT", "x": 190, "y": 400, "piano": 3},
                {"nome": "Francesca Smeraldo", "ruolo": "Infermiere", "device_id": "INF012_BT", "x": 230, "y": 380, "piano": 3},
                {"nome": "Antonio Rubino", "ruolo": "OSS", "device_id": "OSS011_BT", "x": 150, "y": 360, "piano": 3},
                {"nome": "Silvia Zaffiro", "ruolo": "Infermiere", "device_id": "INF013_BT", "x": 250, "y": 400, "piano": 3},
                {"nome": "Emanuele Diamante", "ruolo": "OSS", "device_id": "OSS012_BT", "x": 170, "y": 420, "piano": 3},
                {"nome": "Cristina Topazio", "ruolo": "Infermiere", "device_id": "INF014_BT", "x": 210, "y": 340, "piano": 3},
                {"nome": "Michele Opale", "ruolo": "Infermiere", "device_id": "INF015_BT", "x": 190, "y": 360, "piano": 3}
            ]
            
            for persona in personale_sanitario:
                nuovo_personale = PersonaleManutenzione(
                    nome=persona["nome"],
                    ruolo=persona["ruolo"],
                    device_id=persona["device_id"],
                    disponibile=True,
                    coordinate_x=persona["x"],
                    coordinate_y=persona["y"],
                    coordinate_z=0,
                    piano=persona["piano"],
                    ultimo_aggiornamento=datetime.now()
                )
                db.session.add(nuovo_personale)
            
            try:
                db.session.commit()
                print(f"✅ Aggiunti {len(personale_sanitario)} membri del personale sanitario al database.")
                print(f"📊 Distribuzione: {len([p for p in personale_sanitario if p['ruolo'] == 'OSS'])} OSS, {len([p for p in personale_sanitario if p['ruolo'] == 'Infermiere'])} Infermieri")
                print(f"🏥 Piano 1: {len([p for p in personale_sanitario if p['piano'] == 1])} persone")
                print(f"🏥 Piano 2: {len([p for p in personale_sanitario if p['piano'] == 2])} persone")
                print(f"🏥 Piano 3: {len([p for p in personale_sanitario if p['piano'] == 3])} persone")
            except Exception as e:
                print(f"❌ Errore nel popolamento: {str(e)}")
except ImportError:
    print("⚠️ Moduli di manutenzione non trovati, continuando senza...")

# Aggiungi logging per le chiamate API
@app.before_request
def log_request_info():
    print(f"📡 {request.method} {request.url} - {datetime.now().strftime('%H:%M:%S')}")
    # Controlla se la richiesta ha Content-Type application/json prima di accedere a request.json
    if request.content_type == 'application/json' and request.json:
        print(f"📦 Body: {request.json}")

@app.after_request
def log_response_info(response):
    print(f"📤 Response: {response.status_code} - {datetime.now().strftime('%H:%M:%S')}")
    return response

if __name__ == '__main__':
    print("🚀 Avvio del server Flask...")
    print(f"🌐 Server disponibile su: http://localhost:5000")
    print(f"📋 Endpoints disponibili:")
    print(f"   - GET  /api/beds")
    print(f"   - GET  /api/waiting_patients")
    print(f"   - GET  /api/get_pending_notifications")
    print(f"   - POST /api/update_bed_status")
    print(f"   - POST /api/add_patient")
    print(f"   - POST /api/run_optimization")
    print(f"   - POST /api/complete_cleaning")
    print(f"   - POST /api/sensor_update")
    print(f"   - POST /api/sync_notifications")
    print(f"   - POST /api/init-demo")
    
    # Configurazione per produzione
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port)
