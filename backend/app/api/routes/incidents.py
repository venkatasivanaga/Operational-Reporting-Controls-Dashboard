from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.models.incident import Incident
from backend.app.schemas.incident import IncidentCreate, IncidentOut, IncidentUpdate

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("", response_model=list[IncidentOut])
def list_incidents(
    db: Session = Depends(get_db),
    q: str | None = Query(default=None, description="Search in code/title/owner/service"),
    status: str | None = Query(default=None),
    severity: str | None = Query(default=None),
    service: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    query = db.query(Incident)

    if q:
        like = f"%{q}%"
        query = query.filter(
            (Incident.incident_code.ilike(like)) |
            (Incident.title.ilike(like)) |
            (Incident.owner.ilike(like)) |
            (Incident.service.ilike(like))
        )
    if status:
        query = query.filter(Incident.status == status)
    if severity:
        query = query.filter(Incident.severity == severity)
    if service:
        query = query.filter(Incident.service == service)

    return query.order_by(Incident.id.desc()).offset(offset).limit(limit).all()


@router.post("", response_model=IncidentOut, status_code=201)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    existing = db.query(Incident).filter(Incident.incident_code == payload.incident_code).first()
    if existing:
        raise HTTPException(status_code=409, detail="incident_code already exists")

    obj = Incident(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{incident_id}", response_model=IncidentOut)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    obj = db.query(Incident).filter(Incident.id == incident_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Incident not found")
    return obj


@router.put("/{incident_id}", response_model=IncidentOut)
def update_incident(incident_id: int, payload: IncidentUpdate, db: Session = Depends(get_db)):
    obj = db.query(Incident).filter(Incident.id == incident_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Incident not found")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{incident_id}", status_code=204)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    obj = db.query(Incident).filter(Incident.id == incident_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Incident not found")

    db.delete(obj)
    db.commit()
    return None
