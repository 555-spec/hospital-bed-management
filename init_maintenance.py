#!/usr/bin/env python3
"""
Script per inizializzare il database con il personale di manutenzione
"""

import sys
import os

# Aggiungi il percorso del backend al PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from maintenance_staff import PersonaleManutenzione

def init_maintenance_staff():
    """Inizializza il database con il personale di manutenzione"""
    
    # Lista del personale di manutenzione da creare
    personale_da_creare = [
        {
            'nome': 'Marco Tecnico',
            'ruolo': 'Tecnico Senior',
            'device_id': 'BT001',
            'coordinate_x': -5,
            'coordinate_y': 0,
            'coordinate_z': -2,
            'piano': 1
        },
        {
            'nome': 'Laura Manutenzione',
            'ruolo': 'Tecnico Junior',
            'device_id': 'BT002',
            'coordinate_x': 2,
            'coordinate_y': 0,
            'coordinate_z': 3,
            'piano': 2
        },
        {
            'nome': 'Giovanni Supporto',
            'ruolo': 'Tecnico Specializzato',
            'device_id': 'BT003',
            'coordinate_x': -1,
            'coordinate_y': 0,
            'coordinate_z': 5,
            'piano': 3
        },
        {
            'nome': 'Francesca Assistenza',
            'ruolo': 'Tecnico',
            'device_id': 'BT004',
            'coordinate_x': 4,
            'coordinate_y': 0,
            'coordinate_z': -3,
            'piano': 1
        },
        {
            'nome': 'Roberto Riparazioni',
            'ruolo': 'Capo Tecnico',
            'device_id': 'BT005',
            'coordinate_x': 0,
            'coordinate_y': 0,
            'coordinate_z': 0,
            'piano': 2
        }
    ]
    
    with app.app_context():
        try:
            # Crea tutte le tabelle se non esistono
            db.create_all()
            print("Database inizializzato.")
            
            # Verifica se il personale esiste già
            existing_count = PersonaleManutenzione.query.count()
            if existing_count > 0:
                print(f"Trovati {existing_count} membri del personale esistenti.")
                return
            
            # Crea il personale di manutenzione
            for persona in personale_da_creare:
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
                print(f"Aggiunto: {persona['nome']} - {persona['device_id']}")
            
            # Commit delle modifiche
            db.session.commit()
            print(f"\nPersonale di manutenzione creato con successo! ({len(personale_da_creare)} membri)")
            
            # Verifica finale
            total_staff = PersonaleManutenzione.query.count()
            print(f"Totale membri del personale nel database: {total_staff}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Errore durante l'inizializzazione: {str(e)}")
            return False
    
    return True

if __name__ == '__main__':
    print("Inizializzazione del personale di manutenzione...")
    success = init_maintenance_staff()
    if success:
        print("Inizializzazione completata con successo!")
    else:
        print("Inizializzazione fallita.")
        sys.exit(1)