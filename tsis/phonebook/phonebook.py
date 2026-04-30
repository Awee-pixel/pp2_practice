import json
import csv
import os
import sys
from datetime import date, datetime

import psycopg2
import psycopg2.extras

from config import DB_CONFIG, PAGE_SIZE
from connect import get_conn, get_cursor

BOLD  = "\033[1m"
CYAN  = "\033[96m"
GREEN = "\033[92m"
RED   = "\033[91m"
YELLOW= "\033[93m"
DIM   = "\033[2m"
RESET = "\033[0m"

def h1(text):  print(f"\n{BOLD}{CYAN}{'─'*60}{RESET}\n{BOLD}{CYAN}  {text}{RESET}\n{BOLD}{CYAN}{'─'*60}{RESET}")
def h2(text):  print(f"\n{BOLD}{YELLOW}  {text}{RESET}")
def ok(text):  print(f"{GREEN}  ✔  {text}{RESET}")
def err(text): print(f"{RED}  ✘  {text}{RESET}")
def info(text):print(f"{DIM}  {text}{RESET}")

def prompt(label, default=""):
    val = input(f"  {label}{f' [{default}]' if default else ''}: ").strip()
    return val or default

def confirm(question) -> bool:
    ans = input(f"  {question} [y/N]: ").strip().lower()
    return ans == "y"

def pick(label, options: list[str]) -> str:
    """Display numbered list, return chosen string."""
    print(f"\n  {label}")
    for i, o in enumerate(options, 1):
        print(f"    {i}. {o}")
    while True:
        raw = input("  Choice: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        err("Invalid choice.")

def fmt_date(d) -> str:
    if d is None:
        return "—"
    if isinstance(d, str):
        return d
    return d.strftime("%Y-%m-%d")

def fmt_row(row: dict) -> str:
    phones = row.get("phones", "")
    parts = [
        f"{BOLD}{row['first_name']} {row.get('last_name') or ''}{RESET}",
        f"📞 {phones or '—'}",
        f"✉  {row.get('email') or '—'}",
        f"🎂 {fmt_date(row.get('birthday'))}",
        f"👥 {row.get('group_name') or '—'}",
    ]
    return "  " + "   ".join(parts)

def get_or_create_group(cur, group_name: str) -> int | None:
    if not group_name:
        return None
    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,))
    cur.execute("SELECT id FROM groups WHERE LOWER(name) = LOWER(%s)", (group_name,))
    row = cur.fetchone()
    return row["id"] if row else None


def fetch_phones_for(cur, contact_id: int) -> list[dict]:
    cur.execute(
        "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id",
        (contact_id,))
    return cur.fetchall()


def phones_str(phone_rows) -> str:
    if not phone_rows:
        return ""
    return ", ".join(f"{r['phone']} ({r['type']})" for r in phone_rows)


def contact_exists(cur, first_name: str) -> dict | None:
    cur.execute(
        "SELECT * FROM contacts WHERE LOWER(first_name) = LOWER(%s) LIMIT 1",
        (first_name,))
    return cur.fetchone()


def enrich_rows(cur, rows) -> list[dict]:
    """Add 'phones' string field to each contact row."""
    result = []
    for row in rows:
        d = dict(row)
        ph = fetch_phones_for(cur, d["id"])
        d["phones"] = phones_str(ph)
        d["_phones"] = ph   # raw list kept for JSON export
        result.append(d)
    return result


def list_groups(cur) -> list[str]:
    cur.execute("SELECT name FROM groups ORDER BY name")
    return [r["name"] for r in cur.fetchall()]


def add_contact():
    h1("Add Contact")
    conn = get_conn()
    cur  = get_cursor(conn)
    try:
        first = prompt("First name")
        if not first:
            err("First name is required."); return
        last   = prompt("Last name")
        email  = prompt("Email")
        bday   = prompt("Birthday (YYYY-MM-DD)")
        groups = list_groups(cur)
        grp    = pick("Group", groups + ["(none)"])
        grp    = None if grp == "(none)" else grp

        gid = get_or_create_group(cur, grp)
        cur.execute(
            """
            INSERT INTO contacts (first_name, last_name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
            """,
            (first, last or None, email or None,
             bday or None, gid))
        cid = cur.fetchone()["id"]

        # Add phones
        while True:
            ph = prompt("Phone number (blank to stop)")
            if not ph:
                break
            ptype = pick("Phone type", ["mobile", "home", "work"])
            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                (cid, ph, ptype))
            ok(f"Added {ph} ({ptype})")

        conn.commit()
        ok(f"Contact '{first} {last}' created (id={cid}).")
    except Exception as e:
        conn.rollback(); err(str(e))
    finally:
        cur.close(); conn.close()


