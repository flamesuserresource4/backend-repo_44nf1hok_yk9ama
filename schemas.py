"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection (collection name = lowercase of class name).

Collections for this app:
- Office: each physical hub/office with map coordinates
- Team: field staff associated with an office
- Session: daily sessions conducted in villages
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import datetime as dt

class Office(BaseModel):
    """Offices collection schema (collection name: "office")"""
    name: str = Field(..., description="Office or hub name (e.g., Guntur HQ)")
    address: Optional[str] = Field(None, description="Street address")
    mandal: Optional[str] = Field(None, description="Mandal or region")
    phone: Optional[str] = Field(None, description="Primary contact phone")
    email: Optional[EmailStr] = Field(None, description="Contact email")
    lat: float = Field(..., description="Latitude for map")
    lng: float = Field(..., description="Longitude for map")

class Team(BaseModel):
    """Teams collection schema (collection name: "team")"""
    name: str = Field(..., description="Team member name")
    role: Optional[str] = Field(None, description="Role or title")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[EmailStr] = Field(None, description="Email address")
    office_id: Optional[str] = Field(None, description="Related office id (string)")

class Session(BaseModel):
    """Sessions collection schema (collection name: "session")"""
    date: dt.date = Field(..., description="Session date (YYYY-MM-DD)")
    village: str = Field(..., description="Village name")
    start_time: Optional[str] = Field(None, description="Start time, local (e.g., 10:00)")
    end_time: Optional[str] = Field(None, description="End time, local (e.g., 11:00)")
    learners_count: int = Field(0, ge=0, description="Number of learners present")
    status: str = Field("Scheduled", description="Status: Scheduled/Running/Completed/Cancelled")
    team_id: Optional[str] = Field(None, description="Team member id (string)")
    office_id: Optional[str] = Field(None, description="Office id (string)")
    notes: Optional[str] = Field(None, description="Additional notes")
