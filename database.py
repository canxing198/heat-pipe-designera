import sqlite3
import pandas as pd

DB = "hp_rnd.db"

def init_db():
    c = sqlite3.connect(DB).cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS hp_test (
        id INTEGER PRIMARY KEY,
        powder TEXT,
        d REAL, eps REAL,
        D_out REAL, b_flat REAL,
        L_eff REAL,
        Q_cap REAL, Q_boil REAL, Q_visc REAL,
        Q_allow REAL, result TEXT
    )
    """)
    c.connection.commit()

def save(rec):
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO hp_test VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)", rec)
    conn.commit()

def load_df():
    return pd.read_sql("SELECT * FROM hp_test", sqlite3.connect(DB))
