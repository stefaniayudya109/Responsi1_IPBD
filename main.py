from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open("wired_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def home():
    return {"message": "API Wired Articles aktif"}

@app.get("/articles")
def get_articles():
    data = load_data()
    return {
        "total": len(data),
        "data": data
    }