import sqlite3

class SimpleSQLiteDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        create_users_table_query = '''
            CREATE TABLE IF NOT EXISTS users (
                id BIGINT PRIMARY KEY NOT NULL,
                name VARCHAR(100) NOT NULL,
                realname VARCHAR(100) NOT NULL,
                balance DOUBLE UNSIGNED
            )
        '''
        create_items_table_query = '''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                quantity INT UNSIGNED,
                price DOUBLE UNSIGNED NOT NULL
            )
        '''
        with self.connection:
            self.connection.execute(create_users_table_query)
            self.connection.execute(create_items_table_query)

    # Users Table
    def insert_user(self, id_user, name,realname, balance):
        insert_query = '''
            INSERT INTO users (id, name,realname, balance) VALUES (?,?,?,?)
        '''
        with self.connection:
            self.connection.execute(insert_query, (id_user, name,realname, balance))

    def update_balance_by_id(self, ajout, id_user):
        new_balance  = max(0, round(self.get_balance_by_id(id_user) + ajout, 3))
        update_query = '''
            UPDATE users
            SET balance =  ?
            WHERE id = ?
        '''
        with self.connection:
            self.connection.execute(update_query, (new_balance, id_user))

    def get_user_by_id(self, id_user):
        select_query = '''
            SELECT id, name, realname, balance
            FROM users
            WHERE id = ?
        '''
        with self.connection:
            cursor = self.connection.execute(select_query, (id_user,))
            return cursor.fetchone() #renvoie tuple

    def get_user_name_by_id(self, id_user):
        select_query = '''
            SELECT name
            FROM users
            WHERE id = ?
        '''
        with self.connection:
            cursor = self.connection.execute(select_query, (id_user,))
            result = cursor.fetchone()
            if result:
                return str(result[0])
            else:
                return None  # Ou tout autre indication de l'absence de résultat

    def get_user_realname_by_id(self, id_user):
        select_query = '''
            SELECT realname
            FROM users
            WHERE id = ?
        '''
        with self.connection:
            cursor = self.connection.execute(select_query, (id_user,))
            result = cursor.fetchone()
            if result:
                return str(result[0])  # Renvoie la balance comme float
            else:
                return None  # Ou tout autre indication de l'absence de résultat

    def get_all_users(self):
        select_all_query = '''
            SELECT id, name, realname, balance
            FROM users ORDER BY balance DESC
        '''
        with self.connection:
            cursor = self.connection.execute(select_all_query)
            return cursor.fetchall() #liste de tuples

    def get_balance_by_id(self,id_user):
        select_query = '''
            SELECT balance
            FROM users
            WHERE id = ?
        '''
        with self.connection:
            cursor = self.connection.execute(select_query, (id_user,))
            result = cursor.fetchone()
            if result:
                return float(result[0])  # Renvoie la balance comme float
            else:
                return None  # Ou tout autre indication de l'absence de résultat

    # Items Table
    def insert_item(self, name_item, quantity_item, price_item):
        insert_query = '''
            INSERT INTO items (name,quantity,price) VALUES (?,?,?)
        '''
        with self.connection:
            self.connection.execute(insert_query, (name_item, quantity_item, price_item))

    def update_quantity_by_name(self, new_quantity,name_item):
        update_query = '''
            UPDATE items
            SET quantity = ?
            WHERE name = ?
        '''
        with self.connection:
            self.connection.execute(update_query, (new_quantity,name_item))

    def update_price_by_name(self, new_price, name_item):
        update_query = '''
            UPDATE items
            SET price = ?
            WHERE name = ?
        '''
        with self.connection:
            self.connection.execute(update_query, (new_price, name_item))

    def update_realname_by_id(self,realname,id_user):
        update_query = '''
            UPDATE users
            SET realname = ?
            WHERE id = ?
        '''
        with self.connection:
            self.connection.execute(update_query, (realname, id_user))

    def update_name_by_id(self,name,id_user):
        update_query = '''
            UPDATE users
            SET name = ?
            WHERE id = ?
        '''
        with self.connection:
            self.connection.execute(update_query, (name, id_user))

    def get_item_by_name(self, name_item):
        select_query = '''
            SELECT name, quantity, price
            FROM items
            WHERE name = ?
        '''
        with self.connection:
            cursor = self.connection.execute(select_query, (name_item,))
            return cursor.fetchone() #tuple

    def get_item_price(self,name_item):
        select_query = '''
            SELECT price
            FROM items
            WHERE name = ?
        '''
        with self.connection:
            cursor = self.connection.execute(select_query, (name_item,))
            result = cursor.fetchone()
            if result:
                return float(result[0])
            else:
                return None  # Ou tout autre indication de l'absence de résultat

    def get_item_quantity(self,name_item):
        select_query = '''
            SELECT quantity
            FROM items
            WHERE name = ?
        '''
        with self.connection:
            cursor = self.connection.execute(select_query, (name_item,))
            result = cursor.fetchone()
            if result:
                return int(result[0])
            else:
                return None  # Ou tout autre indication de l'absence de résultat

    def get_all_items(self):
        select_all_query = '''
            SELECT name, quantity, price
            FROM items ORDER BY name
        '''
        with self.connection:
            cursor = self.connection.execute(select_all_query)
            return cursor.fetchall() #retourne liste de tuples

    def user_exist_by_id(self,id):
        select_query="SELECT EXISTS (SELECT 1 FROM users WHERE id=?)"
        with self.connection:
            cursor = self.connection.execute(select_query, (id,))
            result = cursor.fetchone()
            return result[0] == 1 # 1 if exists, 0 if not exists

    def item_exist_by_name(self,name):
        select_query="SELECT EXISTS (SELECT 1 FROM items WHERE name=?)"
        with self.connection:
            cursor = self.connection.execute(select_query, (name,))
            result = cursor.fetchone()
            return result[0] == 1 # 1 if exists, 0 if not exists

    def delete_user_by_id(self,id_user):
        delete_query = '''
        DELETE FROM users WHERE id=?
        '''
        with self.connection:
            cursor = self.connection.execute(delete_query, (id_user,))
            #return cursor.rowcount #nb de lignes affectées par la suppression

    def delete_item_by_name(self,item_name):
        delete_query = '''
        DELETE FROM items WHERE name=?
        '''
        with self.connection:
            cursor = self.connection.execute(delete_query, (item_name,))
            #return cursor.rowcount #nb de lignes affectées par la suppression

    def close_connection(self):
        self.connection.close()
"""
# Example usage
database = SimpleSQLiteDatabase('my_database.db')

# Insert a new user
database.insert_user('John Doe', 1000)

# Insert a new item
database.insert_item('Apple', 5, 100)

# Update user balance by name
database.update_balance_by_name('John Doe', 1200)

# Get user by name
user = database.get_user_by_name('John Doe')
print(user)

# Get item by name
item = database.get_item_by_name('Apple')
print(item)

# Get all users
all_users = database.get_all_users()
print(all_users)

# Get all items
all_items = database.get_all_items()
print(all_items)

# Don't forget to close the connection when you're done
database.close_connection()
"""
