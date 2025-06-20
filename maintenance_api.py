from maintenance_staff import PersonaleManutenzione, trova_personale_piu_vicino
from bluetooth_notification_system import notification_system, notify_nearest_staff_for_bed_cleaning, get_notification_statistics
from datetime import datetime
from flask import jsonify, request

# Queste variabili saranno inizializzate da app.py
app = None
db = None
PostoLetto = None

def init_routes():
    """Inizializza le route dopo che app è stato impostato"""
    
    # API per ottenere tutto il personale di manutenzione
    @app.route('/api/maintenance/staff', methods=['GET'])
    def get_maintenance_staff():
        staff = PersonaleManutenzione.query.all()
        return jsonify([s.to_dict() for s in staff])

    # API per aggiornare la posizione di un bracciale
    @app.route('/api/maintenance/update_position', methods=['POST'])
    def update_staff_position():
        data = request.json
        device_id = data.get('device_id')
        x = data.get('x')
        y = data.get('y')
        z = data.get('z')
        piano = data.get('piano')
        
        if not device_id or x is None or y is None or z is None or piano is None:
            return jsonify({'error': 'Dati mancanti'}), 400
        
        # Trova il personale con questo device_id
        staff = PersonaleManutenzione.query.filter_by(device_id=device_id).first()
        
        if not staff:
            return jsonify({'error': 'Dispositivo non trovato'}), 404
        
        # Aggiorna la posizione
        staff.coordinate_x = float(x)
        staff.coordinate_y = float(y)
        staff.coordinate_z = float(z)
        staff.piano = int(piano)
        staff.ultimo_aggiornamento = datetime.utcnow()
        
        try:
            db.session.commit()
            return jsonify({'success': True, 'staff': staff.to_dict()})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # API per inviare notifica di pulizia al personale più vicino
    @app.route('/api/maintenance/notify_cleaning', methods=['POST'])
    def notify_cleaning():
        data = request.json
        bed_id = data.get('bed_id')
        urgency = data.get('urgency', 'normal')
        
        if not bed_id:
            return jsonify({'error': 'bed_id richiesto'}), 400
        
        # Ottieni informazioni sul letto
        bed = PostoLetto.query.get(bed_id)
        if not bed:
            return jsonify({'error': 'Letto non trovato'}), 404
        
        bed_info = {
            'bed_number': bed.bed_number,
            'department': bed.department,
            'coordinate_x': bed.coordinate_x or 0,
            'coordinate_y': bed.coordinate_y or 0,
            'coordinate_z': bed.coordinate_z or 0,
            'piano': bed.piano or 1
        }
        
        result = notify_nearest_staff_for_bed_cleaning(bed_id, bed_info, urgency)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
    
    # API per confermare ricezione notifica
    @app.route('/api/maintenance/acknowledge_notification', methods=['POST'])
    def acknowledge_notification():
        data = request.json
        notification_id = data.get('notification_id')
        staff_id = data.get('staff_id')
        
        if not notification_id or not staff_id:
            return jsonify({'error': 'notification_id e staff_id richiesti'}), 400
        
        success = notification_system.acknowledge_notification(notification_id, staff_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Notifica confermata'})
        else:
            return jsonify({'error': 'Notifica non trovata'}), 404
    
    # API per ottenere notifiche attive
    @app.route('/api/maintenance/notifications', methods=['GET'])
    def get_notifications():
        device_id = request.args.get('device_id')
        notifications = notification_system.get_active_notifications(device_id)
        return jsonify(notifications)
    
    # API per statistiche notifiche
    @app.route('/api/maintenance/notification_stats', methods=['GET'])
    def get_notification_stats():
        stats = get_notification_statistics()
        return jsonify(stats)
    
    # API per assegnazione automatica compiti di pulizia
    @app.route('/api/maintenance/auto_assign_cleaning', methods=['POST'])
    def auto_assign_cleaning():
        from bluetooth_notification_system import auto_assign_cleaning_tasks
        
        results = auto_assign_cleaning_tasks()
        
        successful = len([r for r in results if r['success']])
        total = len(results)
        
        return jsonify({
            'success': True,
            'message': f'Assegnati {successful}/{total} compiti di pulizia',
            'results': results
        })

    # API per trovare il personale più vicino a un letto
    @app.route('/api/maintenance/nearest_staff', methods=['POST'])
    def find_nearest_maintenance_staff():
        data = request.json
        bed_id = data.get('bed_id')
        
        if not bed_id:
            return jsonify({'error': 'ID letto mancante'}), 400
            
        # Ottieni la posizione del letto
        bed = PostoLetto.query.get(bed_id)
        if not bed:
            return jsonify({'error': 'Letto non trovato'}), 404
        
        # Trova il personale di manutenzione più vicino
        nearest_staff = trova_personale_piu_vicino(
            bed.coordinate_x, 
            bed.coordinate_y, 
            bed.coordinate_z, 
            bed.piano
        )
        
        if nearest_staff:
            # Invia notifica al bracciale (simulato)
            return jsonify({
                'success': True,
                'staff': nearest_staff['staff'],
                'distanza': nearest_staff['distanza'],
                'eta_formatted': nearest_staff['eta_formatted']
            })
        else:
            return jsonify({'error': 'Nessun personale disponibile nelle vicinanze'}), 404

    # API per registrare un nuovo bracciale
    @app.route('/api/maintenance/register_device', methods=['POST'])
    def register_maintenance_device():
        data = request.json
        nome = data.get('nome')
        ruolo = data.get('ruolo', 'Tecnico')
        device_id = data.get('device_id')
        
        if not nome or not device_id:
            return jsonify({'error': 'Nome o device_id mancante'}), 400
        
        # Verifica se il device_id è già registrato
        existing_device = PersonaleManutenzione.query.filter_by(device_id=device_id).first()
        if existing_device:
            return jsonify({'error': 'Dispositivo già registrato'}), 400
        
        # Crea nuovo personale
        new_staff = PersonaleManutenzione(
            nome=nome,
            ruolo=ruolo,
            device_id=device_id,
            disponibile=True
        )
        
        db.session.add(new_staff)
        
        try:
            db.session.commit()
            return jsonify({'success': True, 'staff': new_staff.to_dict()})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # API per aggiornare la disponibilità del personale
    @app.route('/api/maintenance/update_availability', methods=['POST'])
    def update_staff_availability():
        data = request.json
        staff_id = data.get('staff_id')
        disponibile = data.get('disponibile')
        
        if staff_id is None or disponibile is None:
            return jsonify({'error': 'Dati mancanti'}), 400
        
        staff = PersonaleManutenzione.query.get(staff_id)
        if not staff:
            return jsonify({'error': 'Personale non trovato'}), 404
        
        staff.disponibile = bool(disponibile)
        
        try:
            db.session.commit()
            return jsonify({'success': True, 'staff': staff.to_dict()})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500