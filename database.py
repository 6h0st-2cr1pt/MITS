import sqlite3
import bcrypt
import os

def setup_database(db_path):
    """Setup the SQLite database with necessary tables if they don't exist"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create Missing Items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS missing_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reporter TEXT NOT NULL,
        student_id TEXT NOT NULL,
        item_name TEXT NOT NULL,
        description TEXT,
        color TEXT,
        location TEXT,
        date_reported TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Missing'
    )
    ''')
    
    # Create Recovered Items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recovered_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        found_by TEXT NOT NULL,
        item_name TEXT NOT NULL,
        description TEXT,
        color TEXT,
        location_found TEXT,
        date_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        image_path TEXT,
        status TEXT DEFAULT 'Available'
    )
    ''')
    
    # Create Rewards table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rewards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        student_name TEXT NOT NULL,
        reward_points INTEGER DEFAULT 0,
        item_returned INTEGER,
        verified_by TEXT,
        date_awarded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Pending'
    )
    ''')
    
    # Create Claim Requests table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS claim_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        student_name TEXT NOT NULL,
        item_id INTEGER NOT NULL,
        requested_by TEXT NOT NULL,
        date_requested TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Pending',
        verified_by TEXT,
        date_verified TIMESTAMP
    )
    ''')
    
    # Create a default admin user if it doesn't exist
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        # Hash the password for security
        hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                      ('admin', hashed_password.decode('utf-8'), 'admin'))
    
    conn.commit()
    conn.close()

def verify_login(db_path, username, password):
    """Verify user login credentials"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    if result:
        stored_password, role = result
        # Check if the provided password matches the stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            conn.close()
            return True, role
    
    conn.close()
    return False, None

def add_user(db_path, username, password, role):
    """Add a new user to the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Hash the password for security
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                      (username, hashed_password.decode('utf-8'), role))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Username already exists
        conn.close()
        return False

def get_missing_items(db_path, search_query=None):
    """Get all missing items or filter by search query"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cursor = conn.cursor()
    
    if search_query:
        search = f"%{search_query}%"
        cursor.execute("""
        SELECT * FROM missing_items 
        WHERE item_name LIKE ? OR description LIKE ? OR color LIKE ?
        ORDER BY date_reported DESC
        """, (search, search, search))
    else:
        cursor.execute("SELECT * FROM missing_items ORDER BY date_reported DESC")
    
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items

def get_recovered_items(db_path, search_query=None):
    """Get all recovered items or filter by search query"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if search_query:
        search = f"%{search_query}%"
        cursor.execute("""
        SELECT * FROM recovered_items 
        WHERE item_name LIKE ? OR description LIKE ? OR color LIKE ?
        ORDER BY date_found DESC
        """, (search, search, search))
    else:
        cursor.execute("SELECT * FROM recovered_items ORDER BY date_found DESC")
    
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items

def add_missing_item(db_path, reporter, student_id, item_name, description, color, location):
    """Add a new missing item to the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO missing_items (reporter, student_id, item_name, description, color, location)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (reporter, student_id, item_name, description, color, location))
    
    conn.commit()
    conn.close()
    return True

def add_recovered_item(db_path, found_by, item_name, description, color, location_found, image_path):
    """Add a new recovered item to the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO recovered_items (found_by, item_name, description, color, location_found, image_path)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (found_by, item_name, description, color, location_found, image_path))
    
    conn.commit()
    conn.close()
    return True

def submit_claim_request(db_path, student_id, student_name, item_id, requested_by):
    """Submit a claim request for a recovered item"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO claim_requests (student_id, student_name, item_id, requested_by)
    VALUES (?, ?, ?, ?)
    """, (student_id, student_name, item_id, requested_by))
    
    conn.commit()
    conn.close()
    return True

def get_claim_requests(db_path, status=None):
    """Get claim requests with optional status filter"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if status:
        cursor.execute("""
        SELECT cr.*, ri.item_name 
        FROM claim_requests cr
        JOIN recovered_items ri ON cr.item_id = ri.id
        WHERE cr.status = ?
        ORDER BY date_requested DESC
        """, (status,))
    else:
        cursor.execute("""
        SELECT cr.*, ri.item_name 
        FROM claim_requests cr
        JOIN recovered_items ri ON cr.item_id = ri.id
        ORDER BY date_requested DESC
        """)
    
    requests = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return requests

def approve_claim(db_path, claim_id, verified_by):
    """Approve a claim request and update the recovered item status"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get the item_id from the claim request
    cursor.execute("SELECT item_id FROM claim_requests WHERE id = ?", (claim_id,))
    item_id = cursor.fetchone()[0]
    
    # Update the claim request status
    cursor.execute("""
    UPDATE claim_requests 
    SET status = 'Approved', verified_by = ?, date_verified = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (verified_by, claim_id))
    
    # Update the recovered item status
    cursor.execute("""
    UPDATE recovered_items 
    SET status = 'Claimed'
    WHERE id = ?
    """, (item_id,))
    
    conn.commit()
    conn.close()
    return True

def add_reward(db_path, student_id, student_name, reward_points, item_returned):
    """Add a reward for an honest student"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO rewards (student_id, student_name, reward_points, item_returned)
    VALUES (?, ?, ?, ?)
    """, (student_id, student_name, reward_points, item_returned))
    
    conn.commit()
    conn.close()
    return True

def verify_reward(db_path, reward_id, verified_by):
    """Verify a reward"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    UPDATE rewards 
    SET status = 'Verified', verified_by = ?
    WHERE id = ?
    """, (verified_by, reward_id))
    
    conn.commit()
    conn.close()
    return True

def get_rewards(db_path, status=None):
    """Get rewards with optional status filter"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if status:
        cursor.execute("""
        SELECT r.*, ri.item_name 
        FROM rewards r
        LEFT JOIN recovered_items ri ON r.item_returned = ri.id
        WHERE r.status = ?
        ORDER BY date_awarded DESC
        """, (status,))
    else:
        cursor.execute("""
        SELECT r.*, ri.item_name 
        FROM rewards r
        LEFT JOIN recovered_items ri ON r.item_returned = ri.id
        ORDER BY date_awarded DESC
        """)
    
    rewards = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rewards

def get_user_list(db_path):
    """Get a list of all users"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, role, created_at FROM users")
    
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users
