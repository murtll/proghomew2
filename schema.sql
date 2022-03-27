DROP TABLE IF EXISTS types;
DROP TABLE IF EXISTS transport;

CREATE TABLE types (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	capacity REAL NOT NULL,
	min_length REAL NOT NULL,
	min_width REAL NOT NULL,
	min_height REAL NOT NULL,
	max_length REAL NOT NULL,
	max_width REAL NOT NULL,
	max_height REAL NOT NULL
);

INSERT INTO types (
	name,
	capacity,
	min_length,
	max_length,
	min_width,
	max_width,
	min_height,
	max_height
) VALUES ('Газель', 2, 3, 3, 2, 2, 1.7, 2.2),
		 ('Бычок', 3, 4.2, 5, 2, 2.2, 2, 2.4),
		 ('MAN-10', 10, 6, 8, 2.45, 2.45, 2.3, 2.7),
		 ('Фура', 20, 13.6, 13.6, 2.46, 2.46, 2.5, 2.7);

CREATE TABLE transport (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		type_id INTEGER NOT NULL REFERENCES types(id),
		length REAL NOT NULL,
		width REAL NOT NULL,
		height REAL NOT NULL,
		is_busy INTEGER NOT NULL DEFAULT 0
);

INSERT INTO transport (
		type_id,
		name,
		length,
		width,
		height,
		is_busy
		) VALUES 
		(1, 'Абобус', 3, 2, 1.7, 0),
		(2, 'Водохлёбус', 4.5, 2, 2, 1);
