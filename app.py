from fastapi import FastAPI, Header, HTTPException
from monitor import check_once
import os

app = FastAPI()


@app.get("/")
def home():
    return {
        "status": "ok",
        "service": "zealy-monitor"
    }


@app.get("/api")
def api_home():
    return {
        "status": "ok",
        "service": "zealy-monitor"
    }


@app.get("/api/monitor")
def monitor(authorization: str | None = Header(default=None)):
    secret = os.getenv("CRON_SECRET")

    if secret and authorization != f"Bearer {secret}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    return check_once()
