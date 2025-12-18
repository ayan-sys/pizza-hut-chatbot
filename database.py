import sqlite3
import json
from datetime import datetime

DB_NAME = "pizza_hut.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # 1. Menu Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price INTEGER NOT NULL,
            image_path TEXT,
            tags TEXT
        )
    ''')
    
    # 2. Orders Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            address TEXT,
            items TEXT NOT NULL, -- JSON string
            total_amount INTEGER NOT NULL,
            status TEXT DEFAULT 'Pending',
            payment_method TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    seed_menu()

def seed_menu():
    conn = get_connection()
    c = conn.cursor()
    
    # Check if empty
    c.execute('SELECT count(*) FROM menu')
    if c.fetchone()[0] == 0:
        menu_items = [
            ('Large Pizza', 'Pizza', 1500, 'large_pizza.png', 'large, pizza, cheesy'),
            ('Medium Pizza', 'Pizza', 1000, 'medium_pizza.png', 'medium, pizza'),
            ('Small Pizza', 'Pizza', 500, 'small_pizza.png', 'small, pizza'),
            ('Zinger Burger', 'Burger', 600, 'zinger_burger.png', 'zinger, burger, crispy'),
            ('Chicken Burger', 'Burger', 250, 'normal_chicken_burger.png', 'chicken, burger, classic'),
            ('Special Burger', 'Burger', 380, 'special_chicken_burger.png', 'special, burger'),
            ('Cola Next', 'Drink', 80, 'cola_drink.png', 'cola, drink, soda'),
            ('FizzUp', 'Drink', 80, 'cola_drink.png', 'fizzup, drink')
        ]
        c.executemany('INSERT INTO menu (name, category, price, image_path, tags) VALUES (?,?,?,?,?)', menu_items)
        conn.commit()
        print("Menu seeded.")
        
    conn.close()

# --- Helpers ---
def get_menu():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM menu')
    items = c.fetchall()
    conn.close()
    
    # Convert to list of dicts
    menu = []
    for item in items:
        menu.append({
            'id': item[0],
            'name': item[1],
            'category': item[2],
            'price': item[3],
            'image': item[4],
            'tags': item[5].split(', ')
        })
    return menu

def create_order(name, address, items, total, payment):
    conn = get_connection()
    c = conn.cursor()
    items_json = json.dumps(items)
    c.execute('INSERT INTO orders (customer_name, address, items, total_amount, payment_method) VALUES (?, ?, ?, ?, ?)',
              (name, address, items_json, total, payment))
    order_id = c.lastrowid
    conn.commit()
    conn.close()
    return order_id

def get_orders():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM orders ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def update_order_status(order_id, status):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    conn.commit()
    conn.close()

def get_order_by_id(order_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    row = c.fetchone()
    conn.close()
    return row

def get_orders_by_name(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM orders WHERE customer_name LIKE ? ORDER BY timestamp DESC', (f'%{name}%',))
    rows = c.fetchall()
    conn.close()
    return rows
