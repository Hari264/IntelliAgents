import sqlite3
from datetime import datetime, timezone
from app.config import ROOT

DB = ROOT / "logs" / "refusals.db"

def _conn():
    DB.parent.mkdir(exist_ok=True)
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS refusals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT, question TEXT, persona TEXT, date_of_loss TEXT,
        key_terms TEXT, status TEXT,            -- open | drafted | approved | rejected
        draft TEXT, drafted_at TEXT,
        reviewer TEXT, reviewed_at TEXT, doc_id TEXT)""")
    return c

def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def log_refusal(question, persona, date_of_loss=None, key_terms=None):
    """Save a refusal as an open item. The same open question from the same role is not saved twice."""
    with _conn() as c:
        row = c.execute("SELECT id FROM refusals WHERE question=? AND persona=? AND status IN ('open','drafted')",
                        (question, persona)).fetchone()
        if row:
            return row["id"]
        cur = c.execute("INSERT INTO refusals(created_at, question, persona, date_of_loss, key_terms, status) "
                        "VALUES (?,?,?,?,?, 'open')",
                        (_now(), question, persona, date_of_loss or "", ", ".join(key_terms or [])))
        return cur.lastrowid

def list_refusals(status=None):
    with _conn() as c:
        if status:
            rows = c.execute("SELECT * FROM refusals WHERE status=? ORDER BY id", (status,)).fetchall()
        else:
            rows = c.execute("SELECT * FROM refusals ORDER BY id").fetchall()
        return [dict(r) for r in rows]

def get_refusal(rid):
    with _conn() as c:
        row = c.execute("SELECT * FROM refusals WHERE id=?", (rid,)).fetchone()
        return dict(row) if row else None

def save_draft(rid, doc_id, draft):
    with _conn() as c:
        c.execute("UPDATE refusals SET status='drafted', draft=?, doc_id=?, drafted_at=? WHERE id=?",
                  (draft, doc_id, _now(), rid))

def approve(rid, reviewer, note=""):
    """SME approves a drafted item. This does NOT index it; indexing is the next step."""
    if not reviewer.strip():
        raise ValueError("A reviewer name is required.")
    item = get_refusal(rid)
    if not item or item["status"] != "drafted":
        raise ValueError(f"refusal {rid} must be 'drafted' to approve (it is {item['status'] if item else 'missing'}).")
    with _conn() as c:
        c.execute("UPDATE refusals SET status='approved', reviewer=?, reviewed_at=? WHERE id=?",
                  (reviewer.strip(), _now(), rid))

def reject(rid, reviewer, note=""):
    """SME rejects a drafted item. It never reaches the index."""
    if not reviewer.strip():
        raise ValueError("A reviewer name is required.")
    item = get_refusal(rid)
    if not item or item["status"] != "drafted":
        raise ValueError(f"refusal {rid} must be 'drafted' to reject.")
    with _conn() as c:
        c.execute("UPDATE refusals SET status='rejected', reviewer=?, reviewed_at=? WHERE id=?",
                  (reviewer.strip(), _now(), rid))

def mark_indexed(rid):
    with _conn() as c:
        c.execute("UPDATE refusals SET status='indexed' WHERE id=?", (rid,))

def reset_item(rid):
    """Put an item back to 'open' and clear its draft and review. Used to repeat the demo."""
    with _conn() as c:
        c.execute("UPDATE refusals SET status='open', draft=NULL, drafted_at=NULL, reviewer=NULL, "
                  "reviewed_at=NULL, doc_id=NULL WHERE id=?", (rid,))

def dismiss(rid, reviewer, note=""):
    """SME closes an open or drafted item without publishing anything."""
    if not reviewer.strip():
        raise ValueError("A reviewer name is required.")
    with _conn() as c:
        c.execute("UPDATE refusals SET status='rejected', reviewer=?, reviewed_at=? "
                  "WHERE id=? AND status IN ('open','drafted')", (reviewer.strip(), _now(), rid))