#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script di diagnosi completa e risoluzione problemi
"""

import sys
import os
import subprocess
import pathlib
import sqlite3
from datetime import datetime

def print_header(title):
    print("\n" + "=" * 60)
    print(f"🔍 {title}")
    print("=" * 60)

def print_step(step, description):
    print(f"\n📋 Passo {step}: {description}")
    print("-" * 40)

def check_python():
    """Verifica installazione Python"""
    print_step(1, "Verifica Python")
    try:
        version = sys.version
        print(f"✅ Python installato: {version}")
        return True
    except Exception as e:
        print(f"❌ Errore Python: {e}")
        return False

def check_pip():
    """Verifica pip"""
    print_step(2, "Verifica pip")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ pip disponibile: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ pip non funziona: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Errore pip: {e}")
        return False

def install_dependencies():
    """Installa dipendenze essenziali"""
    print_step(3, "Installazione dipendenze")
    
    essential_packages = [
        'Flask==2.3.2',
        'Flask-SQLAlchemy==3.0.3',
        'Flask-CORS==4.0.0',
        'python-dotenv==1.0.0'
    ]
    
    for package in essential_packages:
        try:
            print(f"📦 Installando {package}...")
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"✅ {package} installato")
            else:
                print(f"⚠️ Problema con {package}: {result.stderr}")
        except Exception as e:
            print(f"❌ Errore installazione {package}: {e}")
    
    return True

def check_project_structure():
    """Verifica struttura del progetto"""
    print_step(4, "Verifica struttura progetto")
    
    base_path = pathlib.Path(__file__).parent
    required_paths = [
        'src/backend',
        'src/frontend',
        'src/database'
    ]
    
    all_good = True
    for path in required_paths:
        full_path = base_path / path
        if full_path.exists():
            print(f"✅ {path} esiste")
        else:
            print(f"❌ {path} mancante")
            all_good = False
            # Crea la directory se mancante
            try:
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"🔧 Creato {path}")
            except Exception as e:
                print(f"❌ Impossibile creare {path}: {e}")
    
    return all_good

def check_database():
    """Verifica e crea database"""
    print_step(5, "Verifica database")
    
    database_dir = pathlib.Path(__file__).parent / 'src' / 'database'
    database_file = database_dir / 'hospital.db'
    
    try:
        # Crea directory se non esiste
        database_dir.mkdir(parents=True, exist_ok=True)
        
        # Verifica se il database esiste
        if database_file.exists():
            print(f"✅ Database esiste: {database_file}")
            
            # Verifica contenuto
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()
            
            # Controlla tabelle
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"📊 Tabelle trovate: {[t[0] for t in tables]}")
            
            # Controlla personale
            try:
                cursor.execute("SELECT COUNT(*) FROM personale_manutenzione;")
                count = cursor.fetchone()[0]
                print(f"👥 Personale nel database: {count}")
                
                if count == 0:
                    print("⚠️ Database vuoto, necessario popolamento")
                    return False
                else:
                    print("✅ Database popolato")
                    return True
                    
            except sqlite3.OperationalError:
                print("⚠️ Tabella personale_manutenzione non esiste")
                return False
            finally:
                conn.close()
        else:
            print(f"⚠️ Database non esiste: {database_file}")
            return False
            
    except Exception as e:
        print(f"❌ Errore database: {e}")
        return False

def create_and_populate_database():
    """Crea e popola il database"""
    print_step(6, "Creazione e popolamento database")
    
    try:
        # Importa e configura Flask app
        sys.path.append(str(pathlib.Path(__file__).parent / 'src' / 'backend'))
        
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        database_dir = pathlib.Path(__file__).parent / 'src' / 'database'
        database_dir.mkdir(exist_ok=True)
        database_file = database_dir / 'hospital.db'
        
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_file}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)
        
        # Definisci modello
        class PersonaleManutenzione(db.Model):
            __tablename__ = 'personale_manutenzione'
            
            id = db.Column(db.Integer, primary_key=True)
            nome = db.Column(db.String(100), nullable=False)
            ruolo = db.Column(db.String(50), nullable=False)
            disponibile = db.Column(db.Boolean, default=True)
            coordinate_x = db.Column(db.Float, default=0)
            coordinate_y = db.Column(db.Float, default=0)
            coordinate_z = db.Column(db.Float, default=0)
            piano = db.Column(db.Integer, default=1)
            device_id = db.Column(db.String(20), unique=True, nullable=False)
            ultimo_aggiornamento = db.Column(db.DateTime, default=datetime.utcnow)
        
        with app.app_context():
            # Crea tabelle
            db.create_all()
            print("✅ Tabelle create")
            
            # Popola con personale
            personale_data = [
                {'nome': 'Dr. Marco Rossi', 'ruolo': 'Medico', 'device_id': 'MED001', 'coordinate_x': 150, 'coordinate_y': 200, 'piano': 1},
                {'nome': 'Inf. Sara Bianchi', 'ruolo': 'Infermiere', 'device_id': 'INF001', 'coordinate_x': 250, 'coordinate_y': 200, 'piano': 1},
                {'nome': 'Dr.ssa Elena Verdi', 'ruolo': 'Cardiologo', 'device_id': 'CAR001', 'coordinate_x': 180, 'coordinate_y': 180, 'piano': 1},
                {'nome': 'Inf. Luca Neri', 'ruolo': 'Infermiere', 'device_id': 'INF002', 'coordinate_x': 150, 'coordinate_y': 280, 'piano': 1},
                {'nome': 'OSS Maria Gialli', 'ruolo': 'OSS', 'device_id': 'OSS001', 'coordinate_x': 200, 'coordinate_y': 250, 'piano': 1},
                {'nome': 'Tecnico Paolo Blu', 'ruolo': 'Tecnico', 'device_id': 'TEC001', 'coordinate_x': 100, 'coordinate_y': 100, 'piano': 1},
                {'nome': 'Inf. Giulia Rosa', 'ruolo': 'Infermiere', 'device_id': 'INF003', 'coordinate_x': 300, 'coordinate_y': 150, 'piano': 1},
                {'nome': 'OSS Antonio Viola', 'ruolo': 'OSS', 'device_id': 'OSS002', 'coordinate_x': 120, 'coordinate_y': 300, 'piano': 1},
                {'nome': 'Coord. Francesca Oro', 'ruolo': 'Coordinatore', 'device_id': 'COORD001', 'coordinate_x': 200, 'coordinate_y': 200, 'piano': 1},
                {'nome': 'Inf. Roberto Argento', 'ruolo': 'Infermiere', 'device_id': 'INF004', 'coordinate_x': 280, 'coordinate_y': 280, 'piano': 1}
            ]
            
            # Rimuovi personale esistente
            PersonaleManutenzione.query.delete()
            
            # Aggiungi nuovo personale
            for persona in personale_data:
                nuovo_personale = PersonaleManutenzione(
                    nome=persona['nome'],
                    ruolo=persona['ruolo'],
                    device_id=persona['device_id'],
                    coordinate_x=persona['coordinate_x'],
                    coordinate_y=persona['coordinate_y'],
                    coordinate_z=0,
                    piano=persona['piano'],
                    disponibile=True,
                    ultimo_aggiornamento=datetime.now()
                )
                db.session.add(nuovo_personale)
                print(f"✅ Aggiunto: {persona['nome']} ({persona['ruolo']})")
            
            db.session.commit()
            
            # Verifica finale
            count = PersonaleManutenzione.query.count()
            print(f"🎉 Database popolato con {count} membri del personale")
            
            return True
            
    except Exception as e:
        print(f"❌ Errore nella creazione database: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_backend_files():
    """Verifica file backend essenziali"""
    print_step(7, "Verifica file backend")
    
    backend_dir = pathlib.Path(__file__).parent / 'src' / 'backend'
    required_files = ['app.py', 'maintenance_api.py', 'maintenance_staff.py']
    
    all_good = True
    for file in required_files:
        file_path = backend_dir / file
        if file_path.exists():
            print(f"✅ {file} esiste")
        else:
            print(f"❌ {file} mancante")
            all_good = False
    
    return all_good

def test_backend_import():
    """Testa importazione moduli backend"""
    print_step(8, "Test importazione backend")
    
    try:
        sys.path.append(str(pathlib.Path(__file__).parent / 'src' / 'backend'))
        
        print("📦 Importando Flask...")
        from flask import Flask
        print("✅ Flask importato")
        
        print("📦 Importando Flask-SQLAlchemy...")
        from flask_sqlalchemy import SQLAlchemy
        print("✅ Flask-SQLAlchemy importato")
        
        print("📦 Importando Flask-CORS...")
        from flask_cors import CORS
        print("✅ Flask-CORS importato")
        
        return True
        
    except ImportError as e:
        print(f"❌ Errore importazione: {e}")
        return False
    except Exception as e:
        print(f"❌ Errore generico: {e}")
        return False

def create_startup_script():
    """Crea script di avvio semplificato"""
    print_step(9, "Creazione script avvio")
    
    script_content = '''@echo off
echo Avvio sistema ospedaliero...
echo.

echo Installazione dipendenze...
python -m pip install Flask==2.3.2 Flask-SQLAlchemy==3.0.3 Flask-CORS==4.0.0 python-dotenv==1.0.0

echo.
echo Avvio backend...
cd src\\backend
python app.py

echo.
echo Se ci sono errori, controlla i log sopra.
pause
'''
    
    try:
        script_path = pathlib.Path(__file__).parent / 'start_system.bat'
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        print(f"✅ Script creato: {script_path}")
        return True
    except Exception as e:
        print(f"❌ Errore creazione script: {e}")
        return False

def main():
    """Funzione principale di diagnosi"""
    print_header("DIAGNOSI E RISOLUZIONE PROBLEMI SISTEMA OSPEDALIERO")
    
    results = []
    
    # Esegui tutti i controlli
    results.append(("Python", check_python()))
    results.append(("pip", check_pip()))
    results.append(("Dipendenze", install_dependencies()))
    results.append(("Struttura", check_project_structure()))
    results.append(("Database", check_database()))
    
    # Se database è vuoto, popolalo
    if not results[-1][1]:
        results.append(("Popolamento DB", create_and_populate_database()))
    
    results.append(("File Backend", check_backend_files()))
    results.append(("Import Backend", test_backend_import()))
    results.append(("Script Avvio", create_startup_script()))
    
    # Riepilogo
    print_header("RIEPILOGO DIAGNOSI")
    
    all_ok = True
    for name, status in results:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name}: {'OK' if status else 'PROBLEMA'}")
        if not status:
            all_ok = False
    
    print("\n" + "=" * 60)
    
    if all_ok:
        print("🎉 SISTEMA PRONTO!")
        print("\n📋 Prossimi passi:")
        print("   1. Esegui 'start_system.bat' per avviare il backend")
        print("   2. Apri il frontend e vai alla sezione Manutenzione")
        print("   3. Dovresti vedere la lista del personale")
    else:
        print("⚠️ PROBLEMI RILEVATI")
        print("\n🔧 Azioni consigliate:")
        print("   1. Controlla i messaggi di errore sopra")
        print("   2. Assicurati di avere i permessi di amministratore")
        print("   3. Verifica la connessione internet per l'installazione")
        print("   4. Riavvia il computer se necessario")
    
    print("\n" + "=" * 60)
    input("\nPremi INVIO per chiudere...")

if __name__ == '__main__':
    main()