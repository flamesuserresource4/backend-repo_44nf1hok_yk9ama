import os
from datetime import date
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Office, Team, Session

app = FastAPI(title="Naitika Foundations API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Naitika Foundations Backend Running"}

@app.get("/test")
def test_database():
    resp = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "collections": []
    }
    try:
        if db is not None:
            resp["database"] = "✅ Connected"
            try:
                resp["collections"] = db.list_collection_names()
            except Exception as e:
                resp["database"] = f"⚠️ Connected but error: {str(e)[:80]}"
    except Exception as e:
        resp["database"] = f"❌ Error: {str(e)[:80]}"
    return resp

# --- Office Endpoints ---
class OfficeOut(Office):
    id: Optional[str] = None

@app.post("/offices", response_model=dict)
async def create_office(office: Office):
    oid = create_document("office", office)
    return {"id": oid}

@app.get("/offices", response_model=List[dict])
async def list_offices():
    docs = get_documents("office")
    # convert _id to string
    return [{**{k: v for k, v in d.items() if k != "_id"}, "id": str(d.get("_id"))} for d in docs]

# --- Team Endpoints ---
@app.post("/teams", response_model=dict)
async def create_team(team: Team):
    tid = create_document("team", team)
    return {"id": tid}

@app.get("/teams", response_model=List[dict])
async def list_teams():
    docs = get_documents("team")
    return [{**{k: v for k, v in d.items() if k != "_id"}, "id": str(d.get("_id"))} for d in docs]

# --- Session Endpoints ---
@app.post("/sessions", response_model=dict)
async def create_session(session: Session):
    sid = create_document("session", session)
    return {"id": sid}

@app.get("/sessions", response_model=List[dict])
async def list_sessions(date_eq: Optional[date] = None, office_id: Optional[str] = None, status: Optional[str] = None):
    filt = {}
    if date_eq is not None:
        filt["date"] = date_eq
    if office_id is not None:
        filt["office_id"] = office_id
    if status is not None:
        filt["status"] = status
    docs = get_documents("session", filt)
    return [{**{k: v for k, v in d.items() if k != "_id"}, "id": str(d.get("_id"))} for d in docs]

@app.get("/schema")
async def get_schema_info():
    # The platform uses this to introspect schemas
    return {
        "schemas": {
            "office": Office.model_json_schema(),
            "team": Team.model_json_schema(),
            "session": Session.model_json_schema(),
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
