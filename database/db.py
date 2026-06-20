import sqlite3

DB_PATH = "database/compliance.db"


def init_db():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS violations(

        event_id TEXT PRIMARY KEY,

        timestamp TEXT,

        clip_id TEXT,

        zone TEXT,

        behavior_class TEXT,

        policy_rule_ref TEXT,

        event_description TEXT,

        severity TEXT,

        escalation_action TEXT

    )
    """)

    conn.commit()
    conn.close()


def insert_violation(report):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

    INSERT OR REPLACE INTO violations
    VALUES (?,?,?,?,?,?,?,?,?)

    """,(

        report["event_id"],
        report["timestamp"],
        report["clip_id"],
        report["zone"],
        report["behavior_class"],
        report["policy_rule_ref"],
        report["event_description"],
        report["severity"],
        report["escalation_action"]

    ))

    conn.commit()
    conn.close()