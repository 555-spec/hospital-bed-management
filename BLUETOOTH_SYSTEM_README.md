# 📡 Sistema di Tracciamento Personale Sanitario con Braccialetti Bluetooth

## Panoramica

Il sistema di tracciamento del personale sanitario utilizza braccialetti Bluetooth per monitorare la posizione del personale e inviare notifiche automatiche quando un letto necessita di pulizia o manutenzione.

## 🎯 Funzionalità Principali

### 1. Tracciamento del Personale
- **Braccialetti Bluetooth**: Ogni membro del personale indossa un braccialetto con ID univoco
- **Posizionamento in Tempo Reale**: Coordinate X, Y, Z e piano vengono aggiornate automaticamente
- **Stato di Disponibilità**: Il personale può essere marcato come disponibile/non disponibile

### 2. Sistema di Notifiche Intelligenti
- **Ricerca Automatica**: Trova automaticamente il personale più vicino a un letto
- **Notifiche Prioritizzate**: 4 livelli di priorità (🔵 Bassa, 🟡 Normale, 🟠 Alta, 🔴 Urgente)
- **Calcolo ETA**: Stima del tempo di arrivo basato sulla distanza e velocità media
- **Conferma Ricezione**: Il personale può confermare la ricezione delle notifiche

### 3. Assegnazione Automatica
- **Scansione Automatica**: Identifica tutti i letti che necessitano pulizia
- **Assegnazione Ottimale**: Assegna automaticamente il personale più vicino disponibile
- **Reportistica**: Fornisce risultati dettagliati dell'assegnazione

## 🏗️ Architettura del Sistema

### Backend Components

#### 1. `maintenance_staff.py`
- **Modello PersonaleManutenzione**: Gestisce i dati del personale
- **Funzione trova_personale_piu_vicino**: Algoritmo di ricerca del personale più vicino
- **Calcolo Distanze**: Include penalità per piani diversi

#### 2. `bluetooth_notification_system.py`
- **BluetoothNotificationSystem**: Classe principale per gestire le notifiche
- **Simulazione Bluetooth**: Simula l'invio di notifiche ai braccialetti
- **Gestione Storico**: Mantiene cronologia delle notifiche
- **Statistiche**: Calcola metriche di performance

#### 3. `maintenance_api.py`
- **API REST**: Endpoint per tutte le operazioni
- **Integrazione**: Collega il sistema di notifiche con il database

### Frontend Components

#### 1. `MaintenanceStaffPanel.js`
- **Interfaccia Utente**: Pannello completo per gestire il personale
- **Visualizzazione Notifiche**: Accordion per mostrare notifiche attive
- **Statistiche Real-time**: Dashboard con metriche aggiornate
- **Controlli Manuali**: Pulsanti per operazioni manuali

## 🚀 Come Utilizzare il Sistema

### 1. Popolamento Iniziale del Database

```bash
# Esegui lo script per popolare il database con personale di esempio
cd src/backend
python populate_maintenance_staff.py
```

### 2. Registrazione di Nuovo Personale

1. Vai al pannello "Sistema di Tracciamento Personale Sanitario"
2. Clicca su "Registra Bracciale"
3. Inserisci nome e ruolo del personale
4. Il sistema genererà automaticamente un ID dispositivo

### 3. Monitoraggio delle Notifiche

1. Clicca sul pulsante "🔔 Notifiche" per visualizzare le notifiche attive
2. Le notifiche sono organizzate per priorità con icone colorate
3. Ogni notifica mostra:
   - Letto e reparto interessato
   - Messaggio dettagliato
   - Dispositivo assegnato
   - Timestamp
   - Stato di conferma

### 4. Assegnazione Automatica

1. Clicca su "🪄 Assegna Auto" per avviare l'assegnazione automatica
2. Il sistema:
   - Scansiona tutti i letti che necessitano pulizia
   - Trova il personale più vicino disponibile per ogni letto
   - Invia notifiche automatiche
   - Mostra un report dei risultati

## 📊 API Endpoints

