# Setup Sistema Braccialetti Bluetooth - Personale Manutenzione

## Problema: Sezione Personale Manutenzione Vuota

Se la sezione "Personale Manutenzione" appare vuota, segui questi passaggi per risolvere:

## 1. Avvia il Backend

Apri un terminale nella directory del backend:
```bash
cd "c:\Users\Cinzia Del Fonso\Desktop\hospital-bed-management\src\backend"
python app.py
```

Il server dovrebbe avviarsi su `http://localhost:5000`

## 2. Inizializza il Database

In un nuovo terminale, esegui lo script di inizializzazione:
```bash
cd "c:\Users\Cinzia Del Fonso\Desktop\hospital-bed-management\src\backend"
python init_maintenance.py
```

Questo creerà 5 membri del personale di manutenzione con i seguenti bracciali:
- Marco Tecnico (BT001) - Tecnico Senior
- Laura Manutenzione (BT002) - Tecnico Junior  
- Giovanni Supporto (BT003) - Tecnico Specializzato
- Francesca Assistenza (BT004) - Tecnico
- Roberto Riparazioni (BT005) - Capo Tecnico

## 3. Avvia il Frontend

In un altro terminale:
```bash
cd "c:\Users\Cinzia Del Fonso\Desktop\hospital-bed-management\src\frontend"
npm start
```

## 4. Verifica il Sistema

1. Apri il browser su `http://localhost:3000`
2. Naviga su "Personale Manutenzione" dal menu
3. Dovresti vedere la tabella con i 5 membri del personale

## Funzionalità Disponibili

### Visualizzazione Personale
- Tabella con posizioni 3D in tempo reale
- Stato di disponibilità
- Ultimo aggiornamento posizione
- ID dispositivo bracciale

### Registrazione Nuovi Bracciali
- Clicca "Registra Bracciale"
- Inserisci nome, ruolo e ID dispositivo
- Il personale verrà aggiunto automaticamente

### Ricerca Personale Più Vicino
- Clicca "Trova Personale Vicino"
- Inserisci ID di un letto
- Il sistema calcolerà distanza e tempo di arrivo

### Simulazione Movimento
- Clicca "Avvia Simulazione" per simulare il movimento dei bracciali
- Le posizioni si aggiorneranno ogni 5 secondi
- Clicca "Ferma Simulazione" per interrompere

## Risoluzione Problemi

### Errore "Backend non disponibile"
- Verifica che il server backend sia in esecuzione
- Controlla che non ci siano errori nel terminale del backend
- Assicurati che la porta 5000 non sia occupata

### Errore "Database non inizializzato"
- Esegui lo script `init_maintenance.py`
- Verifica che il file `hospital.db` esista in `src/database/`
- Controlla i permessi di scrittura nella directory

### Sezione ancora vuota dopo l'inizializzazione
- Ricarica la pagina del browser
- Controlla la console del browser per errori JavaScript
- Verifica che le API rispondano visitando `http://localhost:5000/api/maintenance/staff`

## API Endpoints

- `GET /api/maintenance/staff` - Lista personale
- `POST /api/maintenance/update_position` - Aggiorna posizione
- `POST /api/maintenance/nearest_staff` - Trova personale più vicino
- `POST /api/maintenance/register_device` - Registra nuovo bracciale
- `POST /api/maintenance/update_availability` - Aggiorna disponibilità

## File Modificati

### Backend
- `app.py` - Aggiunto import dei moduli di manutenzione
- `maintenance_staff.py` - Modello PersonaleManutenzione
- `maintenance_api.py` - API endpoints
- `init_maintenance.py` - Script di inizializzazione

### Frontend
- `App.js` - Aggiunta rotta /maintenance
- `Navigation.js` - Aggiunto link menu
- `MaintenanceStaffPanel.js` - Componente principale
- `maintenanceApi.js` - Servizi API

## Prossimi Passi

1. Integrare con veri dispositivi Bluetooth BLE
2. Implementare notifiche push ai bracciali
3. Aggiungere mappe 3D per visualizzazione posizioni
4. Implementare algoritmi di ottimizzazione percorsi
5. Aggiungere analytics e reportistica