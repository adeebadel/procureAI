import sqlite3
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "procureai.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY,
            tender_name TEXT NOT NULL,
            bidder_name TEXT,
            tender_pages TEXT NOT NULL,
            requirements TEXT NOT NULL,
            bidder_pages TEXT,
            compliance_report TEXT
        )
    """)

    connection.commit()
    connection.close()


def create_analysis(analysis_id, tender_name, tender_pages, requirements):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO analyses (
            id,
            tender_name,
            tender_pages,
            requirements
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            analysis_id,
            tender_name,
            json.dumps(tender_pages),
            json.dumps(requirements)
        )
    )

    connection.commit()
    connection.close()


def get_analysis(analysis_id):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM analyses
        WHERE id = ?
        """,
        (analysis_id,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "id": row["id"],
        "tender_name": row["tender_name"],
        "bidder_name": row["bidder_name"],
        "tender_pages": json.loads(row["tender_pages"]),
        "requirements": json.loads(row["requirements"]),
        "bidder_pages": (
            json.loads(row["bidder_pages"])
            if row["bidder_pages"]
            else []
        ),
        "compliance_report": (
            json.loads(row["compliance_report"])
            if row["compliance_report"]
            else None
        )
    }


def update_bidder_data(
    analysis_id,
    bidder_name,
    bidder_pages,
    compliance_report
):
    connection = get_connection()

    connection.execute(
        """
        UPDATE analyses
        SET
            bidder_name = ?,
            bidder_pages = ?,
            compliance_report = ?
        WHERE id = ?
        """,
        (
            bidder_name,
            json.dumps(bidder_pages),
            json.dumps(compliance_report)
            if compliance_report is not None
            else None,
            analysis_id
        )
    )

    connection.commit()
    connection.close()


def delete_analysis(analysis_id):
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM analyses
        WHERE id = ?
        """,
        (analysis_id,)
    )

    connection.commit()
    connection.close()