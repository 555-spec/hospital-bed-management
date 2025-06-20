-- Creazione tabelle
CREATE TABLE IF NOT EXISTS reparti (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    piano INT NOT NULL,
    posti_totali INT NOT NULL
);

CREATE TABLE IF NOT EXISTS posti_letto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reparto_id INT NOT NULL,
    numero VARCHAR(20) NOT NULL,
    stato ENUM('libero','occupato','in_pulizia') NOT NULL,
    FOREIGN KEY (reparto_id) REFERENCES reparti(id)
);

CREATE TABLE IF NOT EXISTS notifica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bed_id INT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending'
);