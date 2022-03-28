import sqlite3

class Type:
    def __init__(self, id, name, capacity, minLength, maxLength, minWidth, maxWidth, minHeight, maxHeight):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.minLength = minLength
        self.maxLength = maxLength
        self.minWidth = minWidth
        self.maxWidth = maxWidth
        self.minHeight = minHeight
        self.maxHeight = maxHeight

    def from_dict(t):
        return Type(
                t['types_id'],
                t['types_name'],
                t['types_capacity'],
                t['types_min_length'],
                t['types_max_length'],
                t['types_min_width'],
                t['types_max_width'],
                t['types_min_height'],
                t['types_max_height']
            )

class Transport:
    def __init__(self, id, name, _type, length, width, height, isBusy = False):
        self.id = id
        self.name = name
        self.type = _type
        self.length = length
        self.width = width
        self.height = height
        self.isBusy = isBusy

    def from_dict(t):
        return Transport(
            t['transport_id'], 
            t['transport_name'], 
            Type.from_dict(t),
            t['transport_length'], 
            t['transport_width'], 
            t['transport_height'], 
            bool(t['transport_is_busy'])
        )


class DbWorker:
    def __init__(self):
        connection = sqlite3.connect('database.db')
        with open('schema.sql') as schema:
            connection.executescript(schema.read())
        connection.commit()
        connection.close()

    def get_all_transport(self):
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row

        transport = connection.execute('''SELECT 
                                            transport.id as transport_id, 
                                            transport.name as transport_name,
                                            transport.length as transport_length, 
                                            transport.width as transport_width, 
                                            transport.height as transport_height, 
                                            transport.is_busy as transport_is_busy,
                                            types.id as types_id,
                                            types.name as types_name,
                                            types.capacity as types_capacity,
                                            types.min_length as types_min_length,
                                            types.max_length as types_max_length,
                                            types.min_width as types_min_width,
                                            types.max_width as types_max_width,
                                            types.min_height as types_min_height,
                                            types.max_height as types_max_height
                                        FROM transport 
                                            INNER JOIN types 
                                            ON transport.type_id = types.id''').fetchall()
        connection.close()

        return list(map(Transport.from_dict, transport))

    def get_all_transport_by_capacity(self, min_capacity):
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row

        transport = connection.execute('''SELECT 
                                            transport.id as transport_id, 
                                            transport.name as transport_name,
                                            transport.length as transport_length, 
                                            transport.width as transport_width, 
                                            transport.height as transport_height, 
                                            transport.is_busy as transport_is_busy,
                                            types.id as types_id,
                                            types.name as types_name,
                                            types.capacity as types_capacity,
                                            types.min_length as types_min_length,
                                            types.max_length as types_max_length,
                                            types.min_width as types_min_width,
                                            types.max_width as types_max_width,
                                            types.min_height as types_min_height,
                                            types.max_height as types_max_height
                                        FROM transport 
                                            INNER JOIN types 
                                            ON transport.type_id = types.id WHERE types.capacity>=?''', (min_capacity)).fetchall()
        connection.close()

        return list(map(Transport.from_dict, transport))

    def get_all_transport_by_busy_and_capacity(self, busy, min_capacity):
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row

        transport = connection.execute('''SELECT 
                                            transport.id as transport_id, 
                                            transport.name as transport_name,
                                            transport.length as transport_length, 
                                            transport.width as transport_width, 
                                            transport.height as transport_height, 
                                            transport.is_busy as transport_is_busy,
                                            types.id as types_id,
                                            types.name as types_name,
                                            types.capacity as types_capacity,
                                            types.min_length as types_min_length,
                                            types.max_length as types_max_length,
                                            types.min_width as types_min_width,
                                            types.max_width as types_max_width,
                                            types.min_height as types_min_height,
                                            types.max_height as types_max_height
                                        FROM transport 
                                            INNER JOIN types 
                                            ON transport.type_id = types.id WHERE transport.is_busy=? and types.capacity>=?''', (busy, min_capacity)).fetchall()
        connection.close()

        return list(map(Transport.from_dict, transport))

    def add_car(self, type_id, name, length, width, height):
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row

        connection.execute('''INSERT INTO transport 
                                (type_id, name, length, width, height)
                                VALUES (?, ?, ?, ?, ?)''', (type_id, name, length, width, height))
        connection.commit()
        connection.close()

    def get_all_types(self):
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row

        types = connection.execute('''SELECT 
                                        types.id as types_id,
                                        types.name as types_name,
                                        types.capacity as types_capacity,
                                        types.min_length as types_min_length,
                                        types.max_length as types_max_length,
                                        types.min_width as types_min_width,
                                        types.max_width as types_max_width,
                                        types.min_height as types_min_height,
                                        types.max_height as types_max_height 
                                    FROM types''').fetchall()
        connection.close()

        return list(map(Type.from_dict, types))

    def get_type_by_id(self, id):
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row

        _type = connection.execute('''SELECT 
                                        types.id as types_id,
                                        types.name as types_name,
                                        types.capacity as types_capacity,
                                        types.min_length as types_min_length,
                                        types.max_length as types_max_length,
                                        types.min_width as types_min_width,
                                        types.max_width as types_max_width,
                                        types.min_height as types_min_height,
                                        types.max_height as types_max_height 
                                    FROM types WHERE id = ?''', (id)).fetchone()
        connection.close()

        return Type.from_dict(_type)
    
    def delete_car_by_id(self, id):
        connection = sqlite3.connect('database.db')
        connection.execute('''DELETE FROM transport WHERE id=? AND is_busy=0''', (id))
        connection.commit()
        connection.close()

    def reserve_car_by_id(self, id):
        connection = sqlite3.connect('database.db')
        connection.execute('''UPDATE transport SET is_busy=1 WHERE id=? AND is_busy=0''', (id))
        connection.commit()
        connection.close()

    def unreserve_car_by_id(self, id):
        connection = sqlite3.connect('database.db')
        connection.execute('''UPDATE transport SET is_busy=0 WHERE id=? AND is_busy=1''', (id))
        connection.commit()
        connection.close()

    def get_matching_car_id(self, length, width, height, weight):
        connection = sqlite3.connect('database.db')
        connection.row_factory = sqlite3.Row

        _max = max(length, width, height) 
        _min = min(length, width, height)
        
        rec_id = connection.execute('''SELECT 
                                            transport.id 
                                            FROM transport 
                                            INNER JOIN types
                                            ON transport.type_id = types.id
                                            WHERE 
                                            capacity>=?
                                            AND
                                            max(length, width, height)>=?
                                            AND
                                            min(length, width, height)>=?
                                            AND
                                            (length + width + height - min(length, width, height) - max(length, width, height))>=?
                                            ORDER BY is_busy
                                            LIMIT 1
                                            ''', (weight, _max, _min, length + width + height - _max - _min)).fetchone()
        connection.close()
        return rec_id['id'] if rec_id else None
