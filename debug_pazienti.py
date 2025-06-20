import sqlite3
import os
import requests
import json

# Percorso del database
db_path = os.path.join('src', 'database', 'hospital.db')

print("🔍 DEBUG: Problema caricamento pazienti in attesa")
print("=" * 50)

# 1. Verifica esistenza database
print("\n1️⃣ Controllo database...")
if not os.path.exists(db_path):
    print("❌ Database non trovato!")
    print(f"   Percorso cercato: {db_path}")
    exit(1)
else:
    print(f"✅ Database trovato: {db_path}")

# 2. Verifica contenuto tabella pazienti
print("\n2️⃣ Controllo tabella pazienti...")
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verifica se la tabella esiste
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='paziente';")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("❌ Tabella 'paziente' non trovata!")
        print("   Tabelle disponibili:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(f"   - {table[0]}")
    else:
        print("✅ Tabella 'paziente' trovata")
        
        # Conta tutti i pazienti
        cursor.execute("SELECT COUNT(*) FROM paziente")
        total_patients = cursor.fetchone()[0]
        print(f"   📊 Totale pazienti: {total_patients}")
        
        # Conta pazienti in attesa (non assegnati)
        cursor.execute("SELECT COUNT(*) FROM paziente WHERE assegnato = 0 OR assegnato = 'false'")
        waiting_patients = cursor.fetchone()[0]
        print(f"   ⏳ Pazienti in attesa: {waiting_patients}")
        
        # Mostra dettagli pazienti in attesa
        if waiting_patients > 0:
            print("\n   📋 Dettagli pazienti in attesa:")
            cursor.execute("""
                SELECT id, nome, gravita, reparto_richiesto, assegnato, bed_id 
                FROM paziente 
                WHERE assegnato = 0 OR assegnato = 'false'
            """)
            patients = cursor.fetchall()
            for p in patients:
                print(f"      - ID: {p[0]}, Nome: {p[1]}, Gravità: {p[2]}, Reparto: {p[3]}, Assegnato: {p[4]}, Letto: {p[5]}")
        else:
            print("   ℹ️ Nessun paziente in attesa trovato")
            
            # Mostra tutti i pazienti per debug
            cursor.execute("SELECT id, nome, gravita, reparto_richiesto, assegnato, bed_id FROM paziente LIMIT 5")
            all_patients = cursor.fetchall()
            if all_patients:
                print("\n   📋 Primi 5 pazienti (tutti):")
                for p in all_patients:
                    print(f"      - ID: {p[0]}, Nome: {p[1]}, Gravità: {p[2]}, Reparto: {p[3]}, Assegnato: {p[4]}, Letto: {p[5]}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Errore accesso database: {e}")
    if 'conn' in locals():
        conn.close()

# 3. Verifica connessione backend
print("\n3️⃣ Controllo backend...")
backend_url = "http://localhost:5000"

try:
    # Test connessione base
    response = requests.get(f"{backend_url}/api/beds", timeout=5)
    if response.status_code == 200:
        print("✅ Backend raggiungibile")
        beds_data = response.json()
        print(f"   📊 Letti restituiti: {len(beds_data)}")
    else:
        print(f"⚠️ Backend risponde ma con errore: {response.status_code}")
        print(f"   Risposta: {response.text[:200]}")
except requests.exceptions.ConnectionError:
    print("❌ Backend non raggiungibile")
    print("   💡 Suggerimento: Avvia il backend con 'start_backend.bat'")
except requests.exceptions.Timeout:
    print("❌ Timeout connessione backend")
except Exception as e:
    print(f"❌ Errore connessione backend: {e}")

# 4. Test specifico endpoint pazienti
print("\n4️⃣ Test endpoint pazienti...")
try:
    response = requests.get(f"{backend_url}/api/waiting_patients", timeout=5)
    if response.status_code == 200:
        patients_data = response.json()
        print("✅ Endpoint pazienti funzionante")
        print(f"   📊 Pazienti restituiti: {len(patients_data)}")
        
        if patients_data:
            print("   📋 Primi pazienti:")
            for i, patient in enumerate(patients_data[:3]):
                print(f"      {i+1}. {patient.get('nome', 'N/A')} - Gravità: {patient.get('gravita', 'N/A')} - Reparto: {patient.get('reparto_richiesto', 'N/A')}")
        else:
            print("   ℹ️ Nessun paziente in attesa restituito dall'API")
    else:
        print(f"❌ Endpoint pazienti errore: {response.status_code}")
        print(f"   Risposta: {response.text[:200]}")
except requests.exceptions.ConnectionError:
    print("❌ Backend non raggiungibile per endpoint pazienti")
except Exception as e:
    print(f"❌ Errore test endpoint pazienti: {e}")

# 5. Suggerimenti risoluzione
print("\n" + "=" * 50)
print("💡 SUGGERIMENTI PER RISOLVERE IL PROBLEMA:")
print("\n1. Se il database è vuoto o non ha pazienti:")
print("   → Esegui: check_and_populate.bat")
print("\n2. Se il backend non è raggiungibile:")
print("   → Esegui: start_backend.bat")
print("\n3. Se il backend è attivo ma l'endpoint non funziona:")
print("   → Controlla i log del backend per errori")
print("   → Verifica che la porta 5000 non sia occupata")
print("\n4. Se i pazienti esistono ma non sono 'in attesa':")
print("   → Potrebbero essere già assegnati (assegnato=True)")
print("   → Usa lo script per ripopolare il database")

print("\n🔧 DEBUG COMPLETATO")