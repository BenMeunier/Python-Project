#!/usr/bin/env python3
import argparse, csv, datetime, re, sqlite3, sys
from pathlib import Path

DB = Path("tasks.db")

SCHEMA = """
Create table if not exists tasks(
 id Integer Primary Key Autoincrement,
 title Text Not Null,
 note Text,
 created_at Text Not Null,
 due Text,
 completed Integer Not Null Default 0
);
"""

def conn(db): 
    c = sqlite3.connect(db)
    c.row_factory = sqlite3.Row
    return c

def init(db):
    c = conn(db)
    c.executescript(SCHEMA); c.commit(); c.close()
    print(f"DB initialized at {db}")

def add(db,t,n,d):
    if d and not re.match(r"^\d{4}-\d{2}-\d{2}$", d):
        sys.exit("Invalid --due (YYYY-MM-DD)")
    c = conn(db)
    c.execute("Insert Into tasks(title,note,created_at,due) Values(?,?,?,?)",
              (t,n,datetime.date.today().isoformat(),d))
    c.commit(); c.close()
    print("Task added")

def rm(db,i):
    c = conn(db); r = c.execute("Delete From tasks Where id=?", (i,))
    c.commit(); c.close()
    print("Removed" if r.rowcount else f"No task id {i}")

def done(db,i):
    c = conn(db); r = c.execute("Update tasks Set completed=1 Where id=?", (i,))
    c.commit(); c.close()
    print("Completed" if r.rowcount else f"No task id {i}")

def ls(db,f):
    q = "Select * From tasks"
    if f == "yes": q += " Where completed=1"
    if f == "no":  q += " Where completed=0"
    c = conn(db)
    rows = c.execute(q + " Order By completed,due Is Not Null,due").fetchall()
    c.close()
    if not rows: return print("No tasks")
    for r in rows:
        print(f"[{r['id']}] [{'✓' if r['completed'] else ' '}] {r['title']} (due:{r['due'] or '-'})")
        if r['note']: print("   " + r['note'])

def search(db,pat):
    try: rg = re.compile(pat, re.I)
    except re.error as e: sys.exit(f"Bad regex: {e}")
    c = conn(db)
    rows = c.execute("Select * From tasks").fetchall()
    c.close()
    m = [r for r in rows if rg.search((r['title'] or "") + "\n" + (r['note'] or ""))]
    if not m: return print("No matches")
    for r in m:
        print(f"[{r['id']}] [{'✓' if r['completed'] else ' '}] {r['title']}")

def expcsv(db,out):
    c = conn(db)
    rows = c.execute("Select title,note,due,completed FROM tasks").fetchall()
    c.close()
    with open(out,"w",newline='',encoding="utf8") as f:
        w = csv.writer(f)
        w.writerow(["title","note","due","completed"])
        for r in rows: w.writerow(r)
    print(f"Exported {len(rows)} tasks")

def impcsv(db,inf):
    c = conn(db); cnt=0
    with open(inf,newline='',encoding="utf8") as f:
        for row in csv.DictReader(f):
            if not row.get("title"): continue
            c.execute("Iinsert Into tasks(title,note,created_at,due,completed) Values(?,?,?,?,?)",
                      (row["title"], row.get("note"),
                       datetime.date.today().isoformat(),
                       row.get("due"),
                       1 if row.get("completed")=="1" else 0))
            cnt+=1
    c.commit(); c.close()
    print(f"Imported {cnt} tasks")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--db", type=Path, default=DB)
    s = p.add_subparsers(dest="cmd", required=True)

    s.add_parser("init")
    a = s.add_parser("add"); a.add_argument("title"); a.add_argument("--note"); a.add_argument("--due")
    r = s.add_parser("remove"); r.add_argument("id", type=int)
    c = s.add_parser("complete"); c.add_argument("id", type=int)
    l = s.add_parser("list"); l.add_argument("--completed", choices=["yes","no"])
    f = s.add_parser("search"); f.add_argument("pattern")
    e = s.add_parser("export-csv"); e.add_argument("out")
    i = s.add_parser("import-csv"); i.add_argument("infile")

    a = p.parse_args()
    db = a.db

    if a.cmd == "init": return init(db)
    if not db.exists(): sys.exit("Database missing — run init first")

    match a.cmd:
        case "add": add(db,a.title,a.note,a.due)
        case "remove": rm(db,a.id)
        case "complete": done(db,a.id)
        case "list": ls(db,a.completed)
        case "search": search(db,a.pattern)
        case "export-csv": expcsv(db,a.out)
        case "import-csv": impcsv(db,a.infile)

if __name__ == "__main__":
    main()