def search_menu():
    h1("Search & Filter")
    mode = pick("Search mode", [
        "Full-text search (name / email / phone)",
        "Filter by group",
        "Search by email",
        "Browse all (paginated)",
    ])
    conn = get_conn()
    cur  = get_cursor(conn)
    try:
        if mode.startswith("Full-text"):
            q = prompt("Search query")
            cur.execute("SELECT * FROM search_contacts(%s)", (q,))
            rows = enrich_rows(cur, cur.fetchall())
            _print_contacts(rows)

        elif mode.startswith("Filter by group"):
            groups = list_groups(cur)
            grp    = pick("Group", groups)
            sort   = _ask_sort()
            cur.execute(
                f"""
                SELECT c.*, g.name AS group_name
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                WHERE LOWER(g.name) = LOWER(%s)
                ORDER BY {sort}
                """, (grp,))
            rows = enrich_rows(cur, cur.fetchall())
            _print_contacts(rows)

        elif mode.startswith("Search by email"):
            q    = prompt("Email fragment")
            sort = _ask_sort()
            cur.execute(
                f"""
                SELECT c.*, g.name AS group_name
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                WHERE c.email ILIKE %s
                ORDER BY {sort}
                """, (f"%{q}%",))
            rows = enrich_rows(cur, cur.fetchall())
            _print_contacts(rows)

        else:
            _paginated_browse(cur)
    finally:
        cur.close(); conn.close()


def _ask_sort() -> str:
    choice = pick("Sort by", ["name", "birthday", "date added"])
    return {
        "name":       "c.first_name, c.last_name",
        "birthday":   "c.birthday NULLS LAST",
        "date added": "c.created_at",
    }[choice]


def _print_contacts(rows: list[dict]):
    if not rows:
        info("No contacts found."); return
    h2(f"{len(rows)} contact(s) found:")
    for r in rows:
        print(fmt_row(r))


def _paginated_browse(cur):
    h2("Paginated Browse")
    sort = _ask_sort()
    page = 0
    while True:
        offset = page * PAGE_SIZE
        cur.execute(
            f"""
            SELECT c.*, g.name AS group_name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY {sort}
            LIMIT %s OFFSET %s
            """, (PAGE_SIZE, offset))
        rows = enrich_rows(cur, cur.fetchall())
        if not rows and page > 0:
            info("No more contacts."); page -= 1; continue

        _print_contacts(rows)
        info(f"Page {page + 1}  |  Showing {offset+1}–{offset+len(rows)}")

        nav = prompt("  [n]ext  [p]rev  [q]uit", "q").lower()
        if nav == "n":
            if len(rows) == PAGE_SIZE:
                page += 1
            else:
                info("Last page.")
        elif nav == "p":
            if page > 0: page -= 1
            else: info("Already on first page.")
        else:
            break

def edit_contact():
    h1("Edit Contact")
    name = prompt("Contact first name to edit")
    conn = get_conn()
    cur  = get_cursor(conn)
    try:
        row = contact_exists(cur, name)
        if not row:
            err(f"Contact '{name}' not found."); return

        cid = row["id"]
        print(fmt_row({**dict(row),
                       "phones": phones_str(fetch_phones_for(cur, cid)),
                       "group_name": row.get("group_name")}))

        action = pick("What to edit", [
            "Name / email / birthday",
            "Move to group",
            "Add phone number",
            "Remove phone number",
            "Cancel",
        ])

        if action.startswith("Name"):
            first = prompt("New first name", row["first_name"])
            last  = prompt("New last name",  row["last_name"] or "")
            email = prompt("New email",       row["email"] or "")
            bday  = prompt("New birthday",    fmt_date(row["birthday"]))
            cur.execute(
                """UPDATE contacts SET first_name=%s, last_name=%s,
                   email=%s, birthday=%s WHERE id=%s""",
                (first, last or None, email or None, bday or None, cid))
            conn.commit(); ok("Contact updated.")

        elif action.startswith("Move"):
            cur2 = conn.cursor()
            cur2.execute("CALL move_to_group(%s, %s)",
                         (row["first_name"], prompt("Group name")))
            conn.commit(); ok("Group updated.")

        elif action == "Add phone number":
            ph    = prompt("Phone number")
            ptype = pick("Type", ["mobile", "home", "work"])
            cur.execute("CALL add_phone(%s, %s, %s)",
                        (row["first_name"], ph, ptype))
            conn.commit(); ok("Phone added.")

        elif action == "Remove phone number":
            phones = fetch_phones_for(cur, cid)
            if not phones:
                info("No phones on this contact."); return
            labels = [f"{r['phone']} ({r['type']})" for r in phones]
            chosen = pick("Phone to remove", labels)
            ph_val = chosen.split(" ")[0]
            cur.execute(
                "DELETE FROM phones WHERE contact_id=%s AND phone=%s",
                (cid, ph_val))
            conn.commit(); ok(f"Removed {ph_val}.")
    except Exception as e:
        conn.rollback(); err(str(e))
    finally:
        cur.close(); conn.close()


