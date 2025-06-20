#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per correggere i timestamp None nel database
"""

import sqlite3
import os
from datetime import datetime

def fix_timestamps():
    # Percorso del database
    db_path = os.path.join('src', 'database', 'hospital.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database non trovato: {db_path}")
        return False
    
    try:
        # Connessione al database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Timestamp corrente
        current_timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        
        print("🔧 Correzione timestamp None...")
        
        # Correggi timestamp None nella tabella paziente
        cursor.execute("""
            UPDATE paziente 
            SET timestamp = ? 
            WHERE timestamp IS NULL
        """, (current_timestamp,))
        
        pazienti_aggiornati = cursor.rowcount
        print(f"✅ Aggiornati {pazienti_aggiornati} pazienti con timestamp None")
        
        # Correggi timestamp None nella tabella notifica
        cursor.execute("""
            UPDATE notifica 
            SET timestamp = ? 
            WHERE timestamp IS NULL
        """, (current_timestamp,))
        
        notifiche_aggiornate = cursor.rowcount
        print(f"✅ Aggiornate {notifiche_aggiornate} notifiche con timestamp None")
        
        # Commit delle modifiche
        conn.commit()
        
        # Verifica finale
        cursor.execute("SELECT COUNT(*) FROM paziente WHERE timestamp IS NULL")
        pazienti_null = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM notifica WHERE timestamp IS NULL")
        notifiche_null = cursor.fetchone()[0]
        
        print(f"\n📊 Verifica finale:")
        print(f"   - Pazienti con timestamp None: {pazienti_null}")
        print(f"   - Notifiche con timestamp None: {notifiche_null}")
        
        if pazienti_null == 0 and notifiche_null == 0:
            print("\n✅ Tutti i timestamp sono stati corretti con successo!")
        else:
            print("\n⚠️  Alcuni timestamp potrebbero non essere stati corretti")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Errore durante la correzione: {e}")
        return False

if __name__ == "__main__":
    print("======================================")
    print("    CORREZIONE TIMESTAMP DATABASE")
    print("======================================")
    
    success = fix_timestamps()
    
    if success:
        print("\n🎉 Correzione completata!")
        print("\n💡 Suggerimenti:")
        print("   1. Riavvia il backend se è in esecuzione")
        print("   2. Testa gli endpoint /api/waiting_patients e /api/get_pending_notifications")
        print("   3. Verifica che non ci siano più errori 500")
    else:
        print("\n❌ Correzione fallita. Controlla i messaggi di errore sopra.")
    
    input("\nPremi INVIO per chiudere...")