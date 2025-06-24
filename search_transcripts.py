import sqlite3

DB_NAME = "transcripts.db"

def search(term):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    query = """
    SELECT DISTINCT file, start, end, text FROM segments
    WHERE text LIKE ?
    ORDER BY file, start
    """
    cur.execute(query, (f"%{term}%",))
    results = cur.fetchall()
    conn.close()

    if not results:
        print("No results found.")
        return

    for file, start, end, text in results:
        print(f"\n🎙️  {file} [{start:.2f} - {end:.2f}]")
        print(f"🗣️  {text}")

if __name__ == "__main__":
    while True:
        term = input("\nEnter word or phrase to search (or 'q' to quit): ").strip()
        if term.lower() == 'q':
            break
        search(term)