### Gestione Personale
- `GET /api/maintenance/staff` - Lista tutto il personale
- `POST /api/maintenance/register_device` - Registra nuovo bracciale
- `POST /api/maintenance/update_position` - Aggiorna posizione
- `POST /api/maintenance/update_availability` - Cambia disponibilità

### Sistema Notifiche
- `POST /api/maintenance/notify_cleaning` - Invia notifica per pulizia
- `POST /api/maintenance/acknowledge_notification` - Conferma notifica
- `GET /api/maintenance/notifications` - Ottieni notifiche attive
- `GET /api/maintenance/notification_stats` - Statistiche notifiche

### Automazione
- `POST /api/maintenance/auto_assign_cleaning` - Assegnazione automatica
- `POST /api/maintenance/nearest_staff` - Trova personale più vicino

## 🔧 Configurazione

### Parametri del Sistema

```python
# In bluetooth_notification_system.py
VELOCITA_MEDIA = 1.2  # m/s - velocità media del personale
PENALITA_PIANO = 30   # secondi extra per cambiare piano
TIMEOUT_NOTIFICA = 24 # ore prima di rimuovere notifiche vecchie
```

### Livelli di Priorità

- **🔵 Bassa (low)**: Pulizia di routine
- **🟡 Normale (normal)**: Pulizia standard dopo dimissione
- **🟠 Alta (high)**: Pulizia urgente per nuovo paziente
- **🔴 Urgente (urgent)**: Emergenza o situazione critica

## 📈 Metriche e Statistiche

Il sistema traccia automaticamente:

- **Notifiche Totali**: Numero totale di notifiche inviate
- **Notifiche Attive**: Notifiche in attesa di conferma
- **Notifiche Confermate**: Notifiche confermate dal personale
- **Tasso di Conferma**: Percentuale di notifiche confermate
- **Distribuzione per Priorità**: Breakdown per livello di priorità
- **Distribuzione per Dispositivo**: Carico di lavoro per dispositivo

## 🛠️ Simulazione e Testing

### Simulazione Movimento

Il sistema include una funzione di simulazione che:
- Muove automaticamente il personale in posizioni casuali
- Aggiorna le coordinate ogni 5 secondi
- Utile per testing e dimostrazione

### Test del Sistema

```python
# Esegui il test del sistema di notifiche
cd src/backend
python bluetooth_notification_system.py
```

## 🔮 Sviluppi Futuri

### Integrazioni Pianificate
- **Bluetooth Reale**: Integrazione con hardware Bluetooth reale
- **Beacon Indoor**: Sistema di posizionamento indoor più preciso
- **App Mobile**: App per il personale per ricevere notifiche
- **Analytics Avanzati**: Machine learning per ottimizzare assegnazioni

### Miglioramenti
- **Geofencing**: Zone virtuali per aree specifiche
- **Escalation**: Notifiche automatiche se non confermate
- **Integrazione Calendario**: Considerare turni e disponibilità
- **Reportistica**: Report dettagliati su performance e tempi

## 🆘 Troubleshooting

### Problemi Comuni

1. **Nessun Personale Disponibile**
   - Verifica che ci sia personale registrato
   - Controlla che il personale sia marcato come "disponibile"
   - Esegui lo script di popolamento se necessario

2. **Notifiche Non Visualizzate**
   - Controlla la connessione al backend
   - Verifica che le API siano attive
   - Controlla la console browser per errori

3. **Posizioni Non Aggiornate**
   - Verifica che la simulazione sia attiva
   - Controlla gli endpoint di aggiornamento posizione
   - Verifica i log del backend

## 📞 Supporto

Per supporto tecnico o domande sul sistema:
- Controlla i log del backend in `src/backend/`
- Verifica la console del browser per errori frontend
- Consulta la documentazione API per dettagli sugli endpoint

---

**Nota**: Questo è un sistema di simulazione per scopi dimostrativi. Per un ambiente di produzione, sarà necessaria l'integrazione con hardware Bluetooth reale e sistemi di posizionamento indoor.