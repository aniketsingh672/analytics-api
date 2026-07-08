from collections import defaultdict

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

API_KEY = "ak_88u3mm7plnrfsv1urhtlw824"
EMAIL = "YOUR_EMAIL@example.com"   # <-- Replace with your exam/login email

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: list[Event]


@app.get("/")
def home():
    return {"status": "ok"}


@app.post("/analytics")
def analytics(
    body: AnalyticsRequest,
    x_api_key: str = Header(None, alias="X-API-Key"),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    total_events = len(body.events)
    unique_users = len({e.user for e in body.events})

    revenue = 0.0
    totals = defaultdict(float)

    for e in body.events:
        if e.amount > 0:
            revenue += e.amount
            totals[e.user] += e.amount

    top_user = max(totals, key=totals.get) if totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }
