#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema di Notifiche Bluetooth per Personale Sanitario

Questo modulo gestisce l'invio automatico di notifiche ai braccialetti Bluetooth
del personale sanitario quando un letto necessita di pulizia o manutenzione.
"""

from datetime import datetime, timedelta
from flask import jsonify
import json
import logging
from maintenance_staff import trova_personale_piu_vicino, PersonaleManutenzione

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulazione del sistema Bluetooth
class BluetoothNotificationSystem:
    def __init__(self):
        self.active_notifications = {}
        self.notification_history = []
        
    def send_notification_to_bracelet(self, device_id, message, bed_info, priority="normal"):
        """
        Simula l'invio di una notifica a un braccialetto Bluetooth
        
        Args:
            device_id (str): ID del dispositivo Bluetooth
            message (str): Messaggio da inviare
            bed_info (dict): Informazioni sul letto
            priority (str): Priorità della notifica (low, normal, high, urgent)
        """
        notification = {
            'id': f"notif_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{device_id}",
            'device_id': device_id,
            'message': message,
            'bed_info': bed_info,
            'priority': priority,
            'timestamp': datetime.now().isoformat(),
            'status': 'sent',
            'acknowledged': False
        }
        
        # Salva la notifica attiva
        self.active_notifications[notification['id']] = notification
        self.notification_history.append(notification)
        
        logger.info(f"📡 Notifica inviata a {device_id}: {message}")
        
        return notification
    
    def acknowledge_notification(self, notification_id, staff_id):
        """
        Conferma la ricezione di una notifica
        """
        if notification_id in self.active_notifications:
            self.active_notifications[notification_id]['acknowledged'] = True
            self.active_notifications[notification_id]['acknowledged_at'] = datetime.now().isoformat()
            self.active_notifications[notification_id]['acknowledged_by'] = staff_id
            
            logger.info(f"✅ Notifica {notification_id} confermata da staff {staff_id}")
            return True
        return False
    
    def get_active_notifications(self, device_id=None):
        """
        Ottiene le notifiche attive per un dispositivo specifico o tutti
        """
        if device_id:
            return [n for n in self.active_notifications.values() 
                   if n['device_id'] == device_id and not n['acknowledged']]
        return [n for n in self.active_notifications.values() if not n['acknowledged']]
    
    def clear_old_notifications(self, hours=24):
        """
        Rimuove le notifiche vecchie
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        to_remove = []
        for notif_id, notif in self.active_notifications.items():
            notif_time = datetime.fromisoformat(notif['timestamp'])
            if notif_time < cutoff_time:
                to_remove.append(notif_id)
        
        for notif_id in to_remove:
            del self.active_notifications[notif_id]
        
        logger.info(f"🧹 Rimosse {len(to_remove)} notifiche vecchie")

# Istanza globale del sistema di notifiche
notification_system = BluetoothNotificationSystem()

def notify_nearest_staff_for_bed_cleaning(bed_id, bed_info, urgency="normal"):
    """
    Trova il personale più vicino e invia una notifica per la pulizia del letto
    
    Args:
        bed_id (int): ID del letto
        bed_info (dict): Informazioni complete sul letto
        urgency (str): Livello di urgenza (low, normal, high, urgent)
    """
    try:
        # Trova il personale più vicino
        nearest_staff = trova_personale_piu_vicino(
            bed_info['coordinate_x'],
            bed_info['coordinate_y'], 
            bed_info['coordinate_z'],
            bed_info.get('piano', 1)
        )
        
        if not nearest_staff:
            logger.warning(f"⚠️ Nessun personale disponibile per il letto {bed_id}")
            return {
                'success': False,
                'error': 'Nessun personale disponibile',
                'bed_id': bed_id
            }
        
        staff_info = nearest_staff['staff']
        
        # Crea il messaggio personalizzato
        urgency_icons = {
            'low': '🔵',
            'normal': '🟡', 
            'high': '🟠',
            'urgent': '🔴'
        }
        
        icon = urgency_icons.get(urgency, '🟡')
        
        message = f"{icon} PULIZIA LETTO RICHIESTA\n" \
                 f"Letto: {bed_info['bed_number']}\n" \
                 f"Reparto: {bed_info['department']}\n" \
                 f"Distanza: {nearest_staff['distanza']:.1f}m\n" \
                 f"ETA: {nearest_staff['eta_formatted']}"
        
        # Invia la notifica
        notification = notification_system.send_notification_to_bracelet(
            device_id=staff_info['device_id'],
            message=message,
            bed_info={
                'bed_id': bed_id,
                'bed_number': bed_info['bed_number'],
                'department': bed_info['department'],
                'coordinates': {
                    'x': bed_info['coordinate_x'],
                    'y': bed_info['coordinate_y'],
                    'z': bed_info['coordinate_z'],
                    'piano': bed_info.get('piano', 1)
                }
            },
            priority=urgency
        )
        
        return {
            'success': True,
            'staff': staff_info,
            'notification': notification,
            'distance': nearest_staff['distanza'],
            'eta': nearest_staff['eta_formatted'],
            'bed_id': bed_id
        }
        
    except Exception as e:
        logger.error(f"❌ Errore nell'invio notifica per letto {bed_id}: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'bed_id': bed_id
        }

