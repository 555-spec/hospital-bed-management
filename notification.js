// Registra Service Worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').then(() => {
        console.log('Service Worker registrato');
    });
}

// Funzione per sincronizzazione
async function syncNotifications() {
    const lastSync = localStorage.getItem('lastSync') || null;
    
    try {
        const response = await fetch('/api/sync_notifications', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ last_sync: lastSync })
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            // Salva notifiche in IndexedDB
            await saveNotificationsToIDB(data.notifications);
            localStorage.setItem('lastSync', data.server_time);
        }
    } catch (error) {
        console.error('Errore sincronizzazione:', error);
    }
}

// Sincronizza ogni 5 minuti e all'avvio
setInterval(syncNotifications, 5 * 60 * 1000);
syncNotifications();