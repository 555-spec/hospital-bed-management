from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math

# Questo sarà inizializzato da app.py
db = None
PersonaleManutenzione = None

def init_models():
    global PersonaleManutenzione
    
    class PersonaleManutenzione(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        nome = db.Column(db.String(100), nullable=False)
        ruolo = db.Column(db.String(50), default='Tecnico')
        disponibile = db.Column(db.Boolean, default=True)
        coordinate_x = db.Column(db.Float, default=0)  # Posizione corrente
        coordinate_y = db.Column(db.Float, default=0)
        coordinate_z = db.Column(db.Float, default=0)
        piano = db.Column(db.Integer, default=1)
        device_id = db.Column(db.String(100))  # ID del bracciale Bluetooth
        ultimo_aggiornamento = db.Column(db.DateTime, default=datetime.utcnow)

        def __repr__(self):
            return f'<PersonaleManutenzione {self.nome}> - Dispositivo: {self.device_id}'
        
        def to_dict(self):
            return {
                'id': self.id,
                'nome': self.nome,
                'ruolo': self.ruolo,
                'disponibile': self.disponibile,
                'coordinate': {
                    'x': self.coordinate_x,
                    'y': self.coordinate_y,
                    'z': self.coordinate_z,
                    'piano': self.piano
                },
                'device_id': self.device_id,
                'ultimo_aggiornamento': self.ultimo_aggiornamento.isoformat()
            }
    
    # Assegna la classe alla variabile globale
    globals()['PersonaleManutenzione'] = PersonaleManutenzione

# Funzione per calcolare la distanza euclidea 3D tra due punti
def calcola_distanza(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

# Funzione per trovare il personale più vicino a un punto
def trova_personale_piu_vicino(x, y, z, piano=None):
    personale = PersonaleManutenzione.query.filter_by(disponibile=True).all()
    
    if not personale:
        return None
    
    personale_con_distanza = []
    for p in personale:
        # Se è specificato il piano, considera solo il personale sullo stesso piano
        if piano is not None and p.piano != piano:
            continue
            
        distanza = calcola_distanza(x, y, z, p.coordinate_x, p.coordinate_y, p.coordinate_z)
        # Aggiungi un fattore di penalità se il personale è su un piano diverso
        if piano is not None and p.piano != piano:
            distanza += 100  # Penalità per cambio piano
            
        personale_con_distanza.append((p, distanza))
    
    if not personale_con_distanza:
        return None
        
    # Ordina per distanza e prendi il primo
    personale_con_distanza.sort(key=lambda x: x[1])
    personale_piu_vicino, distanza = personale_con_distanza[0]
    
    # Calcola tempo stimato di arrivo (ETA) - assumiamo una velocità media di 1.2 m/s
    velocita_media = 1.2  # metri al secondo
    eta_secondi = distanza / velocita_media
    
    return {
        'staff': personale_piu_vicino.to_dict(),
        'distanza': distanza,
        'eta': eta_secondi,
        'eta_formatted': f"{int(eta_secondi // 60)} min {int(eta_secondi % 60)} sec"
    }

# Le tabelle verranno create da app.py