def auto_assign_cleaning_tasks():
    """
    Funzione per assegnare automaticamente i compiti di pulizia
    basandosi sullo stato dei letti
    """
    from app import PostoLetto
    
    # Trova tutti i letti che necessitano pulizia
    beds_needing_cleaning = PostoLetto.query.filter(
        PostoLetto.status.in_(['maintenance', 'cleaning_required'])
    ).all()
    
    results = []
    
    for bed in beds_needing_cleaning:
        bed_info = {
            'bed_number': bed.bed_number,
            'department': bed.department,
            'coordinate_x': bed.coordinate_x or 0,
            'coordinate_y': bed.coordinate_y or 0,
            'coordinate_z': bed.coordinate_z or 0,
            'piano': bed.piano or 1
        }
        
        # Determina l'urgenza basandosi sullo stato
        urgency = 'high' if bed.status == 'maintenance' else 'normal'
        
        result = notify_nearest_staff_for_bed_cleaning(
            bed_id=bed.id,
            bed_info=bed_info,
            urgency=urgency
        )
        
        results.append(result)
    
    return results

def get_notification_statistics():
    """
    Ottiene statistiche sulle notifiche
    """
    total_notifications = len(notification_system.notification_history)
    active_notifications = len(notification_system.get_active_notifications())
    acknowledged_notifications = len([n for n in notification_system.notification_history if n['acknowledged']])
    
    # Statistiche per priorità
    priority_stats = {}
    for notif in notification_system.notification_history:
        priority = notif['priority']
        priority_stats[priority] = priority_stats.get(priority, 0) + 1
    
    # Statistiche per dispositivo
    device_stats = {}
    for notif in notification_system.notification_history:
        device = notif['device_id']
        device_stats[device] = device_stats.get(device, 0) + 1
    
    return {
        'total_notifications': total_notifications,
        'active_notifications': active_notifications,
        'acknowledged_notifications': acknowledged_notifications,
        'acknowledgment_rate': (acknowledged_notifications / total_notifications * 100) if total_notifications > 0 else 0,
        'priority_distribution': priority_stats,
        'device_distribution': device_stats,
        'last_notification': notification_system.notification_history[-1] if notification_system.notification_history else None
    }

# Funzioni di utilità per l'integrazione con Flask
def init_bluetooth_routes(app, db):
    """
    Inizializza le route per il sistema Bluetooth
    """
    
    @app.route('/api/bluetooth/notify_cleaning', methods=['POST'])
    def api_notify_cleaning():
        from flask import request
        data = request.json
        bed_id = data.get('bed_id')
        urgency = data.get('urgency', 'normal')
        
        if not bed_id:
            return jsonify({'error': 'bed_id richiesto'}), 400
        
        # Ottieni informazioni sul letto
        from app import PostoLetto
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
    
    @app.route('/api/bluetooth/acknowledge', methods=['POST'])
    def api_acknowledge_notification():
        from flask import request
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
    
    @app.route('/api/bluetooth/notifications', methods=['GET'])
    def api_get_notifications():
        from flask import request
        device_id = request.args.get('device_id')
        
        notifications = notification_system.get_active_notifications(device_id)
        return jsonify(notifications)
    
    @app.route('/api/bluetooth/statistics', methods=['GET'])
    def api_get_statistics():
        stats = get_notification_statistics()
        return jsonify(stats)
    
    @app.route('/api/bluetooth/auto_assign', methods=['POST'])
    def api_auto_assign_cleaning():
        results = auto_assign_cleaning_tasks()
        
        successful = len([r for r in results if r['success']])
        total = len(results)
        
        return jsonify({
            'success': True,
            'message': f'Assegnati {successful}/{total} compiti di pulizia',
            'results': results
        })

if __name__ == '__main__':
    # Test del sistema
    print("🧪 Test del Sistema di Notifiche Bluetooth")
    print("=" * 50)
    
    # Simula una notifica
    test_bed_info = {
        'bed_number': 'L001',
        'department': 'Cardiologia',
        'coordinate_x': 100,
        'coordinate_y': 50,
        'coordinate_z': 0,
        'piano': 1
    }
    
    print("📡 Simulazione invio notifica...")
    result = notify_nearest_staff_for_bed_cleaning(1, test_bed_info, 'high')
    
    if result['success']:
        print(f"✅ Notifica inviata con successo a {result['staff']['nome']}")
        print(f"📊 Distanza: {result['distance']:.1f}m, ETA: {result['eta']}")
    else:
        print(f"❌ Errore: {result['error']}")
    
    # Mostra statistiche
    stats = get_notification_statistics()
    print(f"\n📊 Statistiche: {stats['total_notifications']} notifiche totali")