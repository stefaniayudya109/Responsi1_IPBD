import requests
import psycopg2


res = requests.get("http://host.docker.internal:8000/articles")
data = res.json()["data"]

conn = psycopg2.connect(
    host="localhost",
    port=5433,
    database="wired_db",
    user="admin",
    password="admin"
)

cur = conn.cursor()

for item in data:
    cur.execute("""
        INSERT INTO wired_articles (title, url, description, author, scraped_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        item["title"],
        item["url"],
        item["description"],
        item["author"],
        item["scraped_at"]
    ))

conn.commit()
cur.close()
conn.close()

print("Data masuk ke database!")