def delete_contact():
    h1("Delete Contact")
    name = prompt("First name to delete")
    conn = get_conn()
    cur  = get_cursor(conn)
    try:
        row = contact_exists(cur, name)
        if not row:
            err(f"'{name}' not found."); return
        if confirm(f"Delete '{row['first_name']} {row['last_name']}'?"):
            cur.execute("DELETE FROM contacts WHERE id = %s", (row["id"],))
            conn.commit(); ok("Deleted.")
    except Exception as e:
        conn.rollback(); err(str(e))
    finally:
        cur.close(); conn.close()

def export_json():
    h1("Export to JSON")
    path = prompt("Output file path", "contacts_export.json")
    conn = get_conn()
    cur  = get_cursor(conn)
    try:
        cur.execute(
            """
            SELECT c.*, g.name AS group_name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY c.first_name
            """)
        rows = enrich_rows(cur, cur.fetchall())

        # Convert dates for JSON serialisation
        for r in rows:
            r.pop("group_id", None)
            r.pop("id", None)
            if isinstance(r.get("birthday"), (date, datetime)):
                r["birthday"] = fmt_date(r["birthday"])
            if isinstance(r.get("created_at"), datetime):
                r["created_at"] = r["created_at"].isoformat()
            # Replace _phones (list of dicts) into clean list
            raw = r.pop("_phones", [])
            r["phones"] = [{"phone": p["phone"], "type": p["type"]} for p in raw]
            r.pop("phones", None)   # remove old string version
            r["phones"] = [{"phone": p["phone"], "type": p["type"]} for p in raw]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)

        ok(f"Exported {len(rows)} contact(s) to {path}.")
    finally:
        cur.close(); conn.close()


def import_json():
    h1("Import from JSON")
    path = prompt("JSON file path", "contacts_export.json")
    if not os.path.exists(path):
        err(f"File not found: {path}"); return

    with open(path, encoding="utf-8") as f:
        records = json.load(f)

    if not isinstance(records, list):
        err("Expected a JSON array at top level."); return

    conn = get_conn()
    cur  = get_cursor(conn)
    try:
        inserted = skipped = overwritten = 0
        for rec in records:
            first = rec.get("first_name", "").strip()
            if not first:
                info("Skipping record with no first_name."); continue

            existing = contact_exists(cur, first)
            if existing:
                action = pick(
                    f"'{first}' already exists. What to do?",
                    ["skip", "overwrite"])
                if action == "skip":
                    skipped += 1; continue
                # overwrite → delete old, re-insert
                cur.execute("DELETE FROM contacts WHERE id = %s", (existing["id"],))
                overwritten += 1
            else:
                inserted += 1

            gid = get_or_create_group(cur, rec.get("group_name"))
            cur.execute(
                """
                INSERT INTO contacts (first_name, last_name, email, birthday, group_id)
                VALUES (%s,%s,%s,%s,%s) RETURNING id
                """,
                (first,
                 rec.get("last_name") or None,
                 rec.get("email") or None,
                 rec.get("birthday") or None,
                 gid))
            cid = cur.fetchone()["id"]

            for ph in rec.get("phones", []):
                ptype = ph.get("type", "mobile")
                if ptype not in ("home", "work", "mobile"):
                    ptype = "mobile"
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                    (cid, ph["phone"], ptype))

        conn.commit()
        ok(f"Done — inserted: {inserted}, overwritten: {overwritten}, "
           f"skipped: {skipped}.")
    except Exception as e:
        conn.rollback(); err(str(e))
    finally:
        cur.close(); conn.close()



