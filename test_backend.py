#!/usr/bin/env python3
"""
Script di test per verificare se il backend è in esecuzione
"""

import requests
import json
from datetime import datetime

def test_backend():
    base_url = "http://localhost:5000"
    
    print("🔍 Test di connessione al backend...")
    print(f"📡 URL base: {base_url}")
    print("=" * 50)
    
    # Test 1: Endpoint base
    try:
        print("\n1️⃣ Test endpoint base...")
        response = requests.get(f"{base_url}/api/beds", timeout=5)
        if response.status_code == 200:
            beds = response.json()
            print(f"✅ Endpoint /api/beds funziona - {len(beds)} letti trovati")
        else:
            print(f"❌ Endpoint /api/beds errore: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ ERRORE: Backend non in esecuzione su localhost:5000")
        print("💡 Soluzione: Esegui 'quick_start.bat' per avviare il backend")
        return False
    except Exception as e:
        print(f"❌ Errore imprevisto: {e}")
        return False
    
    # Test 2: Endpoint personale manutenzione
    try:
        print("\n2️⃣ Test endpoint personale manutenzione...")
        response = requests.get(f"{base_url}/api/maintenance/staff", timeout=5)
        if response.status_code == 200:
            staff = response.json()
            print(f"✅ Endpoint /api/maintenance/staff funziona - {len(staff)} membri trovati")
            
            if len(staff) == 0:
                print("⚠️  ATTENZIONE: Nessun personale trovato nel database")
                print("💡 Il database potrebbe non essere inizializzato correttamente")
            else:
                print("\n👥 Personale trovato:")
                for person in staff[:3]:  # Mostra solo i primi 3
                    print(f"   - {person.get('nome', 'N/A')} ({person.get('ruolo', 'N/A')}) - {person.get('device_id', 'N/A')}")
                if len(staff) > 3:
                    print(f"   ... e altri {len(staff) - 3} membri")
        else:
            print(f"❌ Endpoint /api/maintenance/staff errore: {response.status_code}")
            print(f"📄 Risposta: {response.text}")
    except Exception as e:
        print(f"❌ Errore nel test personale: {e}")
    
    # Test 3: Endpoint notifiche
    try:
        print("\n3️⃣ Test endpoint notifiche...")
        response = requests.get(f"{base_url}/api/maintenance/notifications", timeout=5)
        if response.status_code == 200:
            notifications = response.json()
            print(f"✅ Endpoint /api/maintenance/notifications funziona - {len(notifications)} notifiche")
        else:
            print(f"❌ Endpoint notifiche errore: {response.status_code}")
    except Exception as e:
        print(f"❌ Errore nel test notifiche: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Test completato!")
    print("\n💡 Se tutti i test passano ma la pagina è vuota:")
    print("   1. Controlla la console del browser (F12)")
    print("   2. Verifica che il frontend sia su http://localhost:3000")
    print("   3. Controlla le impostazioni CORS")
    
    return True

if __name__ == "__main__":
    test_backend()
    input("\nPremi INVIO per chiudere...")