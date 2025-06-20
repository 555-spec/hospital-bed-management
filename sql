DELETE FROM personale_manutenzione;

INSERT INTO personale_manutenzione (nome, ruolo, device_id, disponibile, coordinate_x, coordinate_y, coordinate_z, piano, ultimo_aggiornamento) VALUES 
('Marco Rossi', 'OSS', 'BT_OSS_001', 1, 50.0, 80.0, 0.0, 1, datetime('now')),
('Giulia Bianchi', 'Infermiere', 'BT_INF_001', 1, 80.0, 120.0, 0.0, 1, datetime('now')),
('Andrea Verdi', 'OSS', 'BT_OSS_002', 1, 120.0, 60.0, 0.0, 1, datetime('now')),
('Sara Neri', 'Infermiere', 'BT_INF_002', 1, 150.0, 100.0, 0.0, 1, datetime('now')),
('Luca Ferrari', 'OSS', 'BT_OSS_003', 1, 200.0, 150.0, 0.0, 1, datetime('now')),
('Elena Conti', 'Infermiere', 'BT_INF_003', 1, 180.0, 200.0, 0.0, 1, datetime('now')),
('Roberto Mancini', 'OSS', 'BT_OSS_004', 1, 250.0, 120.0, 0.0, 1, datetime('now')),
('Alessandro Bruno', 'OSS', 'BT_OSS_005', 1, 300.0, 250.0, 0.0, 1, datetime('now')),
('Valentina Greco', 'Infermiere', 'BT_INF_005', 1, 280.0, 300.0, 0.0, 1, datetime('now')),
('Matteo Lombardi', 'OSS', 'BT_OSS_006', 1, 350.0, 200.0, 0.0, 1, datetime('now')),
('Chiara Romano', 'Infermiere', 'BT_INF_006', 1, 320.0, 280.0, 0.0, 1, datetime('now')),
('Davide Rizzo', 'OSS', 'BT_OSS_007', 1, 400.0, 350.0, 0.0, 1, datetime('now')),
('Silvia Marino', 'Infermiere', 'BT_INF_007', 1, 380.0, 400.0, 0.0, 1, datetime('now')),
('Simone Galli', 'OSS', 'BT_OSS_008', 1, 450.0, 300.0, 0.0, 1, datetime('now')),
('Monica Fontana', 'Infermiere', 'BT_INF_008', 1, 420.0, 380.0, 0.0, 1, datetime('now')),
('Federico Villa', 'OSS', 'BT_OSS_009', 1, 160.0, 250.0, 0.0, 1, datetime('now')),
('Paola Caruso', 'Infermiere', 'BT_INF_009', 1, 240.0, 220.0, 0.0, 1, datetime('now')),
('Nicola Esposito', 'OSS', 'BT_OSS_010', 1, 190.0, 320.0, 0.0, 1, datetime('now')),
('Antonella De Luca', 'Infermiere', 'BT_INF_010', 1, 270.0, 350.0, 0.0, 1, datetime('now')),
('Stefano Moretti', 'OSS', 'BT_OSS_011', 1, 130.0, 180.0, 0.0, 1, datetime('now')),
('Cristina Barbieri', 'Infermiere', 'BT_INF_011', 1, 340.0, 160.0, 0.0, 1, datetime('now')),
('Emanuele Santoro', 'OSS', 'BT_OSS_012', 1, 210.0, 290.0, 0.0, 1, datetime('now')),
('Roberta Pellegrini', 'Infermiere', 'BT_INF_012', 1, 360.0, 320.0, 0.0, 1, datetime('now')),
('Giovanni Testa', 'Infermiere', 'BT_INF_013', 1, 110.0, 140.0, 0.0, 1, datetime('now')),
('Laura Benedetti', 'Infermiere', 'BT_INF_014', 1, 290.0, 190.0, 0.0, 1, datetime('now')),
('Antonio Ferri', 'Infermiere', 'BT_INF_015', 1, 170.0, 360.0, 0.0, 1, datetime('now')),
('Martina Russo', 'Infermiere', 'BT_INF_016', 1, 390.0, 260.0, 0.0, 1, datetime('now')),
('Paolo Ricci', 'Infermiere', 'BT_INF_017', 1, 220.0, 180.0, 0.0, 1, datetime('now'));

SELECT COUNT(*) as 'Personale Totale' FROM personale_manutenzione;
SELECT COUNT(*) as 'OSS' FROM personale_manutenzione WHERE ruolo = 'OSS';
SELECT COUNT(*) as 'Infermieri' FROM personale_manutenzione WHERE ruolo = 'Infermiere';