def import_csv():
    h1("Import from CSV")
    path = prompt("CSV file path", "contacts.csv")
    if not os.path.exists(path):
        err(f"File not found: {path}"); return

    conn = get_conn()
    cur  = get_cursor(conn)
    errors = []
    ok_count = 0

    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=2):
                first = row.get("first_name", "").strip()
                if not first:
                    errors.append(f"Row {i}: missing first_name"); continue
                try:
                    # upsert contact
                    existing = contact_exists(cur, first)
                    gid      = get_or_create_group(cur, row.get("group", ""))
                    bday     = row.get("birthday", "").strip() or None

                    if existing:
                        cid = existing["id"]
                        cur.execute(
                            """UPDATE contacts SET last_name=%s, email=%s,
                               birthday=%s, group_id=%s WHERE id=%s""",
                            (row.get("last_name") or None,
                             row.get("email") or None,
                             bday, gid, cid))
                    else:
                        cur.execute(
                            """INSERT INTO contacts
                               (first_name, last_name, email, birthday, group_id)
                               VALUES (%s,%s,%s,%s,%s) RETURNING id""",
                            (first,
                             row.get("last_name") or None,
                             row.get("email") or None,
                             bday, gid))
                        cid = cur.fetchone()["id"]

                    phone     = row.get("phone", "").strip()
                    phone_type = row.get("phone_type", "mobile").strip().lower()
                    if phone_type not in ("home", "work", "mobile"):
                        phone_type = "mobile"

                    if phone:
                        # avoid duplicates
                        cur.execute(
                            "SELECT id FROM phones WHERE contact_id=%s AND phone=%s",
                            (cid, phone))
                        if not cur.fetchone():
                            cur.execute(
                                "INSERT INTO phones (contact_id, phone, type) "
                                "VALUES (%s,%s,%s)",
                                (cid, phone, phone_type))

                    ok_count += 1
                except Exception as e:
                    errors.append(f"Row {i}: {e}")

        conn.commit()
        ok(f"Imported {ok_count} row(s).")
        for e in errors:
            err(e)
    except Exception as e:
        conn.rollback(); err(str(e))
    finally:
        cur.close(); conn.close()


def stored_procs_menu():
    h1("Stored Procedures")
    action = pick("Procedure", [
        "add_phone",
        "move_to_group",
        "search_contacts (function)",
        "Back",
    ])
    if action == "Back":
        return

    conn = get_conn()
    cur  = get_cursor(conn)
    try:
        if action == "add_phone":
            name  = prompt("Contact first name")
            phone = prompt("Phone number")
            ptype = pick("Phone type", ["mobile", "home", "work"])
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
            conn.commit(); ok("Done.")

        elif action == "move_to_group":
            name = prompt("Contact first name")
            grp  = prompt("Target group name")
            cur.execute("CALL move_to_group(%s, %s)", (name, grp))
            conn.commit(); ok("Done.")

        elif action.startswith("search_contacts"):
            q = prompt("Search query")
            cur.execute("SELECT * FROM search_contacts(%s)", (q,))
            rows = enrich_rows(cur, cur.fetchall())
            _print_contacts(rows)

    except Exception as e:
        conn.rollback(); err(str(e))
    finally:
        cur.close(); conn.close()


MENU = [
    ("Add contact",              add_contact),
    ("Search / filter contacts", search_menu),
    ("Edit contact",             edit_contact),
    ("Delete contact",           delete_contact),
    ("Export to JSON",           export_json),
    ("Import from JSON",         import_json),
    ("Import from CSV",          import_csv),
    ("Stored procedures demo",   stored_procs_menu),
    ("Exit",                     None),
]


def main():
    # Bootstrap DB on first run
    from connect import run_sql_file
    for sql_file in ("schema.sql", "procedures.sql"):
        if os.path.exists(sql_file):
            run_sql_file(sql_file)

    while True:
        h1("📒  PhoneBook — TSIS 1")
        for i, (label, _) in enumerate(MENU, 1):
            print(f"  {CYAN}{i}{RESET}. {label}")
        raw = input("\n  Choice: ").strip()
        if not raw.isdigit() or not (1 <= int(raw) <= len(MENU)):
            err("Invalid choice."); continue
        label, fn = MENU[int(raw) - 1]
        if fn is None:
            print(f"\n{GREEN}  Goodbye!{RESET}\n"); sys.exit(0)
        try:
            fn()
        except KeyboardInterrupt:
            print()


if __name__ == "__main__":
    main()